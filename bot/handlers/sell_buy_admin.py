import os
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    InputMediaPhoto, ReplyKeyboardRemove
)

from bot.channels import (
    CHANNELS,
    ADMINS,
    SLUG_TO_CATEGORY,
    CATEGORY_TO_SLUG,
    get_category_label,
    get_status_keys,
    get_status_label,
)

ADMIN_LANG = 'ru'

admin_sell_router = Router()

# --- Фильтр на админов (можно использовать в каждом хендлере) ---
def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

# --- FSM для админского размещения ---
class AdminSellFSM(StatesGroup):
    category = State()
    status = State()
    name = State()
    desc = State()
    price = State()
    photos = State()
    phone = State()          # номер телефона (вводит админ)
    seller_tg_id = State()   # tg_id продавца (необязательно)
    confirm = State()

# --- Команда /admin_sell ---
@admin_sell_router.message(Command("admin_sell"))
async def admin_start_sell(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_category_label(name, ADMIN_LANG),
                              callback_data=f"adminsell_cat_{CATEGORY_TO_SLUG[name]}")]
        for name in CHANNELS.keys()
    ])
    await message.answer(
        "🛒 <b>Создание объявления (администратор)</b>\n\n"
        "📌 Выберите категорию:",
        reply_markup=kb,
        parse_mode="HTML"
    )
    await state.set_state(AdminSellFSM.category)

# --- Выбор категории ---
@admin_sell_router.callback_query(F.data.startswith('adminsell_cat_'))
async def admin_choose_category(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён.", show_alert=True)
        return

    slug = callback.data.removeprefix('adminsell_cat_')
    category = SLUG_TO_CATEGORY.get(slug)
    if not category:
        await callback.answer("Неизвестная категория", show_alert=True)
        return
    
    await callback.answer()  # Acknowledge the callback

    await state.update_data(category=category, category_slug=slug)

    # Клавиатура статусов собирается из channels.py (типы объявления канала).
    status_row = [
        InlineKeyboardButton(text=get_status_label(category, key, ADMIN_LANG),
                             callback_data=f"adminsell_status_{key}")
        for key in get_status_keys(category)
    ]
    status_kb = InlineKeyboardMarkup(inline_keyboard=[status_row])

    await callback.message.edit_text(
        f"🗂 Категория: <b>{category}</b>\n\n📌 Выберите тип объявления:",
        reply_markup=status_kb,
        parse_mode="HTML"
    )
    await state.set_state(AdminSellFSM.status)

# --- Выбор статуса ---
@admin_sell_router.callback_query(F.data.startswith('adminsell_status_'))
async def admin_choose_status(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён.", show_alert=True)
        return

    data = await state.get_data()
    category = data.get('category')
    status_key = callback.data.removeprefix('adminsell_status_')
    status = get_status_label(category, status_key, ADMIN_LANG)
    await state.update_data(status=status)

    await callback.message.edit_text(
        "📝 <b>Введите заголовок объявления</b>\n\n"
        "<i>Например: iPhone 13, сдаётся квартира, требуется бариста...</i>",
        parse_mode="HTML"
    )
    await state.set_state(AdminSellFSM.name)

# --- Ввод названия ---
@admin_sell_router.message(AdminSellFSM.name)
async def admin_get_name(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    await state.update_data(name=message.text)
    await message.answer(
        "📝 <b>Опишите объявление подробнее</b>\n\n"
        "<i>Укажите состояние, характеристики, условия и т.д.</i>",
        parse_mode="HTML"
    )
    await state.set_state(AdminSellFSM.desc)

# --- Ввод описания ---
@admin_sell_router.message(AdminSellFSM.desc)
async def admin_get_desc(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    await state.update_data(desc=message.text)
    await message.answer(
        "💵 <b>Укажите цену в KGS:</b>\n\n<i>Только число, например: 2500</i>",
        parse_mode="HTML"
    )
    await state.set_state(AdminSellFSM.price)

# --- Ввод цены ---
@admin_sell_router.message(AdminSellFSM.price)
async def admin_get_price(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    price_text = message.text.replace(" ", "")
    if not price_text.isdigit():
        await message.answer("❗️ Цена должна быть числом. Введите только число.")
        return

    await state.update_data(price=price_text, photos=[])
    await message.answer(
        "📸 <b>Добавьте фотографии</b>\n\n"
        "• Можно до 10 фото\n• Отправляйте по одному\n• Когда закончите, нажмите 'Готово ✅'",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Готово ✅")]],
            resize_keyboard=True,
            one_time_keyboard=True
        ),
        parse_mode="HTML"
    )
    await state.set_state(AdminSellFSM.photos)

# --- Обработка фотографий ---
@admin_sell_router.message(AdminSellFSM.photos)
async def admin_get_photos(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    data = await state.get_data()
    photos = data.get("photos", [])

    if message.photo:
        if len(photos) >= 10:
            await message.answer("⚠️ Максимум 10 фото! Нажмите 'Готово ✅'.")
            return
        file_id = message.photo[-1].file_id
        photos.append(file_id)
        await state.update_data(photos=photos)
        await message.answer(
            f"✅ Фото {len(photos)}/10 добавлено. Добавьте ещё или нажмите 'Готово ✅'.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Готово ✅")]],
                resize_keyboard=True
            )
        )
        return

    if message.text and message.text.lower() in ["готово", "готово ✅"]:
        if not photos:
            await message.answer("❌ Добавьте хотя бы одно фото!")
            return

        await message.answer(
            "📞 <b>Введите номер телефона продавца</b>\n\n"
            "<i>Например: +996 555 123 456 или просто 0555123456</i>",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(AdminSellFSM.phone)
        return

    await message.answer("📸 Отправьте фото или нажмите 'Готово ✅'.")

# --- Ввод номера телефона ---
@admin_sell_router.message(AdminSellFSM.phone)
async def admin_get_phone(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    phone = message.text.strip()
    await state.update_data(phone=phone)

    await message.answer(
        "🆔 <b>Введите Telegram ID продавца</b> (если есть)\n\n"
        "<i>Это нужно для создания ссылки «Написать продавцу». Если не знаете, отправьте 0 или пропустите, нажав /skip</i>\n\n"
        "Команда /skip — пропустить",
        parse_mode="HTML"
    )
    await state.set_state(AdminSellFSM.seller_tg_id)

# --- Пропуск tg_id ---
@admin_sell_router.message(AdminSellFSM.seller_tg_id, Command("skip"))
async def admin_skip_tg_id(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    await state.update_data(seller_tg_id=None)
    await show_admin_preview(message, state)

# --- Ввод tg_id ---
@admin_sell_router.message(AdminSellFSM.seller_tg_id)
async def admin_get_tg_id(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return

    text = message.text.strip()
    tg_id = None
    if text.isdigit() and int(text) != 0:
        tg_id = int(text)

    await state.update_data(seller_tg_id=tg_id)
    await show_admin_preview(message, state)

async def show_admin_preview(message: types.Message, state: FSMContext):
    """Показывает предпросмотр и кнопки подтверждения"""
    data = await state.get_data()
    status = data.get('status', '')
    name = data.get('name', '')
    desc = data.get('desc', '')
    price = data.get('price', '')
    phone = data.get('phone', 'Не указан')
    seller_tg_id = data.get('seller_tg_id')
    photos = data.get('photos', [])

    # Формируем строку "Написать продавцу"
    if seller_tg_id:
        contact_link = f"✉️ <a href='tg://user?id={seller_tg_id}'>Написать продавцу</a>"
    else:
        contact_link = "✉️ Написать продавцу"  # некликабельно

    text = (
        f"<b>{status}</b>\n"
        f"🏷️ <b>{name}</b>\n\n"
        f"{desc}\n\n"
        f"💵 <b>Цена:</b> {price} KGS\n"
        f"📱 <b>Телефон:</b> {phone}\n"
        f"{contact_link}\n"
        f"📢 <a href='https://t.me/tez4917_bot'>Разместить объявление</a>"
    )

    if photos:
        media = [InputMediaPhoto(media=pid) for pid in photos]
        media[0].caption = text
        media[0].parse_mode = "HTML"
        await message.answer_media_group(media)
    else:
        await message.answer(text, parse_mode="HTML")

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🚀 Опубликовать", callback_data="adminsell_confirm_send"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="adminsell_confirm_cancel")
    ]])
    await message.answer("📝 Предпросмотр. Опубликовать?", reply_markup=kb)
    await state.set_state(AdminSellFSM.confirm)

# --- Подтверждение публикации ---
@admin_sell_router.callback_query(F.data.in_(['adminsell_confirm_send', 'adminsell_confirm_cancel']))
async def admin_publish_or_cancel(callback: types.CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён.", show_alert=True)
        return

    if callback.data == 'adminsell_confirm_cancel':
        await callback.message.edit_text("❌ Публикация отменена")
        await state.clear()
        await callback.answer()
        return

    await callback.answer("⏳ Публикуем...")
    data = await state.get_data()
    category = data.get('category')
    chan_info = CHANNELS.get(category)
    if not chan_info:
        await callback.message.answer("Ошибка: категория не найдена.")
        await state.clear()
        return

    status = data.get('status', '')
    name = data.get('name', '')
    desc = data.get('desc', '')
    price = data.get('price', '')
    phone = data.get('phone', 'Не указан')
    seller_tg_id = data.get('seller_tg_id')
    photos = data.get('photos', [])

    if seller_tg_id:
        contact_link = f"✉️ <a href='tg://user?id={seller_tg_id}'>Написать продавцу</a>"
    else:
        contact_link = "✉️ Написать продавцу"

    text = (
        f"<b>{status}</b>\n"
        f"🏷️ <b>{name}</b>\n\n"
        f"{desc}\n\n"
        f"💵 <b>Цена:</b> {price} KGS\n"
        f"📱 <b>Телефон:</b> {phone}\n"
        f"{contact_link}\n"
        f"📢 <a href='https://t.me/tez4917_bot'>Разместить объявление</a>"
    )

    try:
        if photos:
            media = [InputMediaPhoto(media=pid) for pid in photos]
            media[0].caption = text
            media[0].parse_mode = "HTML"
            await callback.bot.send_media_group(chan_info['id'], media)
        else:
            await callback.bot.send_message(chan_info['id'], text, parse_mode="HTML")

        await callback.message.edit_text(
            "✅ <b>Объявление опубликовано администратором!</b>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="👁️ Посмотреть в канале", url=chan_info['link'])]
            ]),
            parse_mode="HTML"
        )
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка публикации: {str(e)}")

    await state.clear()
