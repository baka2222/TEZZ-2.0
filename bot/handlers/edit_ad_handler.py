import re
import logging
import asyncio
from typing import Dict, Any

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.session import async_session as async_session_maker
from bot.services.sellbuy_service import SellBuyService
from bot.translations import t
from bot.handlers.sellbuy import CHANNELS

logger = logging.getLogger(__name__)

edit_router = Router()
waiting_album_lock = asyncio.Lock()

# ---------- FSM состояния ----------
class EditFSM(StatesGroup):
    waiting_for_message = State()
    choose_field = State()
    edit_status = State()
    edit_subcategory = State()
    edit_name = State()
    edit_desc = State()
    edit_price = State()
    edit_phone_visibility = State()


# ---------- Вспомогательные функции ----------
def extract_user_id_from_caption(caption: str) -> str:
    if not caption:
        return None
    match = re.search(r"tg://user\?id=(\d+)", caption)
    if match:
        return match.group(1)
    lines = caption.split('\n')
    if len(lines) >= 2:
        second_line = re.sub(r'<[^>]+>', '', lines[1])
        parts = second_line.split('|')
        if len(parts) >= 2:
            possible_id = parts[-1].strip()
            if possible_id.isdigit():
                return possible_id
    return None


def parse_ad_caption(caption: str) -> Dict[str, str]:
    if not caption:
        return {}
    lines = caption.split('\n')
    result = {}

    # 1. Подкатегория
    if lines:
        raw = lines[0].strip()
        result['subcategory'] = re.sub(r'<[^>]+>', '', raw).lstrip('#')
    else:
        result['subcategory'] = ''

    # 2. Строка с пользователем
    if len(lines) > 1:
        result['user_info'] = re.sub(r'<[^>]+>', '', lines[1]).strip()
    else:
        result['user_info'] = ''

    # 3. Статус (сохраняем вместе с эмодзи, не удаляем)
    if len(lines) > 2:
        raw_status = re.sub(r'<[^>]+>', '', lines[2]).strip()
        result['status'] = raw_status   # <--- исправлено: не убираем эмодзи
    else:
        result['status'] = ''

    # 4. Название и описание
    name = None
    desc_lines = []
    found_name = False
    for i, line in enumerate(lines):
        if '🏷️' in line or '🏷' in line:
            name = re.sub(r'<[^>]+>', '', line).replace('🏷️', '').replace('🏷', '').strip()
            found_name = True
            continue
        if found_name:
            if '💵' in line:
                break
            clean_line = re.sub(r'<[^>]+>', '', line).strip()
            if clean_line:
                desc_lines.append(clean_line)
    result['name'] = name if name else ''
    result['desc'] = '\n'.join(desc_lines).strip()

    # 5. Цена
    price = ''
    for line in lines:
        if '💵' in line:
            match = re.search(r'(\d+)', line)
            price = match.group(1) if match else ''
            break
    result['price'] = price

    # 6. Телефон
    phone_line = ''
    for line in lines:
        if '📱' in line:
            phone_line = line.strip()
            break
    result['phone_line'] = phone_line

    # 7. Контакт
    contact_line = ''
    for line in lines:
        if '✉️' in line:
            contact_line = line.strip()
            break
    result['contact_line'] = contact_line

    # 8. Реклама бота
    ad_line = ''
    for line in lines:
        if '📢' in line:
            ad_line = line.strip()
            break
    result['ad_line'] = ad_line

    return result


def build_new_caption(parsed: Dict[str, str], user_id: str, client_phone: str = None, show_phone: bool = None) -> str:
    """
    Собирает caption в том же формате, что и при публикации в sellbuy.
    Все поля приводятся к строке, чтобы избежать None.
    """
    subcategory = str(parsed.get('subcategory', ''))
    user_info = str(parsed.get('user_info', ''))
    status = str(parsed.get('status', ''))
    name = str(parsed.get('name', ''))
    desc = str(parsed.get('desc', ''))
    price = str(parsed.get('price', ''))

    # Формируем строку телефона
    if client_phone is not None and show_phone is not None:
        if show_phone:
            phone_line = f"📱 Телефон: {client_phone if client_phone else 'Не указан'}"
        else:
            phone_line = "📱 Телефон: Скрыт"
    else:
        phone_line = parsed.get('phone_line', "📱 Телефон: Скрыт")
        if phone_line is None:
            phone_line = "📱 Телефон: Скрыт"

    contact_line = f"✉️ <a href='tg://user?id={user_id}'>Написать продавцу</a>"
    ad_line = "📢 <a href='https://t.me/tez4917_bot'>Разместить объявление</a>"

    # Собираем структуру (два переноса после названия и после описания)
    parts = [
        f"<b>#{subcategory}</b>",
        f"<b>{user_info}</b>",
        f"<b>{status}</b>",
        f"🏷️ <b>{name}</b>\n",
        ""
    ]
    if desc and str(desc).strip():
        parts.append(f"{str(desc)}\n")
        parts.append("")
    parts.extend([
        f"💵 Цена: {price} KGS",
        phone_line,
        contact_line,
        ad_line
    ])
    # Фильтруем None и пустые строки
    clean_parts = []
    for p in parts:
        if p is None:
            continue
        if isinstance(p, str) and p == "":
            continue
        clean_parts.append(p)
    return '\n'.join(clean_parts)


# ---------- Клавиатуры ----------
def get_edit_fields_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=t('status', lang), callback_data="edit_field_status")],
        [InlineKeyboardButton(text=t('subcategory', lang), callback_data="edit_field_subcategory")],
        [InlineKeyboardButton(text=t('title', lang), callback_data="edit_field_name")],
        [InlineKeyboardButton(text=t('description', lang), callback_data="edit_field_desc")],
        [InlineKeyboardButton(text=t('edit_price', lang), callback_data="edit_field_price")],
        [InlineKeyboardButton(text=t('phone', lang), callback_data="edit_field_phone")],
        [InlineKeyboardButton(text=t('publish', lang), callback_data="edit_publish"),
         InlineKeyboardButton(text=t('cancel', lang), callback_data="edit_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_status_keyboard(category: str, lang: str) -> InlineKeyboardMarkup:
    if category == 'Недвижимость':
        statuses = ['sell', 'hand', 'search']
    elif category == 'Работа':
        statuses = ['resume', 'vacancy']
    elif category == 'Бьютимаркет':
        statuses = ['sell', 'poda', 'search']
    else:
        statuses = ['sell', 'exchange', 'search']

    emoji_map = {
        'sell': '💰',
        'exchange': '🔄',
        'search': '🔍',
        'hand': '🔑',
        'resume': '👨‍💼',
        'vacancy': '💼',
        'poda': '👀'
    }
    buttons = []
    for s in statuses:
        emoji = emoji_map.get(s, '')
        text = t(f'status_{s}', lang)
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"edit_set_status_{s}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_subcategory_keyboard(category: str, lang: str) -> InlineKeyboardMarkup:
    subcategories = CHANNELS.get(category, {}).get('subcategories', [])
    buttons = []
    for subkey in subcategories:
        sub_name = t(f'subcategory_{subkey}', lang)
        buttons.append([InlineKeyboardButton(text=sub_name, callback_data=f"edit_set_subcat_{subkey}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@edit_router.callback_query(F.data == "edit_ad")
async def start_edit(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    await callback.message.answer(t('ask_for_message_to_edit', lang))
    await state.set_state(EditFSM.waiting_for_message)
    await callback.answer()


@edit_router.message(EditFSM.waiting_for_message)
async def receive_message_to_edit(message: types.Message, state: FSMContext):
    async with waiting_album_lock:
        async with async_session_maker() as session:
            service = SellBuyService(session)
            user = await service.get_client_by_tg(message.from_user.id)
            lang = user.language if user and user.language else 'ru'

        # Обработка медиагруппы – отвечаем только один раз
        data = await state.get_data()
        if message.media_group_id:
            if data.get("processed_media_group_id") == message.media_group_id:
                return
            await state.update_data(processed_media_group_id=message.media_group_id)

        if not message.forward_origin:
            await message.answer(t("pin_forward_only", lang))
            return

        original_chat_id = message.forward_origin.chat.id
        if original_chat_id not in [chan["id"] for chan in CHANNELS.values()]:
            await message.answer(t("pin_wrong_channel", lang))
            return

        original_message_id = message.forward_origin.message_id
        original_caption = message.caption or ""

        tg_id = extract_user_id_from_caption(original_caption)
        if tg_id != str(message.from_user.id):
            await message.answer(t("edit_ad_not_your_ad", lang))
            return

        parsed = parse_ad_caption(original_caption)

        category = None
        for cat_name, chan_data in CHANNELS.items():
            if chan_data["id"] == original_chat_id:
                category = cat_name
                break
        if not category:
            await message.answer(t("unknown_category", lang))
            return

        await state.update_data(
            channel_id=original_chat_id,
            message_id=original_message_id,
            category=category,
            subcategory=parsed.get('subcategory'),
            status=parsed.get('status'),
            name=parsed.get('name'),
            desc=parsed.get('desc'),
            price=parsed.get('price'),
            phone_line=parsed.get('phone_line'),
            contact_line=parsed.get('contact_line'),
            ad_line=parsed.get('ad_line'),
            user_info=parsed.get('user_info'),
            user_id=tg_id,
            original_caption=original_caption
        )

        kb = get_edit_fields_keyboard(lang)
        await message.answer(t('choose_field_to_edit', lang), reply_markup=kb)
        await state.set_state(EditFSM.choose_field)


@edit_router.callback_query(EditFSM.choose_field, F.data.startswith("edit_field_"))
async def process_field_selection(callback: types.CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[-1]
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    data = await state.get_data()
    category = data.get('category')

    if field == "status":
        kb = await get_status_keyboard(category, lang)
        await callback.message.edit_text(t('edit_status_prompt', lang), reply_markup=kb)
        await state.set_state(EditFSM.edit_status)
    elif field == "subcategory":
        kb = await get_subcategory_keyboard(category, lang)
        await callback.message.edit_text(t('edit_subcategory_prompt', lang), reply_markup=kb)
        await state.set_state(EditFSM.edit_subcategory)
    elif field == "name":
        await callback.message.edit_text(t('edit_name_prompt', lang))
        await state.set_state(EditFSM.edit_name)
    elif field == "desc":
        await callback.message.edit_text(t('edit_desc_prompt', lang))
        await state.set_state(EditFSM.edit_desc)
    elif field == "price":
        await callback.message.edit_text(t('edit_price_prompt', lang))
        await state.set_state(EditFSM.edit_price)
    elif field == "phone":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t('show_phone_yes', lang), callback_data="edit_phone_yes"),
             InlineKeyboardButton(text=t('show_phone_no', lang), callback_data="edit_phone_no")]
        ])
        await callback.message.edit_text(t('edit_phone_prompt', lang), reply_markup=kb)
        await state.set_state(EditFSM.edit_phone_visibility)
    await callback.answer()


@edit_router.callback_query(EditFSM.edit_status, F.data.startswith("edit_set_status_"))
async def set_new_status(callback: types.CallbackQuery, state: FSMContext):
    status_key = callback.data.split("_")[-1]
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)

    emoji_map = {
        'sell': '💰',
        'exchange': '🔄',
        'search': '🔍',
        'hand': '🔑',
        'resume': '👨‍💼',
        'vacancy': '💼',
        'poda': '👀'
    }
    emoji = emoji_map.get(status_key, '')
    status_text = t(f'status_{status_key}', lang)

    await state.update_data(status=status_text)
    await callback.message.edit_text(t('field_updated', lang).format(field=t('status', lang), value=status_text))
    kb = get_edit_fields_keyboard(lang)
    await callback.message.answer(t('choose_field_to_edit', lang), reply_markup=kb)
    await state.set_state(EditFSM.choose_field)
    await callback.answer()


@edit_router.callback_query(EditFSM.edit_subcategory, F.data.startswith("edit_set_subcat_"))
async def set_new_subcategory(callback: types.CallbackQuery, state: FSMContext):
    subkey = callback.data.split("_")[-1]
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)
    sub_name = t(f'subcategory_{subkey}', lang)
    await state.update_data(subcategory=subkey)
    await callback.message.edit_text(t('field_updated', lang).format(field=t('subcategory', lang), value=sub_name))
    kb = get_edit_fields_keyboard(lang)
    await callback.message.answer(t('choose_field_to_edit', lang), reply_markup=kb)
    await state.set_state(EditFSM.choose_field)
    await callback.answer()


@edit_router.message(EditFSM.edit_name)
async def set_new_name(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)
    new_name = message.text.strip()
    if not new_name:
        await message.answer(t('invalid_name', lang))
        return
    await state.update_data(name=new_name)
    await message.answer(t('field_updated', lang).format(field=t('title', lang), value=new_name))
    kb = get_edit_fields_keyboard(lang)
    await message.answer(t('choose_field_to_edit', lang), reply_markup=kb)
    await state.set_state(EditFSM.choose_field)


@edit_router.message(EditFSM.edit_desc)
async def set_new_desc(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)
    new_desc = message.text.strip()
    await state.update_data(desc=new_desc)
    preview = new_desc[:50] + "..." if len(new_desc) > 50 else new_desc
    await message.answer(t('field_updated', lang).format(field=t('description', lang), value=preview))
    kb = get_edit_fields_keyboard(lang)
    await message.answer(t('choose_field_to_edit', lang), reply_markup=kb)
    await state.set_state(EditFSM.choose_field)


@edit_router.message(EditFSM.edit_price)
async def set_new_price(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)
    price_text = message.text.replace(" ", "")
    if not price_text.isdigit():
        await message.answer(t('price_must_be_number', lang))
        return
    await state.update_data(price=price_text)
    await message.answer(t('field_updated', lang).format(field=t('edit_price', lang), value=price_text))
    kb = get_edit_fields_keyboard(lang)
    await message.answer(t('choose_field_to_edit', lang), reply_markup=kb)
    await state.set_state(EditFSM.choose_field)


@edit_router.callback_query(EditFSM.edit_phone_visibility, F.data.in_(['edit_phone_yes', 'edit_phone_no']))
async def set_new_phone_visibility(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

    show_phone = callback.data == 'edit_phone_yes'
    await state.update_data(show_phone=show_phone, client_phone=client.phone)
    visibility_text = t('show_phone_yes', lang) if show_phone else t('show_phone_no', lang)
    await callback.message.edit_text(t('field_updated', lang).format(field=t('phone', lang), value=visibility_text))
    kb = get_edit_fields_keyboard(lang)
    await callback.message.answer(t('choose_field_to_edit', lang), reply_markup=kb)
    await state.set_state(EditFSM.choose_field)
    await callback.answer()


@edit_router.callback_query(EditFSM.choose_field, F.data == "edit_publish")
async def publish_edit(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

    data = await state.get_data()

    parsed = {
        'subcategory': data.get('subcategory'),
        'user_info': data.get('user_info'),
        'status': data.get('status'),
        'name': data.get('name'),
        'desc': data.get('desc'),
        'price': data.get('price'),
    }

    show_phone = data.get('show_phone')
    client_phone = data.get('client_phone') or (client.phone if client else None)
    user_id = data.get('user_id', str(callback.from_user.id))

    new_caption = build_new_caption(parsed, user_id, client_phone, show_phone)

    channel_id = data['channel_id']
    message_id = data['message_id']

    try:
        await callback.bot.edit_message_caption(
            chat_id=channel_id,
            message_id=message_id,
            caption=new_caption,
            parse_mode="HTML"
        )

        # Формируем ссылку на сообщение
        channel_link = None
        for cat_name, chan_data in CHANNELS.items():
            if chan_data["id"] == channel_id:
                channel_link = chan_data["link"]
                break

        if channel_link and '/t.me/' in channel_link:
            username = channel_link.split('/t.me/')[-1].split('/')[0]
            message_link = f"https://t.me/{username}/{message_id}"
        else:
            message_link = channel_link or ""

        if message_link:
            view_button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t('see_in_channel', lang), url=message_link)]
            ])
            await callback.message.edit_text(
                t('edit_success', lang),
                reply_markup=view_button,
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(t('edit_success', lang))

        await state.clear()
    except Exception as e:
        await callback.message.answer(t('edit_error', lang).format(error=str(e)))
    await callback.answer()


@edit_router.callback_query(EditFSM.choose_field, F.data == "edit_cancel")
async def cancel_edit(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t('edit_cancelled', lang))
    await state.clear()
    await callback.answer()