import asyncio
import logging
from html import escape
from math import ceil
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta, timezone

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    KeyboardButtonRequestUsers, FSInputFile
)

from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.database.session import scheduler
from bot.services.profile_service import ProfileService
from bot.services.sellbuy_service import SellBuyService
from bot.services.payment_service import PaymentService
from bot.channels import (
    ADMIN_ID,
    get_category_label,
    get_subcategory_label,
    get_subcategory_keys,
    get_status_keys,
    get_status_label,
    get_message_link,
    get_favorite_link,
    get_pin_price,
    get_placement_price,
    category_by_channel_id,
    get_cooldown_name,
    get_cooldown_days,
    PIN_DURATION_DAYS,
    SUBSCRIPTION_PRICE,
    SUBSCRIPTION_DAYS,
    AVAILABLE_CASH_REPLENISH,
)
from bot.handlers.menu_handler import (
    send_not_registered,
    show_menu_prompt,
    get_main_menu_keyboard,
)
from bot.handlers.commands import is_own_contact

TRANSFER_REQUEST_ID = 7

logger = logging.getLogger(__name__)

profile_router = Router()

PER_PAGE = 5
MAX_SUBCATS = 2

# Цена 0 = «Договорная» (см. sellbuy.py — поле price NOT NULL Integer).
NEGOTIABLE_PRICE = 0
NEGOTIABLE_WORDS = {
    'договорная', 'договор', 'келишим', 'келишим баада',
    'negotiable', 'nego', '面议',
}
_DIVIDER = "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈"

# Максимальный возраст чека для авто-приёма по OCR (мин). Старее — уходит админу.
OCR_MAX_DELAY_MIN = 180


async def unpin_message(chat_id, message_id):
    from bot.main import bot
    channel_link = f'https://t.me/c/{str(chat_id)[4:]}'
    message_link = f'{channel_link}/{message_id}'
    try:
        await bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
        await bot.send_message(
            ADMIN_ID,
            f"📌 Сообщение <a href=\"{message_link}\">{message_id}</a> откреплено автоматически.",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    except Exception as e:
        await bot.send_message(
            ADMIN_ID,
            (
                f"Ошибка при откреплении сообщения <code>{message_id}</code> в канале "
                f"<a href=\"{channel_link}\">{channel_link}</a>: {str(e)}"
            ),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


class ProfileFSM(StatesGroup):
    edit_ad_name = State()
    edit_ad_price = State()
    edit_ad_desc = State()
    edit_name = State()
    edit_phone = State()
    transfer_user = State()
    transfer_amount = State()
    replenish_receipt = State()


def esc(value) -> str:
    return escape(str(value)) if value is not None else ''


def money(amount, lang: str) -> str:
    return f"{amount} {t('currency', lang)}"


def _group(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def format_price(price, currency, lang: str) -> str:
    """Цена для показа: «Договорная» если price==0, иначе '2 500 KGS'."""
    currency = currency or 'KGS'
    try:
        value = int(price)
    except (TypeError, ValueError):
        value = 0
    if value == NEGOTIABLE_PRICE:
        return t('price_negotiable', lang)
    return f"{_group(value)} {currency}"


def format_price_ru(price, currency) -> str:
    """Русский вариант цены для публикации в канал."""
    currency = currency or 'KGS'
    try:
        value = int(price)
    except (TypeError, ValueError):
        value = 0
    if value == NEGOTIABLE_PRICE:
        return 'Договорная'
    return f"{_group(value)} {currency}"


def _clip(value, n: int) -> str:
    value = str(value)
    return value if len(value) <= n else value[:n - 1] + '…'


def _bishkek(dt: datetime) -> datetime:
    return dt + timedelta(hours=6)


async def _service_client_lang(session, tg_id: int):
    service = ProfileService(session)
    client = await service.get_client_by_tg(tg_id)
    lang = client.language if client and client.language else 'ru'
    return service, client, lang


def _page_slice(items: list, page: int):
    pages = max(1, ceil(len(items) / PER_PAGE))
    page = max(0, min(page, pages - 1))
    start = page * PER_PAGE
    return items[start:start + PER_PAGE], page, pages


def build_ads_table(items: list, lang: str, with_state: bool = False) -> str:
    """Карточный список объявлений (rich message вместо моно-таблицы)."""
    cards = []
    for i, ad in enumerate(items, 1):
        currency = getattr(ad, 'currency', None)
        price = format_price(ad.price, currency, lang)
        head = f"<b>{i}.</b> 🏷️ <b>{esc(_clip(ad.name, 30))}</b>"
        info = f"      💵 <b>{esc(price)}</b>"
        if with_state:
            badge = t('ad_status_active', lang) if ad.status == 'active' else t('ad_status_inactive', lang)
            info += f"\n      {badge}"
        cards.append(head + "\n" + info)
    return f"\n{_DIVIDER}\n".join(cards)


def paginated_kb(items, page, pages, item_prefix, nav_prefix, back_cb, lang,
                 extra_rows=None) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"{i}. {_clip(ad.name, 25)}",
                              callback_data=f"{item_prefix}{ad.id}")]
        for i, ad in enumerate(items, 1)
    ]
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text='◀️', callback_data=f"{nav_prefix}{page - 1}"))
    nav.append(InlineKeyboardButton(
        text=t('page_of', lang).format(current=page + 1, total=pages),
        callback_data='profile_noop'
    ))
    if page < pages - 1:
        nav.append(InlineKeyboardButton(text='▶️', callback_data=f"{nav_prefix}{page + 1}"))
    rows.append(nav)
    if extra_rows:
        rows.extend(extra_rows)
    rows.append([InlineKeyboardButton(text=t('back', lang), callback_data=back_cb)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_profile_text(client, active_ads: int, lang: str) -> str:
    lines = [
        t('profile_title', lang),
        "",
        f"{t('profile_name', lang)}: <b>{esc(client.name) or '—'}</b>",
    ]
    if client.username:
        lines.append(f"🔗 Username: @{esc(client.username)}")
    lines.append(f"{t('profile_phone', lang)}: <code>{esc(client.phone) or '—'}</code>")
    lines.append(f"{t('profile_balance', lang)}: <b>{money(client.balance, lang)}</b>")
    lines.append(f"{t('profile_ads_count', lang)}: <b>{active_ads}</b>")

    sub = client.next_subscription_disable
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if sub and sub.replace(tzinfo=None) > now:
        date_str = _bishkek(sub.replace(tzinfo=None)).strftime('%d.%m.%Y %H:%M')
        lines.append(t('profile_sub_until', lang).format(date=date_str))
    else:
        lines.append(t('profile_sub_none', lang))
    return '\n'.join(lines)


def profile_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t('btn_my_ads', lang), callback_data='profile_ads'),
            InlineKeyboardButton(text=t('btn_favorites', lang), callback_data='profile_favs'),
        ],
        [
            InlineKeyboardButton(text=t('btn_transactions', lang), callback_data='profile_txs'),
            InlineKeyboardButton(text=t('subscription_menu', lang), callback_data='profile_sub'),
        ],
        [
            InlineKeyboardButton(text=t('btn_transfer', lang), callback_data='profile_transfer'),
            InlineKeyboardButton(text=t('btn_replenish', lang), callback_data='profile_replenish'),
        ],
        [
            InlineKeyboardButton(text=t('btn_edit_name', lang), callback_data='profile_edit_name'),
            InlineKeyboardButton(text=t('btn_edit_phone', lang), callback_data='profile_edit_phone'),
        ],
        [InlineKeyboardButton(text=t('back', lang), callback_data='back_to_menu')],
    ])


def ad_card_text(ad, lang: str) -> str:
    status_key = 'ad_status_active' if ad.status == 'active' else 'ad_status_inactive'
    subcat_labels = ', '.join(
        get_subcategory_label(ad.category_slug, s, lang) for s in ad.subcategory_slug.split()
    )
    currency = getattr(ad, 'currency', None) or 'KGS'
    base = t('ad_card', lang).format(
        name=esc(ad.name),
        category=esc(get_category_label(ad.category_slug, lang) or ad.category_slug),
        subcategory=esc(subcat_labels),
        price=format_price(ad.price, currency, lang),
        status=t(status_key, lang),
        date=_bishkek(ad.created_at).strftime('%d.%m.%Y'),
    )
    extra = []
    if ad.description:
        extra.append(f"📝 {t('description', lang)}: {esc(_clip(ad.description, 200))}")
    phone_vis = t('show_phone_yes', lang) if ad.show_phone else t('show_phone_no', lang)
    extra.append(f"📱 {t('phone', lang)}: {phone_vis}")
    return base + "\n" + "\n".join(extra)


def ad_card_kb(ad, lang: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text=t('btn_edit_ad_name', lang), callback_data=f'pad|name|{ad.id}'),
            InlineKeyboardButton(text=t('btn_edit_ad_price', lang), callback_data=f'pad|price|{ad.id}'),
        ],
        [
            InlineKeyboardButton(text=t('btn_edit_ad_status', lang), callback_data=f'pad|status|{ad.id}'),
            InlineKeyboardButton(text=t('btn_edit_ad_subcat', lang), callback_data=f'pad|sub|{ad.id}'),
        ],
        [
            InlineKeyboardButton(text=t('btn_edit_ad_desc', lang), callback_data=f'pad|desc|{ad.id}'),
            InlineKeyboardButton(text=t('btn_edit_ad_phone', lang), callback_data=f'pad|phone|{ad.id}'),
        ],
    ]
    if ad.status == 'active':
        rows.append([
            InlineKeyboardButton(text=t('btn_pin_ad', lang), callback_data=f'pad|pin|{ad.id}'),
            InlineKeyboardButton(text=t('btn_deactivate', lang), callback_data=f'pad|deact|{ad.id}'),
        ])
        rows.append([
            InlineKeyboardButton(text=t('up_ad_button', lang), callback_data=f'up|ad|{ad.id}'),
        ])
    link = get_message_link(ad.channel_id, ad.message_id)
    if link:
        rows.append([InlineKeyboardButton(text=t('see_in_channel', lang), url=link)])
    rows.append([InlineKeyboardButton(text=t('back', lang), callback_data='profile_ads')])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_edit_subcat_kb(category_slug: str, lang: str, selected: list,
                         ad_id: int) -> InlineKeyboardMarkup:
    keys = get_subcategory_keys(category_slug)
    rows = []
    for i in range(0, len(keys), 2):
        row = []
        for key in keys[i:i + 2]:
            mark = '✅ ' if key in selected else ''
            row.append(InlineKeyboardButton(
                text=f"{mark}{get_subcategory_label(category_slug, key, lang)}",
                callback_data=f"pad|subtog|{ad_id}|{key}"
            ))
        rows.append(row)
    rows.append([InlineKeyboardButton(text=t('btn_subcat_done', lang),
                                      callback_data=f"pad|subdone|{ad_id}")])
    rows.append([InlineKeyboardButton(text=t('back', lang),
                                      callback_data=f"pad|open|{ad_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_channel_caption(ad, client, sold: bool = False) -> str:
    owner_line = f"{esc(client.name)} | {client.tg_code}"
    if sold:
        owner_line += " | ❌ПРОДАНО"
    phone_line = (
        f"📱 Телефон: {esc(client.phone)}"
        if ad.show_phone and client.phone else
        "📱 Телефон: Скрыт"
    )
    hashtags = ' '.join(f'#{s}' for s in ad.subcategory_slug.split())
    currency = getattr(ad, 'currency', None) or 'KGS'
    parts = [
        f"<b>{esc(hashtags)}</b>",
        f"<b>{owner_line}</b>",
        f"<b>{esc(ad.status_label)}</b>",
        f"🏷️ <b>{esc(ad.name)}</b>",
        "",
    ]
    if ad.description:
        parts.extend([esc(ad.description), ""])
    parts.extend([
        f"💵 <b>Цена:</b> {esc(format_price_ru(ad.price, currency))}",
        phone_line,
        f"✉️ <a href='tg://user?id={client.tg_code}'>Написать продавцу</a>",
        f"⭐️ <a href='{get_favorite_link(ad.id)}'>Добавить в избранное</a>",
        "📢 <a href='https://t.me/tez4917_bot'>Разместить объявление</a>",
    ])
    return '\n'.join(parts)


async def edit_channel_ad(bot, ad, caption: str) -> bool:
    try:
        await bot.edit_message_caption(
            chat_id=ad.channel_id, message_id=ad.message_id,
            caption=caption, parse_mode="HTML"
        )
        return True
    except Exception:
        try:
            await bot.edit_message_text(
                chat_id=ad.channel_id, message_id=ad.message_id,
                text=caption, parse_mode="HTML"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update channel ad {ad.id}: {e}")
            return False


async def show_card(target, ad, lang: str, edit: bool):
    text = ad_card_text(ad, lang)
    kb = ad_card_kb(ad, lang)
    if edit:
        await target.edit_text(text, reply_markup=kb, parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=kb, parse_mode="HTML")


async def apply_ad_change(bot, service, ad_id, client, **fields):
    ad = await service.update_ad(ad_id, **fields)
    updated = await edit_channel_ad(bot, ad, build_channel_caption(ad, client))
    return ad, updated


async def show_profile_message(message: types.Message, tg_id: int):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, tg_id)
        if not client:
            await send_not_registered(message)
            return
        active_ads = await service.count_active_ads(client.id)
    await message.answer(
        build_profile_text(client, active_ads, lang),
        reply_markup=profile_menu_kb(lang),
        parse_mode="HTML"
    )


@profile_router.callback_query(F.data == "profile_noop")
async def noop(callback: types.CallbackQuery):
    await callback.answer()


@profile_router.callback_query(F.data == "check_profile")
async def check_profile(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
        active_ads = await service.count_active_ads(client.id)

    await state.clear()
    text = build_profile_text(client, active_ads, lang)
    kb = profile_menu_kb(lang)
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


async def render_ads_page(callback: types.CallbackQuery, page: int):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
        ads = await service.get_client_ads(client.id)

    if not ads:
        await callback.answer(t('no_ads', lang), show_alert=True)
        return

    chunk, page, pages = _page_slice(ads, page)
    text = t('my_ads_title', lang) + "\n\n" + build_ads_table(chunk, lang)
    kb = paginated_kb(chunk, page, pages, "profile_ad_", "prof_adpg_", "check_profile", lang)
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@profile_router.callback_query(F.data == "profile_ads")
async def my_ads(callback: types.CallbackQuery):
    await render_ads_page(callback, 0)


@profile_router.callback_query(F.data.startswith("prof_adpg_"))
async def my_ads_page(callback: types.CallbackQuery):
    await render_ads_page(callback, int(callback.data.removeprefix("prof_adpg_")))


@profile_router.callback_query(F.data.startswith("profile_ad_"))
async def ad_card(callback: types.CallbackQuery):
    ad_id = int(callback.data.removeprefix("profile_ad_"))
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        ad = await service.get_ad(ad_id)

    if not ad or not client or ad.client_id != client.id:
        await callback.answer(t('ad_not_found', lang), show_alert=True)
        return

    await show_card(callback.message, ad, lang, edit=True)
    await callback.answer()


@profile_router.callback_query(F.data.startswith("pad|"))
async def ad_action(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split("|")
    action = parts[1]
    ad_id = int(parts[2])

    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        ad = await service.get_ad(ad_id)
        if not ad or not client or ad.client_id != client.id:
            await callback.answer(t('ad_not_found', lang), show_alert=True)
            return

        if action == "open":
            await show_card(callback.message, ad, lang, edit=True)

        elif action == "name":
            await state.set_state(ProfileFSM.edit_ad_name)
            await state.update_data(ad_id=ad_id)
            await callback.message.answer(t('enter_new_ad_name', lang), parse_mode="HTML")

        elif action == "price":
            await state.set_state(ProfileFSM.edit_ad_price)
            await state.update_data(ad_id=ad_id)
            neg_kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=t('btn_negotiable', lang), callback_data=f'pad|priceneg|{ad_id}')
            ]])
            await callback.message.answer(t('enter_new_ad_price', lang), reply_markup=neg_kb, parse_mode="HTML")

        elif action == "priceneg":
            ad, updated = await apply_ad_change(callback.bot, service, ad_id, client, price=NEGOTIABLE_PRICE)
            await state.clear()
            await callback.answer(t('ad_updated', lang) if updated else t('channel_update_failed', lang))
            await show_card(callback.message, ad, lang, edit=True)

        elif action == "desc":
            await state.set_state(ProfileFSM.edit_ad_desc)
            await state.update_data(ad_id=ad_id)
            await callback.message.answer(t('enter_new_ad_desc', lang), parse_mode="HTML")

        elif action == "status":
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=get_status_label(ad.category_slug, key, lang),
                                      callback_data=f"pad|setstatus|{ad_id}|{key}")]
                for key in get_status_keys(ad.category_slug)
            ] + [[InlineKeyboardButton(text=t('back', lang), callback_data=f"pad|open|{ad_id}")]])
            await callback.message.edit_text(t('choose_ad_status', lang), reply_markup=kb, parse_mode="HTML")

        elif action == "setstatus":
            label = get_status_label(ad.category_slug, parts[3], lang)
            ad, updated = await apply_ad_change(callback.bot, service, ad_id, client, status_label=label)
            await callback.answer(t('ad_updated', lang) if updated else t('channel_update_failed', lang))
            await show_card(callback.message, ad, lang, edit=True)

        elif action == "sub":
            selected = ad.subcategory_slug.split()
            await state.update_data(edit_sub_ad_id=ad_id, edit_subcats=selected)
            await callback.message.edit_text(
                t('choose_subcategories', lang),
                reply_markup=build_edit_subcat_kb(ad.category_slug, lang, selected, ad_id),
                parse_mode="HTML"
            )

        elif action == "subtog":
            data = await state.get_data()
            selected = list(data.get('edit_subcats', []))
            key = parts[3]
            if key in selected:
                selected.remove(key)
            elif len(selected) >= MAX_SUBCATS:
                await callback.answer(t('subcat_max', lang).format(n=MAX_SUBCATS), show_alert=True)
                return
            else:
                selected.append(key)
            await state.update_data(edit_subcats=selected)
            await callback.message.edit_reply_markup(
                reply_markup=build_edit_subcat_kb(ad.category_slug, lang, selected, ad_id)
            )
            await callback.answer()

        elif action == "subdone":
            data = await state.get_data()
            selected = list(data.get('edit_subcats', []))
            if not selected:
                await callback.answer(t('subcat_min', lang), show_alert=True)
                return
            ad, updated = await apply_ad_change(
                callback.bot, service, ad_id, client, subcategory_slug=' '.join(selected)
            )
            await state.update_data(edit_subcats=[], edit_sub_ad_id=None)
            await callback.answer(t('ad_updated', lang) if updated else t('channel_update_failed', lang))
            await show_card(callback.message, ad, lang, edit=True)

        elif action == "phone":
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text=t('show_phone_yes', lang), callback_data=f"pad|setphone|{ad_id}|1"),
                    InlineKeyboardButton(text=t('show_phone_no', lang), callback_data=f"pad|setphone|{ad_id}|0"),
                ],
                [InlineKeyboardButton(text=t('back', lang), callback_data=f"pad|open|{ad_id}")],
            ])
            await callback.message.edit_text(t('choose_phone_visibility', lang), reply_markup=kb, parse_mode="HTML")

        elif action == "setphone":
            ad, updated = await apply_ad_change(callback.bot, service, ad_id, client, show_phone=parts[3] == "1")
            await callback.answer(t('ad_updated', lang) if updated else t('channel_update_failed', lang))
            await show_card(callback.message, ad, lang, edit=True)

        elif action == "deact":
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=t('btn_confirm_yes', lang), callback_data=f"pad|deactyes|{ad_id}"),
                InlineKeyboardButton(text=t('btn_confirm_no', lang), callback_data=f"pad|open|{ad_id}"),
            ]])
            await callback.message.edit_text(t('deactivate_confirm', lang), reply_markup=kb, parse_mode="HTML")

        elif action == "deactyes":
            await service.deactivate_ad(ad_id)
            ad = await service.get_ad(ad_id)
            updated = await edit_channel_ad(callback.bot, ad, build_channel_caption(ad, client, sold=True))
            await callback.answer(t('ad_deactivated', lang) if updated else t('channel_update_failed', lang), show_alert=True)
            await show_card(callback.message, ad, lang, edit=True)

        elif action == "pin":
            price = get_pin_price(ad.category_slug)
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text=t('btn_confirm_yes', lang), callback_data=f"pad|pinyes|{ad_id}"),
                InlineKeyboardButton(text=t('btn_confirm_no', lang), callback_data=f"pad|open|{ad_id}"),
            ]])
            await callback.message.edit_text(
                t('pin_offer', lang).format(
                    days=PIN_DURATION_DAYS,
                    price=money(price, lang),
                    balance=money(client.balance, lang)
                ),
                reply_markup=kb, parse_mode="HTML"
            )

        elif action == "pinyes":
            price = get_pin_price(ad.category_slug)
            if not await service.try_charge(client.id, price):
                await callback.answer(
                    t('pin_low_balance', lang).format(
                        price=money(price, lang),
                        balance=money(client.balance, lang)
                    ),
                    show_alert=True
                )
                return
            try:
                await callback.bot.pin_chat_message(chat_id=ad.channel_id, message_id=ad.message_id)
                run_date = datetime.now() + timedelta(days=PIN_DURATION_DAYS)
                scheduler.add_job(unpin_message, "date", run_date=run_date,
                                  args=[ad.channel_id, ad.message_id])
                await callback.answer(t('pin_paid', lang).format(days=PIN_DURATION_DAYS), show_alert=True)
            except Exception as e:
                logger.error(f"Pin failed for ad {ad_id}: {e}")
                await service.add_balance(client.id, price)
                await callback.answer(t('pin_failed', lang), show_alert=True)
            await show_card(callback.message, ad, lang, edit=True)


async def _finish_text_edit(message, state, field_value_key, value):
    data = await state.get_data()
    ad_id = data.get('ad_id')
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, message.from_user.id)
        ad = await service.get_ad(ad_id)
        if not ad or not client or ad.client_id != client.id:
            await message.answer(t('ad_not_found', lang))
            await state.clear()
            return
        ad, updated = await apply_ad_change(
            message.bot, service, ad_id, client, **{field_value_key: value}
        )
    await state.clear()
    await message.answer(t('ad_updated', lang) if updated else t('channel_update_failed', lang), parse_mode="HTML")
    await show_card(message, ad, lang, edit=False)


@profile_router.message(ProfileFSM.edit_ad_name, F.text)
async def set_new_ad_name(message: types.Message, state: FSMContext):
    await _finish_text_edit(message, state, 'name', message.text.strip())


@profile_router.message(ProfileFSM.edit_ad_desc, F.text)
async def set_new_ad_desc(message: types.Message, state: FSMContext):
    await _finish_text_edit(message, state, 'description', message.text.strip())


@profile_router.message(ProfileFSM.edit_ad_price, F.text)
async def set_new_ad_price(message: types.Message, state: FSMContext):
    if message.text.strip().lower() in NEGOTIABLE_WORDS:
        await _finish_text_edit(message, state, 'price', NEGOTIABLE_PRICE)
        return
    price_text = message.text.replace(" ", "")
    if not price_text.isdigit():
        async with async_session_maker() as session:
            lang = await ProfileService(session).get_user_lang(message.from_user.id)
        await message.answer(t('price_must_be_number', lang), parse_mode="HTML")
        return
    await _finish_text_edit(message, state, 'price', int(price_text))


async def render_favs_page(callback: types.CallbackQuery, page: int):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
        favs = await service.get_favorites(client.id)

    if not favs:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t('back', lang), callback_data='check_profile')]
        ])
        await callback.message.edit_text(t('no_favorites', lang), reply_markup=kb, parse_mode="HTML")
        await callback.answer()
        return

    chunk, page, pages = _page_slice(favs, page)
    text = t('favorites_title', lang) + "\n\n" + build_ads_table(chunk, lang, with_state=True)
    kb = paginated_kb(chunk, page, pages, "profile_fav_", "prof_favpg_", "check_profile", lang)
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@profile_router.callback_query(F.data == "profile_favs")
async def favorites(callback: types.CallbackQuery):
    await render_favs_page(callback, 0)


@profile_router.callback_query(F.data.startswith("prof_favpg_"))
async def favorites_page(callback: types.CallbackQuery):
    await render_favs_page(callback, int(callback.data.removeprefix("prof_favpg_")))


@profile_router.callback_query(F.data.startswith("profile_fav_"))
async def favorite_card(callback: types.CallbackQuery):
    ad_id = int(callback.data.removeprefix("profile_fav_"))
    async with async_session_maker() as session:
        service, _, lang = await _service_client_lang(session, callback.from_user.id)
        ad = await service.get_ad(ad_id)

    if not ad:
        await callback.answer(t('ad_not_found', lang), show_alert=True)
        return

    status = t('ad_status_active', lang) if ad.status == 'active' else t('ad_status_inactive', lang)
    text = ad_card_text(ad, lang) + f"\n\n{status}"

    rows = []
    link = get_message_link(ad.channel_id, ad.message_id)
    if link:
        rows.append([InlineKeyboardButton(text=t('see_in_channel', lang), url=link)])
    rows.append([InlineKeyboardButton(text=t('btn_remove_favorite', lang), callback_data=f'profile_favdel_{ad.id}')])
    rows.append([InlineKeyboardButton(text=t('back', lang), callback_data='profile_favs')])

    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=rows), parse_mode="HTML")
    await callback.answer()


@profile_router.callback_query(F.data.startswith("profile_favdel_"))
async def remove_favorite(callback: types.CallbackQuery):
    ad_id = int(callback.data.removeprefix("profile_favdel_"))
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        if client:
            await service.remove_favorite(client.id, ad_id)
    await callback.answer(t('favorite_removed', lang), show_alert=True)
    await render_favs_page(callback, 0)


def build_tx_table(items, client_id: int, lang: str) -> str:
    """Карточный список транзакций (rich message вместо моно-таблицы)."""
    cards = []
    for i, tx in enumerate(items, 1):
        if tx.sender_id == client_id:
            icon = "📤"
            amount = f"−{money(tx.amount, lang)}"
            party = f"{t('tx_to', lang)} <b>{esc(_clip(tx.receiver.name if tx.receiver else '—', 22))}</b>"
        else:
            icon = "📥"
            amount = f"+{money(tx.amount, lang)}"
            party = f"{t('tx_from', lang)} <b>{esc(_clip(tx.sender.name if tx.sender else '—', 22))}</b>"
        head = f"<b>{i}.</b> {icon} <b>{esc(amount)}</b>"
        info = f"      👤 {party}"
        cards.append(head + "\n" + info)
    return f"\n{_DIVIDER}\n".join(cards)


def nav_only_kb(page, pages, nav_prefix, back_cb, lang) -> InlineKeyboardMarkup:
    rows = []
    if pages > 1:
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton(text='◀️', callback_data=f"{nav_prefix}{page - 1}"))
        nav.append(InlineKeyboardButton(
            text=t('page_of', lang).format(current=page + 1, total=pages),
            callback_data='profile_noop'
        ))
        if page < pages - 1:
            nav.append(InlineKeyboardButton(text='▶️', callback_data=f"{nav_prefix}{page + 1}"))
        rows.append(nav)
    rows.append([InlineKeyboardButton(text=t('back', lang), callback_data=back_cb)])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def render_txs_page(callback: types.CallbackQuery, page: int):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
        client_id = client.id
        txs = await service.get_transactions(client_id, limit=200)

    if not txs:
        await callback.answer(t('no_transactions', lang), show_alert=True)
        return

    chunk, page, pages = _page_slice(txs, page)
    text = t('transactions_title', lang) + "\n\n" + build_tx_table(chunk, client_id, lang)
    kb = nav_only_kb(page, pages, "prof_txpg_", "check_profile", lang)
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@profile_router.callback_query(F.data == "profile_txs")
async def transactions(callback: types.CallbackQuery):
    await render_txs_page(callback, 0)


@profile_router.callback_query(F.data.startswith("prof_txpg_"))
async def transactions_page(callback: types.CallbackQuery):
    await render_txs_page(callback, int(callback.data.removeprefix("prof_txpg_")))


@profile_router.callback_query(F.data == "profile_sub")
async def subscription_offer(callback: types.CallbackQuery):
    async with async_session_maker() as session:
        _, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t('btn_sub_from_balance', lang), callback_data='profile_subpay')],
        [InlineKeyboardButton(text=t('back', lang), callback_data='check_profile')],
    ])
    await callback.message.edit_text(
        t('sub_offer', lang).format(
            days=SUBSCRIPTION_DAYS,
            price=money(SUBSCRIPTION_PRICE, lang),
            balance=money(client.balance, lang)
        ),
        reply_markup=kb, parse_mode="HTML"
    )
    await callback.answer()


@profile_router.callback_query(F.data == "profile_subpay")
async def subscription_confirm(callback: types.CallbackQuery):
    async with async_session_maker() as session:
        _, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t('btn_confirm_yes', lang), callback_data='profile_subpay_yes'),
        InlineKeyboardButton(text=t('btn_confirm_no', lang), callback_data='profile_sub'),
    ]])
    await callback.message.edit_text(
        t('sub_confirm_charge', lang).format(
            price=money(SUBSCRIPTION_PRICE, lang),
            balance=money(client.balance, lang)
        ),
        reply_markup=kb, parse_mode="HTML"
    )
    await callback.answer()


@profile_router.callback_query(F.data == "profile_subpay_yes")
async def subscription_pay_balance(callback: types.CallbackQuery):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
        if not await service.try_charge(client.id, SUBSCRIPTION_PRICE):
            await callback.answer(
                t('sub_low_balance', lang).format(
                    price=money(SUBSCRIPTION_PRICE, lang),
                    balance=money(client.balance, lang)
                ),
                show_alert=True
            )
            return
        await service.extend_subscription(client.id, SUBSCRIPTION_DAYS)
        active_ads = await service.count_active_ads(client.id)
        client = await service.get_client_by_tg(callback.from_user.id)

    await callback.answer(t('sub_paid', lang).format(days=SUBSCRIPTION_DAYS), show_alert=True)
    await callback.message.edit_text(
        build_profile_text(client, active_ads, lang),
        reply_markup=profile_menu_kb(lang),
        parse_mode="HTML"
    )


@profile_router.callback_query(F.data == "profile_edit_name")
async def ask_new_name(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        lang = await ProfileService(session).get_user_lang(callback.from_user.id)
    await state.set_state(ProfileFSM.edit_name)
    await callback.message.answer(t('enter_new_name', lang), parse_mode="HTML")
    await callback.answer()


@profile_router.message(ProfileFSM.edit_name, F.text)
async def set_new_name(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, message.from_user.id)
        if not client:
            await send_not_registered(message)
            await state.clear()
            return
        await service.update_client_name(message.from_user.id, message.text.strip())
    await state.clear()
    await message.answer(t('name_updated', lang), parse_mode="HTML")
    await show_profile_message(message, message.from_user.id)


@profile_router.callback_query(F.data == "profile_edit_phone")
async def ask_new_phone(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        lang = await ProfileService(session).get_user_lang(callback.from_user.id)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t('send_phone_btn', lang), request_contact=True)],
            [KeyboardButton(text=t('menu_button', lang))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(ProfileFSM.edit_phone)
    await callback.message.answer(f"📱 {t('registration_phone', lang)}", reply_markup=kb)
    await callback.answer()


@profile_router.message(ProfileFSM.edit_phone)
async def set_new_phone(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, message.from_user.id)
        if not client:
            await send_not_registered(message)
            await state.clear()
            return

        if not message.contact:
            await state.clear()
            await message.answer(
                t('phone_need_contact', lang),
                reply_markup=get_main_menu_keyboard(lang),
                parse_mode="HTML"
            )
            return

        if not is_own_contact(message):
            await message.answer(t('phone_not_yours', lang), parse_mode="HTML")
            return

        await service.update_client_phone(message.from_user.id, message.contact.phone_number)

    await state.clear()
    await message.answer(t('phone_updated', lang), reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
    await show_menu_prompt(message.chat.id, message.bot, lang)
    await show_profile_message(message, message.from_user.id)


@profile_router.callback_query(F.data == "profile_transfer")
async def start_transfer(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        _, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text=t('btn_choose_user', lang),
                request_users=KeyboardButtonRequestUsers(request_id=TRANSFER_REQUEST_ID, max_quantity=1)
            )],
            [KeyboardButton(text=t('menu_button', lang))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(ProfileFSM.transfer_user)
    await callback.message.answer(t('transfer_choose_user', lang), reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@profile_router.message(ProfileFSM.transfer_user, F.users_shared)
async def transfer_user_selected(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, message.from_user.id)
        if not client:
            await send_not_registered(message)
            await state.clear()
            return

        user_ids = message.users_shared.user_ids if message.users_shared else []
        if not user_ids:
            await message.answer(t('transfer_pick_user_hint', lang), parse_mode="HTML")
            return

        target_id = user_ids[0]
        if target_id == message.from_user.id:
            await state.clear()
            await message.answer(t('transfer_self', lang), reply_markup=get_main_menu_keyboard(lang), parse_mode="HTML")
            await show_profile_message(message, message.from_user.id)
            return

        receiver = await service.get_client_by_tg(target_id)
        if not receiver:
            await state.clear()
            await message.answer(t('transfer_user_not_found', lang), reply_markup=get_main_menu_keyboard(lang), parse_mode="HTML")
            await show_profile_message(message, message.from_user.id)
            return
        receiver_name = receiver.name or str(target_id)

    await state.update_data(receiver_tg=target_id, receiver_name=receiver_name)
    await state.set_state(ProfileFSM.transfer_amount)
    await message.answer(
        t('transfer_enter_amount', lang).format(name=esc(receiver_name)),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML"
    )


@profile_router.message(ProfileFSM.transfer_user)
async def transfer_user_hint(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        lang = await ProfileService(session).get_user_lang(message.from_user.id)
    await message.answer(t('transfer_pick_user_hint', lang), parse_mode="HTML")


@profile_router.message(ProfileFSM.transfer_amount, F.text)
async def transfer_amount_entered(message: types.Message, state: FSMContext):
    data = await state.get_data()
    receiver_tg = data.get('receiver_tg')
    receiver_name = data.get('receiver_name', '')

    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, message.from_user.id)
        if not client:
            await send_not_registered(message)
            await state.clear()
            return

        try:
            amount = Decimal(message.text.replace(',', '.').strip())
        except (InvalidOperation, AttributeError):
            await message.answer(t('transfer_amount_invalid', lang), parse_mode="HTML")
            return
        if amount <= 0:
            await message.answer(t('transfer_amount_invalid', lang), parse_mode="HTML")
            return

        try:
            result = await SellBuyService(session).send_teziks(message.from_user.id, receiver_tg, amount)
        except ValueError:
            await message.answer(
                t('transfer_insufficient', lang).format(balance=money(client.balance, lang)),
                parse_mode="HTML"
            )
            return
        sender, receiver = result['sender'], result['receiver']
        sender_balance, receiver_balance = sender.balance, receiver.balance
        receiver_tg_code, receiver_lang = receiver.tg_code, receiver.language or 'ru'
        sender_name = sender.name or str(message.from_user.id)

    await state.clear()
    await message.answer(
        t('transfer_done', lang).format(
            amount=money(amount, lang),
            name=esc(receiver_name),
            balance=money(sender_balance, lang)
        ),
        parse_mode="HTML"
    )
    try:
        await message.bot.send_message(
            int(receiver_tg_code),
            t('transfer_received', receiver_lang).format(
                amount=money(amount, receiver_lang),
                name=esc(sender_name),
                balance=money(receiver_balance, receiver_lang)
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Transfer notify failed: {e}")
    await show_profile_message(message, message.from_user.id)


def replenish_amount_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=money(amount, lang), callback_data=f"repl_amt_{amount}")]
        for amount in AVAILABLE_CASH_REPLENISH
    ]
    rows.append([InlineKeyboardButton(text=t('back', lang), callback_data='check_profile')])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@profile_router.callback_query(F.data == "profile_replenish")
async def start_replenish(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        _, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
    await state.clear()
    text = t('replenish_choose', lang)
    await callback.message.edit_text(text, reply_markup=replenish_amount_kb(lang), parse_mode="HTML")
    await callback.answer()


@profile_router.callback_query(F.data.startswith("repl_amt_"))
async def replenish_amount_chosen(callback: types.CallbackQuery, state: FSMContext):
    amount = int(callback.data.removeprefix("repl_amt_"))
    async with async_session_maker() as session:
        _, client, lang = await _service_client_lang(session, callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            await callback.answer()
            return
    await state.set_state(ProfileFSM.replenish_receipt)
    await state.update_data(replenish_amount=amount)
    qr_path = Path(__file__).resolve().parent.parent / "assets" / f"mbank_qr_{amount}.jpg"
    await callback.message.answer_photo(
        FSInputFile(qr_path),
        caption=t('replenish_instruction', lang).format(amount=money(amount, lang))
        + "\n\n" + t('replenish_warning', lang),
        parse_mode="HTML"
    )
    await callback.answer()


async def _try_ocr_receipt(message: types.Message, amount) -> "object | None":
    """Скачивает чек в память и прогоняет OCR в отдельном потоке.
    Фото на диск не пишется. Возвращает TopupResult или None при ошибке."""
    try:
        from bot.services.receipt_ocr import verify_topup_bytes
    except Exception as e:
        logger.error(f"OCR module unavailable: {e}")
        return None

    img_bytes = None
    try:
        buf = await message.bot.download(message.photo[-1])
        img_bytes = buf.read()
    except Exception as e:
        logger.error(f"Receipt download failed: {e}")
        return None

    bishkek_now = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=6)
    try:
        return await asyncio.to_thread(
            verify_topup_bytes, img_bytes, float(amount), bishkek_now, OCR_MAX_DELAY_MIN
        )
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return None
    finally:
        img_bytes = None  # освобождаем буфер сразу


@profile_router.message(ProfileFSM.replenish_receipt, F.photo)
async def replenish_receipt(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('receipt_sent'):
        return
    amount = data.get('replenish_amount')

    async with async_session_maker() as session:
        lang = await ProfileService(session).get_user_lang(message.from_user.id)

    ocr = await _try_ocr_receipt(message, amount)

    auto_done = False
    admin_note = ""
    if ocr is not None and ocr.ok:
        async with async_session_maker() as session:
            psvc = PaymentService(session)
            if await psvc.transaction_exists(ocr.transaction_id or ''):
                admin_note = "\n⚠️ Возможный дубликат: такой чек уже принимался."
            else:
                await SellBuyService(session).replenishment_balance(
                    message.from_user.id, Decimal(str(amount))
                )
                cl = await psvc.get_client_by_tg(message.from_user.id)
                await psvc.record_payment(
                    client_id=cl.id if cl else None,
                    tg_code=str(message.from_user.id),
                    username=message.from_user.username or '',
                    amount=Decimal(str(amount)),
                    method='ocr',
                    transaction_id=ocr.transaction_id or '',
                    ocr_confidence=round(ocr.confidence, 1),
                    receipt_datetime=ocr.receipt_datetime,
                )
                auto_done = True

    if auto_done:
        await state.update_data(receipt_sent=True)
        await state.clear()
        await message.answer(
            t('replenish_confirmed', lang).format(amount=money(amount, lang)),
            parse_mode="HTML"
        )
        return

    # --- 2) OCR не уверен / ошибка / дубликат — ручной флоу для админа ---
    if ocr is not None and not admin_note:
        reasons = "; ".join(ocr.reasons[:3]) if ocr.reasons else "не уверен"
        admin_note = f"\n🔎 OCR: {reasons} (conf {ocr.confidence:.0f}%)"
    elif ocr is None and not admin_note:
        admin_note = "\n🔎 OCR: не удалось обработать фото"

    file_id = message.photo[-1].file_id
    user_link = f"tg://user?id={message.from_user.id}"
    caption = (
        f"💳 Новый чек на пополнение\n\n"
        f"👤 <a href=\"{user_link}\">@{message.from_user.username or message.from_user.full_name or message.from_user.id}</a>\n"
        f"🆔 <code>{message.from_user.id}</code>\n"
        f"💰 Сумма: <b>{amount}</b>\n"
        f"📅 {(datetime.now(timezone.utc) + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')}"
        f"{admin_note}"
    )
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"repl_confirm|{message.from_user.id}|{amount}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"repl_decline|{message.from_user.id}"),
        ],
        [InlineKeyboardButton(text="🚫 Бан", callback_data=f"repl_ban|{message.from_user.id}")],
    ])
    try:
        await message.bot.send_photo(
            chat_id=ADMIN_ID, photo=file_id, caption=caption,
            parse_mode="HTML", reply_markup=ikb
        )
        await message.answer(t('replenish_receipt_sent', lang))
        await state.update_data(receipt_sent=True)
        await state.clear()
    except Exception as e:
        await message.answer(t('error_sending_receipt', lang).format(error=str(e)))


@profile_router.callback_query(F.data.startswith("repl_confirm|"))
async def admin_replenish_confirm(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(t('admin_only', 'ru'), show_alert=True)
        return
    try:
        _, user_id, amount = callback.data.split("|", 2)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    async with async_session_maker() as session:
        psvc = PaymentService(session)
        lang_user = await psvc.get_user_lang(int(user_id))
        try:
            client = await SellBuyService(session).replenishment_balance(int(user_id), Decimal(amount))
        except ValueError:
            await callback.answer("Клиент не найден.", show_alert=True)
            return
        await psvc.record_payment(
            client_id=client.id if client else None,
            tg_code=str(user_id),
            username=client.username if client else '',
            amount=Decimal(amount),
            method='admin',
        )

    try:
        await callback.bot.send_message(
            int(user_id),
            t('replenish_confirmed', lang_user).format(amount=money(amount, lang_user)),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Replenish notify failed: {e}")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Пополнение подтверждено.")


@profile_router.callback_query(F.data.startswith("repl_ban|"))
async def admin_replenish_ban(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(t('admin_only', 'ru'), show_alert=True)
        return
    try:
        _, user_id = callback.data.split("|", 1)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    async with async_session_maker() as session:
        try:
            await SellBuyService(session).ban_client(int(user_id))
        except ValueError:
            await callback.answer("Клиент не найден.", show_alert=True)
            return

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(f"Пользователь {user_id} забанен.", show_alert=True)


@profile_router.callback_query(F.data.startswith("repl_decline|"))
async def admin_replenish_decline(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(t('admin_only', 'ru'), show_alert=True)
        return
    try:
        _, user_id = callback.data.split("|", 1)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    async with async_session_maker() as session:
        lang_user = await ProfileService(session).get_user_lang(int(user_id))
    try:
        await callback.bot.send_message(int(user_id), t('replenish_declined', lang_user))
    except Exception as e:
        logger.error(f"Replenish decline notify failed: {e}")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Отклонено.")


def _format_cooldown_wait(next_allowed: datetime, now: datetime, lang: str) -> str:
    total_minutes = int((next_allowed - now).total_seconds() // 60)
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
        parts.append(t('less_than_minute', lang))
    return ' '.join(parts)


def _up_ad_confirm_kb(ad_id: int, lang: str, pay: bool) -> InlineKeyboardMarkup:
    yes_cb = f'up_pay|{ad_id}' if pay else f'up_yes|{ad_id}'
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t('btn_confirm_yes', lang), callback_data=yes_cb),
        InlineKeyboardButton(text=t('btn_confirm_no', lang), callback_data=f'pad|open|{ad_id}'),
    ]])


async def _perform_up_ad(bot, session, service, ad, client) -> None:
    category = category_by_channel_id(ad.channel_id)
    old_message_ids = sorted(ad.full_message_ids)

    copied_messages = await bot.copy_messages(
        chat_id=ad.channel_id,
        from_chat_id=ad.channel_id,
        message_ids=old_message_ids
    )
    new_message_ids = [msg.message_id for msg in copied_messages]

    await service.create_ad(
        client_id=ad.client_id,
        category_slug=ad.category_slug,
        subcategory_slug=ad.subcategory_slug,
        name=ad.name,
        description=ad.description,
        status_label=ad.status_label,
        show_phone=ad.show_phone,
        price=ad.price,
        currency=ad.currency,
        channel_id=ad.channel_id,
        message_id=new_message_ids[0],
        full_message_ids=new_message_ids
    )
    await service.delete_ad(ad.id)
    await bot.delete_messages(chat_id=ad.channel_id, message_ids=old_message_ids)
    await SellBuyService(session).set_next_ability(
        client.id, get_cooldown_name(category), days=get_cooldown_days(category)
    )


@profile_router.callback_query(F.data.startswith('up|ad|'))
async def up_ad(callback: types.CallbackQuery):
    ad_id = int(callback.data.removeprefix('up|ad|'))

    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        ad = await service.get_ad(ad_id)

        if not ad or not client or ad.client_id != client.id:
            await callback.answer(t('ad_not_found', lang), show_alert=True)
            return

        category = category_by_channel_id(ad.channel_id)
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        subscription_date = client.next_subscription_disable
        if subscription_date and subscription_date.replace(tzinfo=None) > now:
            await callback.message.edit_text(
                t('up_ad_confirm_free', lang),
                reply_markup=_up_ad_confirm_kb(ad_id, lang, pay=False),
                parse_mode="HTML"
            )
            await callback.answer()
            return

        field = get_cooldown_name(category)
        next_allowed = getattr(client, field)
        if next_allowed and next_allowed.tzinfo:
            next_allowed = next_allowed.replace(tzinfo=None)

        if next_allowed and next_allowed > now:
            price = get_placement_price(category)
            await callback.message.edit_text(
                t('wait_cooldown', lang).format(time=_format_cooldown_wait(next_allowed, now, lang))
                + "\n\n"
                + t('up_ad_confirm', lang).format(price=money(price, lang), balance=money(client.balance, lang)),
                reply_markup=_up_ad_confirm_kb(ad_id, lang, pay=True),
                parse_mode="HTML"
            )
            await callback.answer()
            return

        await callback.message.edit_text(
            t('up_ad_confirm_free', lang),
            reply_markup=_up_ad_confirm_kb(ad_id, lang, pay=False),
            parse_mode="HTML"
        )
        await callback.answer()


@profile_router.callback_query(F.data.startswith('up_pay|'))
async def up_ad_pay(callback: types.CallbackQuery):
    ad_id = int(callback.data.removeprefix('up_pay|'))

    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        ad = await service.get_ad(ad_id)

        if not ad or not client or ad.client_id != client.id:
            await callback.answer(t('ad_not_found', lang), show_alert=True)
            return

        category = category_by_channel_id(ad.channel_id)
        price = get_placement_price(category)

        if not await service.try_charge(client.id, price):
            await callback.answer(
                t('up_ad_low_balance', lang).format(price=money(price, lang), balance=money(client.balance, lang)),
                show_alert=True
            )
            return

        await _perform_up_ad(callback.bot, session, service, ad, client)

    await callback.answer()
    await callback.message.edit_text(t('up_ad_success', lang), parse_mode="HTML")
    await show_profile_message(callback.message, callback.from_user.id)


@profile_router.callback_query(F.data.startswith('up_yes|'))
async def up_ad_free(callback: types.CallbackQuery):
    ad_id = int(callback.data.removeprefix('up_yes|'))

    async with async_session_maker() as session:
        service, client, lang = await _service_client_lang(session, callback.from_user.id)
        ad = await service.get_ad(ad_id)

        if not ad or not client or ad.client_id != client.id:
            await callback.answer(t('ad_not_found', lang), show_alert=True)
            return

        await _perform_up_ad(callback.bot, session, service, ad, client)

    await callback.answer()
    await callback.message.edit_text(t('up_ad_success', lang), parse_mode="HTML")
    await show_profile_message(callback.message, callback.from_user.id)