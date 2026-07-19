"""
Распознавание чеков пополнения (OCR) полностью в памяти.

Фото чека НЕ сохраняется на диск: на вход принимаем байты изображения,
декодируем через cv2.imdecode из numpy-буфера, буфер живёт только на время
проверки. Модуль рассчитан на слабый сервер (~1 ГБ RAM), поэтому число
проходов Tesseract сведено к минимуму.

Публичная точка входа — verify_topup_bytes(...). Внутри бота её нужно вызывать
через asyncio.to_thread(...), т.к. Tesseract/OpenCV блокируют поток.
"""
import re
from dataclasses import dataclass, field
from datetime import datetime

import cv2
import numpy as np
import pytesseract
from pytesseract import Output


# Куда должны были прийти деньги (нормализуется: нижний регистр, без пробелов).
RECIPIENT_MARKERS = [
    "бакай",
    "bakai",
    "771514979",
    "996771514979",
]

# Рядом с этими словами число — это НЕ сумма перевода (остаток, комиссия и т.п.).
BAD_ANCHORS = [
    "остаток", "комисси",
    "счет списания", "счёт списания", "со счета", "со счёта",
    "реквизит", "карта",
]

MIN_CONFIDENCE = 55
ANCHOR_LOOKBACK = 40
AMOUNT_TOLERANCE = 0.01
FUTURE_TOLERANCE_MINUTES = 5

_MONTHS = {
    "января": 1, "февраля": 2, "марта": 3, "апреля": 4,
    "мая": 5, "июня": 6, "июля": 7, "августа": 8,
    "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12,
}


@dataclass
class TopupResult:
    ok: bool
    expected_amount: float
    found_amounts: list
    recipient_verified: bool
    transaction_id: str | None
    receipt_datetime: datetime | None
    delay_minutes: float | None
    confidence: float
    raw_text: str
    reasons: list = field(default_factory=list)


def _decode(image_bytes: bytes):
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Не удалось декодировать изображение")
    return img


def _preprocess_variants(image_bytes: bytes):
    """Лёгкий набор вариантов (2 прохода вместо 4) — экономим RAM/CPU."""
    raw = _decode(image_bytes)

    h = raw.shape[0]
    cropped = raw[int(h * 0.05):, :]  # срезаем шапку приложения

    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    up = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    binary = cv2.adaptiveThreshold(
        up, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15
    )
    return [("gray", up), ("binary", binary)]


def _avg_conf(data: dict) -> float:
    c = [int(x) for x in data["conf"] if int(x) != -1]
    return sum(c) / len(c) if c else 0.0


def _run_ocr(image_bytes: bytes) -> tuple[str, float]:
    best_text, best_conf = "", 0.0
    for _, img in _preprocess_variants(image_bytes):
        for psm in (6, 4):
            try:
                data = pytesseract.image_to_data(
                    img, lang="rus+eng", config=f"--oem 3 --psm {psm}",
                    output_type=Output.DICT,
                )
            except pytesseract.TesseractError:
                continue
            conf = _avg_conf(data)
            if conf > best_conf:
                best_conf = conf
                best_text = " ".join(w for w in data["text"] if w.strip())
    return best_text, best_conf


def _find_amounts(text: str) -> list:
    found = []
    tl = text.lower()
    for m in re.finditer(r'(\d[\d\s]{0,8}[.,]\d{2}|\d{1,6})\s*(KGS|kgs|[сcC©€])', text):
        ctx = tl[max(0, m.start() - ANCHOR_LOOKBACK):m.start()]
        if any(b in ctx for b in BAD_ANCHORS):
            continue
        try:
            val = float(m.group(1).replace(" ", "").replace(",", "."))
        except ValueError:
            continue
        if 0 < val <= 1_000_000:
            found.append(val)
    return found


def _verify_recipient(text: str) -> bool:
    norm = text.lower().replace(" ", "")
    return any(mk in norm for mk in RECIPIENT_MARKERS)


def _extract_tx_id(text: str) -> str | None:
    m = re.search(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}(?:-[0-9a-fA-F]{4})?', text)
    if m:
        return m.group(0)
    m = re.search(r'[РP]\d{10,15}', text)
    if m:
        return "P" + m.group(0)[1:]
    m = re.search(r'(?:№|No|N[оo]?)\s*[РP]?(\d{10,14})', text)
    if m:
        return m.group(1)
    return None


def extract_receipt_datetime(text: str) -> datetime | None:
    tl = text.lower()

    m = re.search(r'(\d{1,2})\.(\d{2})\.(\d{4})[,\s]+(\d{1,2}):(\d{2})(?::(\d{2}))?', text)
    if m:
        d, mo, y, h, mi, s = m.groups()
        try:
            return datetime(int(y), int(mo), int(d), int(h), int(mi), int(s or 0))
        except ValueError:
            pass

    m = re.search(r'(\d{1,2}):(\d{2})[,\s]+(\d{1,2})\.(\d{2})\.(\d{4})', text)
    if m:
        h, mi, d, mo, y = m.groups()
        try:
            return datetime(int(y), int(mo), int(d), int(h), int(mi))
        except ValueError:
            pass

    m = re.search(r'(\d{1,2})\s+([а-яё]+)\s+(\d{4})[,\s]+(\d{1,2}):(\d{2})', tl)
    if m:
        d, mon, y, h, mi = m.groups()
        if mon in _MONTHS:
            try:
                return datetime(int(y), _MONTHS[mon], int(d), int(h), int(mi))
            except ValueError:
                pass

    m = re.search(r'(\d{1,2})\.(\d{2})\.(\d{2})\s+(\d{1,2}):(\d{2})', text)
    if m:
        d, mo, y, h, mi = m.groups()
        try:
            return datetime(2000 + int(y), int(mo), int(d), int(h), int(mi))
        except ValueError:
            pass

    return None


def verify_topup_bytes(
    image_bytes: bytes,
    expected_amount: float,
    now: datetime | None = None,
    max_delay_minutes: int = 180,
) -> TopupResult:
    """
    Проверяет чек из байтов. Возвращает TopupResult.
    ok=True только если: получатель верный + сумма совпала + OCR уверен +
    (если передан now) время чека свежее и не из будущего.
    """
    reasons: list = []

    try:
        text, conf = _run_ocr(image_bytes)
    except ValueError as e:
        return TopupResult(
            ok=False, expected_amount=expected_amount, found_amounts=[],
            recipient_verified=False, transaction_id=None, receipt_datetime=None,
            delay_minutes=None, confidence=0.0, raw_text="", reasons=[str(e)],
        )

    if not text.strip():
        return TopupResult(
            ok=False, expected_amount=expected_amount, found_amounts=[],
            recipient_verified=False, transaction_id=None, receipt_datetime=None,
            delay_minutes=None, confidence=conf, raw_text="",
            reasons=["OCR вернул пустой текст"],
        )

    amounts = _find_amounts(text)
    recipient_ok = _verify_recipient(text)
    tx_id = _extract_tx_id(text)
    receipt_dt = extract_receipt_datetime(text)
    amount_match = any(abs(a - expected_amount) < AMOUNT_TOLERANCE for a in amounts)

    if not recipient_ok:
        reasons.append("получатель не подтверждён")
    if not amount_match:
        reasons.append(f"сумма {expected_amount} не найдена (найдено: {amounts})")
    if conf < MIN_CONFIDENCE:
        reasons.append(f"низкая уверенность OCR ({conf:.0f}%)")

    delay_minutes = None
    time_ok = True
    if now is not None:
        if receipt_dt is None:
            time_ok = False
            reasons.append("дата/время на чеке не распознаны")
        else:
            delay_minutes = (now - receipt_dt).total_seconds() / 60.0
            if delay_minutes < -FUTURE_TOLERANCE_MINUTES:
                time_ok = False
                reasons.append("время на чеке из будущего")
            elif delay_minutes > max_delay_minutes:
                time_ok = False
                reasons.append(f"чек слишком старый ({delay_minutes:.0f} мин)")

    ok = recipient_ok and amount_match and conf >= MIN_CONFIDENCE and time_ok

    return TopupResult(
        ok=ok, expected_amount=expected_amount, found_amounts=amounts,
        recipient_verified=recipient_ok, transaction_id=tx_id,
        receipt_datetime=receipt_dt, delay_minutes=delay_minutes,
        confidence=conf, raw_text=text, reasons=reasons,
    )
