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
from aiogram.types import FSInputFile
from pathlib import Path

logger = logging.getLogger(__name__)

sellbuy_router = Router()

# ---------- Конфигурация каналов ----------
CHANNELS = {
    "Веломаркет": {
        "id": -1002615944125,
        "link": "https://t.me/teztezfg",
        "cooldown_field": "next_ability",
        "subcategories": ['frameset', 'wheelset', 'fullbike', 'components', 'crankset', 'accessories', 'clothing', 'velo']
    },
    "Бьютимаркет": {
        "id": -1002762051372,
        "link": "https://t.me/tezbueaty/4",
        "cooldown_field": "next_ability_beauty",
        "subcategories": ['makeup', 'skincare', 'haircare', 'fragrance', 'tools', 'nails', 'models', 'clothing', 'beauty']
    },
    "Техномаркет": {
        "id": -1002897679802,
        "link": "https://t.me/teztechno/2",
        "cooldown_field": "next_ability_techno",
        "subcategories": ['phones', 'laptops', 'tablets', 'wearables', 'audio', 'gaming', 'cameras', 'techno']
    },
    "Автомотомаркет": {
        "id": -1002549461746,
        "link": "https://t.me/tezautomoto/2",
        "cooldown_field": "next_ability_automoto",
        "subcategories": ['cars', 'motorcycles', 'parts', 'accessories', 'tires', 'tools', 'automoto']
    },
    "Недвижимость": {
        "id": -1002711157981,
        "link": "https://t.me/tezhousing/2",
        "cooldown_field": "next_ability_housing",
        "subcategories": ['apartment', 'house', 'land', 'commercial', 'rent', 'one-bedroom', 'two-bedroom', 'three-bedroom', 'housing']
    },
    "Работа": {
        "id": -1002788239459,
        "link": "https://t.me/tezzjob/3",
        "cooldown_field": "next_ability_job",
        "subcategories": ['fulltime', 'parttime', 'contract', 'office', 'athome', 'job']
    }
}

ADMIN_ID = 5837210969

def slugify(name: str) -> str:
    return ''.join(ch if ch.isalnum() else '_' for ch in name).lower()

SLUG_TO_CATEGORY = { slugify(k): k for k in CHANNELS.keys() }
CATEGORY_TO_SLUG = { v: k for k, v in SLUG_TO_CATEGORY.items() }

# ---------- FSM состояния ----------
class SellFSM(StatesGroup):
    category = State()
    status = State()
    subcategory = State()
    name = State()
    desc = State()
    price = State()
    photos = State()
    show_phone = State()
    confirm = State()

class PaidAnnouncement(StatesGroup):
    waiting_for_payment = State()

# ---------- Вспомогательные функции для работы с меню ----------
def get_main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Клавиатура с единственной кнопкой «Меню» (показывается после завершения опроса)."""
    button = KeyboardButton(text=t('menu_button', lang))
    return ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

async def show_menu_prompt(chat_id: int, bot, lang: str):
    """Отправляет подсказку нажать кнопку «Меню» и саму клавиатуру."""
    await bot.send_message(
        chat_id=chat_id,
        text=t('press_menu_button', lang),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML"
    )


@sellbuy_router.message(Command("market"))
async def start_sell_command(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(message.from_user.id)
        lang = client.language if client and client.language else 'ru'

    if not client:
        await message.answer(t('not_registered', lang))
        return
    if client.is_banned:
        await message.answer(t('banned', lang))
        return

    buttons = []
    buttons.append([InlineKeyboardButton(text=t('pin_begin', lang), callback_data='pin_message'), InlineKeyboardButton(text=t('subscription_menu', lang), callback_data='subscription')])

    for name in CHANNELS.keys():
        slug = CATEGORY_TO_SLUG[name]
        button_text = t(f'category_{slug}', lang)
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
        await callback.message.answer(t('not_registered', lang))
        await callback.answer()
        return
    if client.is_banned:
        await callback.message.answer(t('banned', lang))
        await callback.answer()
        return

    buttons = []
    buttons.append([InlineKeyboardButton(text=t('pin_begin', lang), callback_data='pin_message'), InlineKeyboardButton(text=t('subscription_menu', lang), callback_data='subscription')])

    for name in CHANNELS.keys():
        slug = CATEGORY_TO_SLUG[name]
        button_text = t(f'category_{slug}', lang)
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
        await callback.message.answer(t('not_registered', lang))
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
            await state.update_data(category=category, category_slug=slug)

            if category == 'Недвижимость':
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text=t('status_sell', lang), callback_data="sb_status_sell"),
                    InlineKeyboardButton(text=t('status_hand', lang), callback_data="sb_status_hand"),
                    InlineKeyboardButton(text=t('status_search', lang), callback_data="sb_status_search"),
                ]])
            elif category == 'Работа':
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text=t('status_resume', lang), callback_data="sb_status_resume"),
                    InlineKeyboardButton(text=t('status_vacancy', lang), callback_data="sb_status_vacancy"),
                ]])
            elif category == 'Бьютимаркет':
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text=t('status_sell', lang), callback_data="sb_status_sell"),
                    InlineKeyboardButton(text=t('status_poda', lang), callback_data="sb_status_poda"),
                    InlineKeyboardButton(text=t('status_search', lang), callback_data="sb_status_search"),
                ]])
            else:
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text=t('status_sell', lang), callback_data="sb_status_sell"),
                    InlineKeyboardButton(text=t('status_exchange', lang), callback_data="sb_status_exchange"),
                    InlineKeyboardButton(text=t('status_search', lang), callback_data="sb_status_search"),
                ]])

            category_display = t(f'category_{slug}', lang)
            await callback.message.delete()
            await callback.message.answer(subscription_text, parse_mode="HTML")
            await callback.message.answer(
                t('choose_status', lang).format(category=category_display),
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

        pay_kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=t('pay_placement_button', lang), callback_data=f"sb_paid|{slug}|{callback.from_user.id}")
        ]])

        await callback.message.edit_text(t('wait_cooldown', lang).format(category=category, time=time_str))
        await callback.message.answer(t('pay_placement', lang), reply_markup=pay_kb)
        await state.clear()
        return

    await state.update_data(category=category, category_slug=slug)

    if category == 'Недвижимость':
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=t('status_sell', lang), callback_data="sb_status_sell"),
            InlineKeyboardButton(text=t('status_hand', lang), callback_data="sb_status_hand"),
            InlineKeyboardButton(text=t('status_search', lang), callback_data="sb_status_search"),
        ]])
    elif category == 'Работа':
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=t('status_resume', lang), callback_data="sb_status_resume"),
            InlineKeyboardButton(text=t('status_vacancy', lang), callback_data="sb_status_vacancy"),
        ]])
    elif category == 'Бьютимаркет':
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=t('status_sell', lang), callback_data="sb_status_sell"),
            InlineKeyboardButton(text=t('status_poda', lang), callback_data="sb_status_poda"),
            InlineKeyboardButton(text=t('status_search', lang), callback_data="sb_status_search"),
        ]])
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=t('status_sell', lang), callback_data="sb_status_sell"),
            InlineKeyboardButton(text=t('status_exchange', lang), callback_data="sb_status_exchange"),
            InlineKeyboardButton(text=t('status_search', lang), callback_data="sb_status_search"),
        ]])

    category_display = t(f'category_{slug}', lang)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(
        t('choose_status', lang).format(category=category_display),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.status)

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

    status_map = {
        "sb_status_sell": t('status_sell', lang),
        "sb_status_exchange": t('status_exchange', lang),
        "sb_status_search": t('status_search', lang),
        "sb_status_hand": t('status_hand', lang),
        "sb_status_resume": t('status_resume', lang),
        "sb_status_vacancy": t('status_vacancy', lang),
        "sb_status_poda": t('status_poda', lang),
    }
    status = status_map.get(callback.data, t('status_sell', lang))
    await state.update_data(status=status)

    subcategories = CHANNELS.get(data.get('category'), {}).get('subcategories', [])
    buttons = []
    for subkey in subcategories:
        sub_name = t(f'subcategory_{subkey}', lang)
        buttons.append([InlineKeyboardButton(text=sub_name, callback_data=f"sb_subcat_{subkey}")])
    ikb = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(t('enter_subcategory', lang).format(category=data.get('category')), reply_markup=ikb, parse_mode="HTML")
    await state.set_state(SellFSM.subcategory)

@sellbuy_router.callback_query(F.data.startswith('sb_subcat_'))
async def choose_subcategory(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    await callback.answer()
    subkey = callback.data.removeprefix('sb_subcat_')
    await state.update_data(subcategory=subkey)

    await callback.message.edit_text(t('ad_title', lang), parse_mode="HTML")
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

    await state.update_data(name=message.text)
    await message.answer(t('ad_desc', lang), parse_mode="HTML")
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

    await state.update_data(desc=message.text)
    await message.answer(t('ad_price', lang), parse_mode="HTML")
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

    price_text = message.text.replace(" ", "")
    if not price_text.isdigit():
        await message.answer(t('price_must_be_number', lang), parse_mode="HTML")
        return
    await state.update_data(price=price_text, photos=[])

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t('done_button', lang))], [KeyboardButton(text=t('menu_button', lang))]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        t('add_photos', lang),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(SellFSM.photos)

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

        # Клавиатура только с кнопкой "Готово" (без меню)
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=t('done_button', lang))]],
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
        await message.answer(
            t('show_phone', lang),
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
    status = data.get('status', '')
    subcategory = data.get('subcategory', '')
    name = data.get('name', '')
    desc = data.get('desc', '')
    price = data.get('price', '')
    photos = data.get('photos', []) or []

    phone_text = (
        f"📱 {t('phone', lang)}: {client.phone if client and client.phone else 'Не указан'}"
        if show_phone else
        f"📱 {t('phone', lang)}: {t('hidden', lang)}"
    )

    text = (
        f'<b>#{subcategory}</b>\n'
        f'<b>{client.name} | {client.tg_code}</b>\n'
        f"<b>{status}</b>\n"
        f"🏷️ <b>{name}</b>\n\n"
        f"{desc}\n\n"
        f"💵 <b>{t('price', lang)}:</b> {price} KGS\n"
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

@sellbuy_router.callback_query(F.data.in_(['sb_confirm_send', 'sb_confirm_cancel']))
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

    await callback.answer(t('sending_ad', lang))
    data = await state.get_data()
    chan_info = CHANNELS.get(data.get('category'))
    if not chan_info:
        await callback.message.answer(t('channel_not_found', lang))
        await state.clear()
        await show_menu_prompt(callback.from_user.id, callback.bot, lang)
        return

    status = data.get('status', '')
    subcategory = data.get('subcategory', '')
    name = data.get('name', '')
    desc = data.get('desc', '')
    price = data.get('price', '')
    photos = data.get('photos', []) or []
    show_phone = data.get('show_phone', False)

    phone_text_russian = (
        f"📱 Телефон: {client.phone if client and client.phone else 'Не указан'}"
        if show_phone else
        f"📱 Телефон: Скрыт"
    )

    text_for_channel = (
        f'<b>#{subcategory}</b>\n'
        f'<b>{client.name} | {client.tg_code}</b>\n'
        f"<b>{status}</b>\n"
        f"🏷️ <b>{name}</b>\n\n"
        f"{desc}\n\n"
        f"💵 <b>Цена:</b> {price} KGS\n"
        f"{phone_text_russian}\n"
        f"✉️ <a href='tg://user?id={callback.from_user.id}'>Написать продавцу</a>\n"
        f"📢 <a href='https://t.me/tez4917_bot'>Разместить объявление</a>"
    )

    try:
        message_id = None

        if photos:
            sent_messages = await callback.bot.send_media_group(chan_info['id'], [
                InputMediaPhoto(media=pid, caption=text_for_channel if i == 0 else "", parse_mode="HTML")
                for i, pid in enumerate(photos)
            ])
            if sent_messages:
                message_id = sent_messages[0].message_id
        else:
            sent_message = await callback.bot.send_message(chan_info['id'], text_for_channel, parse_mode="HTML")
            message_id = sent_message.message_id

        channel_link = chan_info['link']
        if '/t.me/' in channel_link:
            username = channel_link.split('/t.me/')[-1].split('/')[0]
        else:
            username = None

        if username:
            message_link = f"https://t.me/{username}/{message_id}"
        else:
            message_link = chan_info['link']

        async with async_session_maker() as session:
            service = SellBuyService(session)
            client = await service.get_client_by_tg(callback.from_user.id)
            if client:
                await service.set_next_ability(client.id, chan_info["cooldown_field"])

        await callback.message.edit_text(
            t('ad_published', lang),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t('see_in_channel', lang), url=message_link)]
            ]),
            parse_mode="HTML"
        )
        await show_menu_prompt(callback.from_user.id, callback.bot, lang)

    except Exception as e:
        await callback.message.answer(t('publish_error', lang).format(error=str(e)))
        print(f"Error publishing ad: {e}")
        await state.clear()
        await show_menu_prompt(callback.from_user.id, callback.bot, lang)