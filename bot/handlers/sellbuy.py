import logging
from datetime import datetime, timedelta, timezone
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InputMediaPhoto
)
from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.services.sellbuy_service import SellBuyService
from bot.services.profile_service import ProfileService
from aiogram.types import FSInputFile
from pathlib import Path

from bot.channels import (
    CHANNELS,
    ADMIN_ID,
    SLUG_TO_CATEGORY,
    CATEGORY_TO_SLUG,
    get_category_label,
    get_status_keys,
    get_status_label,
    get_subcategory_keys,
    get_subcategory_label,
    get_cooldown_days,
    get_placement_price,
    get_currencies,
    get_favorite_link,
)
from bot.handlers.menu_handler import show_menu_prompt, send_not_registered, get_main_menu_keyboard

logger = logging.getLogger(__name__)

sellbuy_router = Router()

STEP_KEYS = ['status', 'subcategory', 'name', 'desc', 'price', 'photos', 'phone']
MAX_SUBCATS = 2

MAX_NAME_LEN = 100
MAX_DESC_LEN = 650
MAX_PRICE = 1_000_000_000

# Цена 0 в БД = «Договорная» (без миграции схемы: поле price NOT NULL Integer).
NEGOTIABLE_PRICE = 0
NEGOTIABLE_WORDS = {
    'договорная', 'договор', 'келишим', 'келишим баада',
    'negotiable', 'nego', '面议',
}

_publishing = set()


def money(amount, lang: str) -> str:
    return f"{amount} {t('currency', lang)}"


def format_price(price, currency, lang: str) -> str:
    currency = currency or 'KGS'
    try:
        value = int(price)
    except (TypeError, ValueError):
        value = 0
    if value == NEGOTIABLE_PRICE:
        return t('price_negotiable', lang)
    grouped = f"{value:,}".replace(",", " ")
    return f"{grouped} {currency}"


def build_channel_caption(hashtags, owner, status_ru, name, desc, price_text,
                          phone_text, user_id, fav_ad_id=None) -> str:
    fav_line = ''
    if fav_ad_id is not None:
        fav_line = (
            f"⭐️ <a href='{get_favorite_link(fav_ad_id)}'>Добавить в избранное</a>\n"
        )
    return (
        f'<b>{hashtags}</b>\n'
        f'<b>{owner}</b>\n'
        f"<b>{status_ru}</b>\n"
        f"🏷️ <b>{name}</b>\n\n"
        f"{desc}\n\n"
        f"💵 Цена: {price_text}\n"
        f"{phone_text}\n"
        f"✉️ <a href='tg://user?id={user_id}'>Написать продавцу</a>\n"
        f"{fav_line}"
        f"📢 <a href='https://t.me/tez4917_bot'>Разместить объявление</a>"
    )


def breadcrumbs(lang: str, current: str) -> str:
    parts = []
    reached = False
    for key in STEP_KEYS:
        label = t(f'step_{key}', lang)
        if key == current:
            parts.append(f"🔵 {label}")
            reached = True
        elif not reached:
            parts.append(f"✅ {label}")
        else:
            parts.append(f"⚪ {label}")
    return "🧭 " + " · ".join(parts)


def build_status_keyboard(category: str, lang: str) -> InlineKeyboardMarkup:
    keys = get_status_keys(category)
    rows = [
        [
            InlineKeyboardButton(text=get_status_label(category, key, lang), callback_data=f"sb_status_{key}")
            for key in keys[i:i + 3]
        ]
        for i in range(0, len(keys), 3)
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_subcat_keyboard(category: str, lang: str, selected: list) -> InlineKeyboardMarkup:
    keys = get_subcategory_keys(category)
    rows = []
    for i in range(0, len(keys), 2):
        row = []
        for key in keys[i:i + 2]:
            mark = '✅ ' if key in selected else ''
            row.append(InlineKeyboardButton(
                text=f"{mark}{get_subcategory_label(category, key, lang)}",
                callback_data=f"sb_subtog_{key}"
            ))
        rows.append(row)
    rows.append([InlineKeyboardButton(text=t('btn_subcat_done', lang), callback_data="sb_sub_done")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def ask_photos(target, state: FSMContext, lang: str):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t('done_button', lang))], [KeyboardButton(text=t('menu_button', lang))]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await target.answer(
        breadcrumbs(lang, 'photos') + "\n\n" + t('add_photos', lang),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.photos)


class SellFSM(StatesGroup):
    category = State()
    status = State()
    subcategory = State()
    name = State()
    desc = State()
    price = State()
    currency = State()
    photos = State()
    show_phone = State()
    confirm = State()

class PaidAnnouncement(StatesGroup):
    waiting_for_payment = State()


@sellbuy_router.message(Command("market"))
async def start_sell_command(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(message.from_user.id)
        lang = client.language if client and client.language else 'ru'

    if not client:
        await send_not_registered(message)
        return
    if client.is_banned:
        await message.answer(t('banned', lang))
        return

    buttons = []

    for name in CHANNELS.keys():
        slug = CATEGORY_TO_SLUG[name]
        button_text = get_category_label(name, lang)
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"sb_cat_{slug}")])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(t('sell_create', lang), reply_markup=kb, parse_mode="HTML")
    await state.set_state(SellFSM.category)


@sellbuy_router.callback_query(F.data == "sellbuy")
async def start_sell(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

    if not client:
        await send_not_registered(callback)
        await callback.answer()
        return
    if client.is_banned:
        await callback.message.answer(t('banned', lang))
        await callback.answer()
        return

    buttons = []

    for name in CHANNELS.keys():
        slug = CATEGORY_TO_SLUG[name]
        button_text = get_category_label(name, lang)
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"sb_cat_{slug}")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.answer(t('sell_create', lang), reply_markup=kb, parse_mode="HTML")
    await state.set_state(SellFSM.category)
    await callback.answer()

@sellbuy_router.callback_query(F.data.startswith('sb_cat_'))
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

    slug = callback.data.removeprefix('sb_cat_')
    category = SLUG_TO_CATEGORY.get(slug)
    if not category:
        await callback.answer(t('unknown_category', lang), show_alert=True)
        return

    if not client:
        await send_not_registered(callback)
        await state.clear()
        return

    subscription_date = getattr(client, "next_subscription_disable", None)
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    subscription_text = None

    if subscription_date:
        sub_naive = subscription_date.replace(tzinfo=None)
        if sub_naive > now_naive:
            delta = sub_naive - now_naive
            time_parts = []

            if delta.days > 0:
                time_parts.append(f"{delta.days} {t('days', lang)}")
            if delta.seconds >= 3600:
                hours = delta.seconds // 3600
                time_parts.append(f"{hours} {t('hours', lang)}")
            if delta.seconds >= 60:
                minutes = (delta.seconds % 3600) // 60
                time_parts.append(f"{minutes} {t('minutes', lang)}")
            
            subscription_text = t('subscription_active', lang).format(time=' '.join(time_parts))
            await state.update_data(category=category, category_slug=slug, subcats=[])

            kb = build_status_keyboard(category, lang)

            category_display = get_category_label(category, lang)
            await callback.message.delete()
            await callback.message.answer(subscription_text, parse_mode="HTML")
            await callback.message.answer(
                t('flow_start_notice', lang) + "\n\n"
                + breadcrumbs(lang, 'status') + "\n\n"
                + t('choose_status', lang).format(category=category_display),
                reply_markup=kb,
                parse_mode="HTML"
            )
            await state.set_state(SellFSM.status)
            return

    field = CHANNELS[category]["cooldown_field"]
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    next_allowed = getattr(client, field)
    if next_allowed:
        next_allowed = next_allowed.replace(tzinfo=None) if next_allowed.tzinfo else next_allowed

    if next_allowed and next_allowed > now:
        wait = next_allowed - now
        total_minutes = int(wait.total_seconds() // 60)
        days = total_minutes // (24 * 60)
        hours = (total_minutes % (24 * 60)) // 60
        minutes = total_minutes % 60
        parts = []
        if days:
            parts.append(f"{days} {t('days', lang)}")
        if hours:
            parts.append(f"{hours} {t('hours', lang)}")
        if minutes:
            parts.append(f"{minutes} {t('minutes', lang)}")
        if not parts:
            parts.append(f"{t('less_than_minute', lang)}")
        time_str = ' '.join(parts)

        price = get_placement_price(category)
        category_display = get_category_label(category, lang)
        await state.update_data(category=category, category_slug=slug)

        pay_kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=t('btn_confirm_yes', lang), callback_data=f"sb_cdpay_yes|{slug}"),
            InlineKeyboardButton(text=t('btn_confirm_no', lang), callback_data="sb_cdpay_no"),
        ]])
        await callback.message.edit_text(
            t('wait_cooldown', lang).format(category=category_display, time=time_str) + "\n\n"
            + t('cooldown_pay_offer', lang).format(
                price=money(price, lang), balance=money(client.balance, lang)
            ),
            reply_markup=pay_kb,
            parse_mode="HTML"
        )
        return

    await state.update_data(category=category, category_slug=slug, subcats=[])

    kb = build_status_keyboard(category, lang)

    category_display = get_category_label(category, lang)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(
        t('flow_start_notice', lang) + "\n\n"
        + breadcrumbs(lang, 'status') + "\n\n"
        + t('choose_status', lang).format(category=category_display),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.status)


@sellbuy_router.callback_query(F.data.startswith('sb_cdpay_yes|'))
async def cooldown_pay_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    _, slug = callback.data.split('|', 1)
    category = SLUG_TO_CATEGORY.get(slug)
    if not category:
        return

    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'
        if not client:
            await send_not_registered(callback)
            await state.clear()
            return

        price = get_placement_price(category)
        charged = await ProfileService(session).try_charge(client.id, price)
        if not charged:
            await callback.message.edit_text(
                t('cooldown_low_balance', lang).format(
                    price=money(price, lang), balance=money(client.balance, lang)
                ),
                parse_mode="HTML"
            )
            await state.clear()
            await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            return
        await service.clear_next_ability_for_category(callback.from_user.id, slug)

    await state.update_data(category=category, category_slug=slug, subcats=[])
    kb = build_status_keyboard(category, lang)
    await callback.message.edit_text(
        t('cooldown_paid', lang) + "\n\n"
        + breadcrumbs(lang, 'status') + "\n\n"
        + t('choose_status', lang).format(category=get_category_label(category, lang)),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.status)


@sellbuy_router.callback_query(F.data == 'sb_cdpay_no')
async def cooldown_pay_no(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(t('cancel', lang))
    await show_menu_prompt(callback.from_user.id, callback.bot, lang)

@sellbuy_router.callback_query(F.data.startswith('sb_paid|'))
async def paid_announcement(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    await callback.answer()
    try:
        _, slug, payer_id = callback.data.split('|', 2)
    except ValueError:
        await callback.message.answer(t('error_invalid_data', lang))
        return

    category = SLUG_TO_CATEGORY.get(slug)
    if not category:
        await callback.message.answer(t('unknown_category', lang))
        return

    qr_path = Path(__file__).resolve().parent.parent / 'assets' / 'mbank_qr.jpg'
    photo_qr = FSInputFile(qr_path)

    await state.update_data(paid_for_category_slug=slug, paid_for_category=category, payer_id=str(payer_id))
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo_qr,
        caption=t('paid_placement', lang)
    )
    await state.set_state(PaidAnnouncement.waiting_for_payment)

@sellbuy_router.message(PaidAnnouncement.waiting_for_payment)
async def waiting_for_payment(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)

    data = await state.get_data()
    payer_id = data.get('payer_id') or str(message.from_user.id)
    category_slug = data.get('paid_for_category_slug')

    file_id = None
    if message.photo:
        file_id = message.photo[-1].file_id
    elif getattr(message, "document", None) and (message.document.mime_type or "").startswith("image/"):
        file_id = message.document.file_id

    if not file_id:
        await message.answer(t('send_receipt_photo', lang))
        return

    category = SLUG_TO_CATEGORY.get(category_slug, t('unknown_category', lang))

    caption = (
        f"💳 Новый чек на проверку\n\n"
        f"Категория: <b>{category}</b>\n"
        f"👤 @{message.from_user.username or 'Без username'}\n"
        f"🆔 <code>{payer_id}</code>\n"
        f"📅 {(datetime.utcnow() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')}"
    )

    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Подтвердить оплату", callback_data=f"sb_confirm|{payer_id}|{category_slug}"),
        InlineKeyboardButton(text="❌ Отклонить оплату", callback_data=f"sb_decline|{payer_id}|{category_slug}")
    ]])

    try:
        await message.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=ikb
        )
        await message.answer(t('receipt_sent', lang))
        await state.clear()
    except Exception as e:
        await message.answer(t('error_sending_receipt', lang).format(error=str(e)))

@sellbuy_router.callback_query(F.data.startswith('sb_confirm|'))
async def admin_confirm_payment(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Только админ может подтверждать оплату.", show_alert=True)
        return

    try:
        _, payer_id, slug = callback.data.split('|', 2)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    category = SLUG_TO_CATEGORY.get(slug)
    if not category:
        await callback.answer("Неизвестная категория.", show_alert=True)
        return

    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.clear_next_ability_for_category(int(payer_id), slug)
        lang_user = client.language if client and client.language else 'ru'

    try:
        await callback.bot.send_message(
            int(payer_id),
            t('payment_confirmed', lang_user).format(category=category)
        )
        # Убираем инлайн-кнопки, но оставляем caption
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Оплата подтверждена.")
    except Exception as e:
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)

@sellbuy_router.callback_query(F.data.startswith('sb_decline|'))
async def admin_decline_payment(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Только админ может отклонять оплату.", show_alert=True)
        return

    try:
        _, payer_id, slug = callback.data.split('|', 2)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    category = SLUG_TO_CATEGORY.get(slug, "(неизвестно)")

    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang_user = await service.get_user_lang(int(payer_id))

    try:
        await callback.bot.send_message(
            int(payer_id),
            t('payment_declined', lang_user).format(category=category)
        )
        # Убираем инлайн-кнопки, но оставляем caption
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Оплата отклонена.")
    except Exception as e:
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)

@sellbuy_router.callback_query(F.data.startswith('sb_status_'))
async def choose_status(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    await callback.answer()
    data = await state.get_data()
    category = data.get('category')

    status_key = callback.data.removeprefix('sb_status_')
    # Храним КЛЮЧ статуса, а не готовую подпись: подпись рендерим на языке
    # пользователя для превью и по-русски для канала.
    await state.update_data(status_key=status_key, subcats=[])

    kb = build_subcat_keyboard(category, lang, [])
    await callback.message.edit_text(
        breadcrumbs(lang, 'subcategory') + "\n\n" + t('choose_subcategories', lang),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.subcategory)


@sellbuy_router.callback_query(SellFSM.subcategory, F.data.startswith('sb_subtog_'))
async def toggle_subcategory(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    data = await state.get_data()
    category = data.get('category')
    selected = list(data.get('subcats', []))
    subkey = callback.data.removeprefix('sb_subtog_')

    if subkey in selected:
        selected.remove(subkey)
    else:
        if len(selected) >= MAX_SUBCATS:
            await callback.answer(t('subcat_max', lang).format(n=MAX_SUBCATS), show_alert=True)
            return
        selected.append(subkey)

    await state.update_data(subcats=selected)
    await callback.message.edit_reply_markup(reply_markup=build_subcat_keyboard(category, lang, selected))
    await callback.answer()


@sellbuy_router.callback_query(SellFSM.subcategory, F.data == 'sb_sub_done')
async def subcategory_done(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    data = await state.get_data()
    selected = list(data.get('subcats', []))
    if not selected:
        await callback.answer(t('subcat_min', lang), show_alert=True)
        return

    await callback.answer()
    await callback.message.edit_text(
        breadcrumbs(lang, 'name') + "\n\n" + t('ad_title', lang),
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.name)

@sellbuy_router.message(SellFSM.name)
async def get_name(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)

    if message.text == t('menu_button', lang):
        await state.clear()
        await show_menu_prompt(message.chat.id, message.bot, lang)
        return

    if not message.text:
        await message.answer(t('ad_title', lang), parse_mode="HTML")
        return

    if len(message.text) > MAX_NAME_LEN:
        await message.answer(t('name_too_long', lang).format(max=MAX_NAME_LEN), parse_mode="HTML")
        return

    await state.update_data(name=message.text)
    await message.answer(breadcrumbs(lang, 'desc') + "\n\n" + t('ad_desc', lang), parse_mode="HTML")
    await state.set_state(SellFSM.desc)

@sellbuy_router.message(SellFSM.desc)
async def get_desc(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)

    if message.text == t('menu_button', lang):
        await state.clear()
        await show_menu_prompt(message.chat.id, message.bot, lang)
        return

    if not message.text:
        await message.answer(t('ad_desc', lang), parse_mode="HTML")
        return

    if len(message.text) > MAX_DESC_LEN:
        await message.answer(t('desc_too_long', lang).format(max=MAX_DESC_LEN), parse_mode="HTML")
        return

    await state.update_data(desc=message.text)
    neg_kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t('btn_negotiable', lang), callback_data="sb_price_neg")
    ]])
    await message.answer(
        breadcrumbs(lang, 'price') + "\n\n" + t('ad_price', lang),
        reply_markup=neg_kb,
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.price)

@sellbuy_router.message(SellFSM.price)
async def get_price(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)

    if message.text == t('menu_button', lang):
        await state.clear()
        await show_menu_prompt(message.chat.id, message.bot, lang)
        return

    if not message.text:
        return

    # «Договорная» текстом — сразу к фото, минуя выбор валюты.
    if message.text.strip().lower() in NEGOTIABLE_WORDS:
        await state.update_data(price=str(NEGOTIABLE_PRICE), currency='KGS', photos=[])
        await ask_photos(message, state, lang)
        return

    price_text = message.text.replace(" ", "")
    if not price_text.isdigit():
        await message.answer(t('price_must_be_number', lang), parse_mode="HTML")
        return
    if int(price_text) > MAX_PRICE:
        max_str = f"{MAX_PRICE:,}".replace(",", " ")
        await message.answer(t('price_too_large', lang).format(max=max_str), parse_mode="HTML")
        return
    await state.update_data(price=price_text, photos=[])

    data = await state.get_data()
    currencies = get_currencies(data.get('category'))
    if len(currencies) == 1:
        await state.update_data(currency=currencies[0])
        await ask_photos(message, state, lang)
    else:
        rows = [[InlineKeyboardButton(text=cur, callback_data=f"sb_cur_{cur}")] for cur in currencies]
        await message.answer(
            breadcrumbs(lang, 'price') + "\n\n" + t('choose_currency', lang),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
            parse_mode="HTML"
        )
        await state.set_state(SellFSM.currency)


@sellbuy_router.callback_query(SellFSM.price, F.data == 'sb_price_neg')
async def price_negotiable(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    await callback.answer()
    # Договорная цена — валюта не нужна, идём сразу к фото.
    await state.update_data(price=str(NEGOTIABLE_PRICE), currency='KGS', photos=[])
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await ask_photos(callback.message, state, lang)


@sellbuy_router.callback_query(SellFSM.currency, F.data.startswith('sb_cur_'))
async def choose_currency(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    await callback.answer()
    currency = callback.data.removeprefix('sb_cur_')
    await state.update_data(currency=currency)
    await callback.message.delete()
    await ask_photos(callback.message, state, lang)

@sellbuy_router.message(SellFSM.photos)
async def get_photos(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)

    if message.text == t('menu_button', lang):
        await state.clear()
        await show_menu_prompt(message.chat.id, message.bot, lang)
        return

    data = await state.get_data()
    photos = data.get("photos", []) or []

    if message.photo:
        if len(photos) >= 10:
            await message.answer(t('max_10_photos', lang), parse_mode="HTML")
            return
        file_id = message.photo[-1].file_id
        photos.append(file_id)
        await state.update_data(photos=photos)

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=t('done_button', lang))], [KeyboardButton(text=t('menu_button', lang))]],
            resize_keyboard=True
        )
        await message.answer(
            t('photo_added', lang).format(n=len(photos)),
            reply_markup=kb,
            parse_mode="HTML"
        )
        return

    if message.text and message.text.lower() in [t('done_button', lang).lower(), "готово", "done"]:
        if not photos:
            await message.answer(t('add_at_least_one_photo', lang), parse_mode="HTML")
            return

        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=t('show_phone_yes', lang), callback_data="sb_show_phone_yes"),
            InlineKeyboardButton(text=t('show_phone_no', lang), callback_data="sb_show_phone_no")
        ]])
        await message.answer("📸✅", reply_markup=get_main_menu_keyboard(lang))
        await message.answer(
            breadcrumbs(lang, 'phone') + "\n\n" + t('show_phone', lang),
            reply_markup=kb,
            parse_mode="HTML"
        )
        await state.set_state(SellFSM.show_phone)
        return

    await message.answer(t('send_photo_or_done', lang), parse_mode="HTML")

@sellbuy_router.callback_query(F.data.in_(['sb_show_phone_yes', 'sb_show_phone_no']))
async def choose_phone_visibility(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

    if callback.message.text == t('menu_button', lang):
        await state.clear()
        await show_menu_prompt(callback.from_user.id, callback.bot, lang)
        return

    await callback.answer()
    await callback.message.delete()
    show_phone = callback.data == 'sb_show_phone_yes'
    await state.update_data(show_phone=show_phone)

    data = await state.get_data()
    category = data.get('category')
    status_key = data.get('status_key', '')
    subcats = data.get('subcats', [])
    name = data.get('name', '')
    desc = data.get('desc', '')
    price = data.get('price', '')
    currency = data.get('currency', 'KGS')
    photos = data.get('photos', []) or []

    # Превью — на языке пользователя.
    status = get_status_label(category, status_key, lang)
    hashtags = ' '.join(f'#{s}' for s in subcats)
    phone_text = (
        f"📱 {t('phone', lang)}: {client.phone if client and client.phone else t('not_specified', lang)}"
        if show_phone else
        f"📱 {t('phone', lang)}: {t('hidden', lang)}"
    )

    text = (
        f'<b>{hashtags}</b>\n'
        f'<b>{client.name} | {client.tg_code}</b>\n'
        f"<b>{status}</b>\n"
        f"🏷️ <b>{name}</b>\n\n"
        f"{desc}\n\n"
        f"💵 {t('price', lang)}: {format_price(price, currency, lang)}\n"
        f"{phone_text}\n"
        f"✉️ <a href='tg://user?id={callback.from_user.id}'>{t('contact', lang)}</a>"
    )

    if photos:
        try:
            media = [InputMediaPhoto(media=pid) for pid in photos]
            media[0].caption = text
            media[0].parse_mode = "HTML"
            await callback.message.answer_media_group(media)
        except Exception:
            await callback.message.answer(text, parse_mode="HTML")
    else:
        await callback.message.answer(text, parse_mode="HTML")

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t('publish', lang), callback_data="sb_confirm_send"),
        InlineKeyboardButton(text=t('cancel', lang), callback_data="sb_confirm_cancel")
    ]])
    await callback.message.answer(t('ad_preview', lang), reply_markup=kb, parse_mode="HTML")
    await state.set_state(SellFSM.confirm)

@sellbuy_router.callback_query(SellFSM.confirm, F.data.in_(['sb_confirm_send', 'sb_confirm_cancel']))
async def publish_or_cancel(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

    if callback.data == 'sb_confirm_cancel':
        await callback.message.edit_text(t('cancel', lang))
        await state.clear()
        await show_menu_prompt(callback.from_user.id, callback.bot, lang)
        await callback.answer()
        return

    uid = callback.from_user.id
    if uid in _publishing:
        await callback.answer(t('publish_in_progress', lang), show_alert=True)
        return
    _publishing.add(uid)
    try:
        if not client:
            await send_not_registered(callback)
            await state.clear()
            return

        await callback.answer(t('sending_ad', lang))
        data = await state.get_data()
        chan_info = CHANNELS.get(data.get('category'))
        if not chan_info:
            await callback.message.answer(t('channel_not_found', lang))
            await state.clear()
            await show_menu_prompt(uid, callback.bot, lang)
            return

        category = data.get('category')
        status_key = data.get('status_key', '')
        subcats = data.get('subcats', [])
        name = data.get('name', '')
        desc = data.get('desc', '')
        price = data.get('price', '')
        currency = data.get('currency', 'KGS')
        photos = data.get('photos', []) or []
        show_phone = data.get('show_phone', False)

        status_ru = get_status_label(category, status_key, 'ru')
        subcategory = ' '.join(subcats)
        hashtags = ' '.join(f'#{s}' for s in subcats)
        phone_text_russian = (
            f"📱 Телефон: {client.phone if client.phone else 'Не указан'}"
            if show_phone else
            "📱 Телефон: Скрыт"
        )
        owner = f"{client.name} | {client.tg_code}"
        price_text = format_price(price, currency, 'ru')

        created_ad = None
        try:
            async with async_session_maker() as session:
                client_db = await SellBuyService(session).get_client_by_tg(uid)
                client_id = client_db.id
                created_ad = await ProfileService(session).create_ad(
                    client_id=client_id,
                    category_slug=data.get('category_slug', ''),
                    subcategory_slug=subcategory,
                    name=name,
                    description=desc,
                    status_label=status_ru,
                    show_phone=show_phone,
                    price=int(price),
                    currency=currency,
                    channel_id=chan_info['id'],
                    message_id=0,
                    full_message_ids=[],
                )
                ad_id = created_ad.id

            caption = build_channel_caption(
                hashtags, owner, status_ru, name, desc, price_text,
                phone_text_russian, uid, fav_ad_id=ad_id
            )

            if photos:
                sent_messages = await callback.bot.send_media_group(chan_info['id'], [
                    InputMediaPhoto(media=pid, caption=caption if i == 0 else "", parse_mode="HTML")
                    for i, pid in enumerate(photos)
                ])
                full_message_ids = [msg.message_id for msg in sent_messages]
                message_id = full_message_ids[0]
            else:
                sent_message = await callback.bot.send_message(chan_info['id'], caption, parse_mode="HTML")
                message_id = sent_message.message_id
                full_message_ids = [message_id]

            async with async_session_maker() as session:
                await ProfileService(session).update_ad(
                    ad_id, message_id=message_id, full_message_ids=full_message_ids
                )
                await SellBuyService(session).set_next_ability(
                    client_id, chan_info["cooldown_field"], days=get_cooldown_days(category)
                )

            channel_link = chan_info['link']
            if '/t.me/' in channel_link:
                username = channel_link.split('/t.me/')[-1].split('/')[0]
                message_link = f"https://t.me/{username}/{message_id}"
            else:
                message_link = chan_info['link']

            await state.clear()
            await callback.message.edit_text(
                t('ad_published', lang),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=t('see_in_channel', lang), url=message_link)]
                ]),
                parse_mode="HTML"
            )
            await show_menu_prompt(uid, callback.bot, lang)

        except Exception as e:
            logger.error(f"Error publishing ad: {e}")
            if created_ad is not None:
                try:
                    async with async_session_maker() as session:
                        await ProfileService(session).delete_ad(created_ad.id)
                except Exception as del_err:
                    logger.error(f"Rollback failed for ad {created_ad.id}: {del_err}")
            await callback.message.answer(t('publish_error', lang).format(error=str(e)))
            await state.clear()
            await show_menu_prompt(uid, callback.bot, lang)
    finally:
        _publishing.discard(uid)