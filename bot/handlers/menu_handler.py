import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import update

from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.database.models import Client
from bot.services.shop_service import ShopService

logger = logging.getLogger(__name__)

common_router = Router()


async def get_user_lang(user_id: int) -> str:
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(user_id)
        return client.language if client and client.language else 'ru'


async def update_user_lang(user_id: int, lang_code: str) -> None:
    """Обновляет язык пользователя в базе данных."""
    async with async_session_maker() as session:
        stmt = update(Client).where(Client.tg_code == str(user_id)).values(language=lang_code)
        await session.execute(stmt)
        await session.commit()


def get_main_menu_inline(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=t('menu_market', lang), callback_data="sellbuy")],
        [InlineKeyboardButton(text=t('edit_ad_button_inline', lang), callback_data="edit_ad")],
        [InlineKeyboardButton(text=t('delete_ad', lang), callback_data="delete_ad")],
        [InlineKeyboardButton(text=t('menu_categories', lang), callback_data="menu_categories")],
        [
            InlineKeyboardButton(text=t('menu_stores', lang), callback_data="stores"),
            InlineKeyboardButton(text=t('menu_delivery', lang), callback_data="delivery")
        ],
        [InlineKeyboardButton(text=t('menu_change_lang', lang), callback_data="change_lang")],
        [InlineKeyboardButton(text=t('menu_support', lang), url="https://t.me/isbakks")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Хэндлер для текстовой кнопки "Меню" (reply-клавиатура)
@common_router.message(F.text.in_([t('menu_button', lang) for lang in ['ru', 'kg', 'en', 'cn']]))
async def cmd_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    lang = await get_user_lang(message.from_user.id)
    text = t('menu_text', lang)
    kb = get_main_menu_inline(lang)
    await message.answer(t('going_to_menu', lang), reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t('menu_button', lang))]], resize_keyboard=True), parse_mode="HTML")
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@common_router.message(Command("menu"))
async def cmd_main_menu_command(message: types.Message, state: FSMContext):
    await state.clear()
    lang = await get_user_lang(message.from_user.id)
    text = t('menu_text', lang)
    kb = get_main_menu_inline(lang)
    await message.answer(t('going_to_menu', lang), reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t('menu_button', lang))]], resize_keyboard=True), parse_mode="HTML")
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@common_router.callback_query(F.data == "change_lang")
async def change_language(callback: types.CallbackQuery):
    """Показывает выбор языка."""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="lang_kg")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇨🇳 中文", callback_data="lang_cn")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_menu")],
    ])
    await callback.message.edit_text(
        "🌐 Пожалуйста, выберите язык / Please choose your language:",
        reply_markup=kb
    )
    await callback.answer()


@common_router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    """Сохраняет выбранный язык и возвращает в меню."""
    lang_map = {
        "lang_ru": "ru",
        "lang_kg": "kg",
        "lang_en": "en",
        "lang_cn": "cn"
    }
    new_lang = lang_map.get(callback.data)
    if not new_lang:
        await callback.answer("Ошибка выбора языка", show_alert=True)
        return

    # Сохраняем язык в БД
    await update_user_lang(callback.from_user.id, new_lang)

    # Показываем обновлённое меню
    kb = get_main_menu_inline(new_lang)
    await callback.message.delete()
    await callback.message.answer(
        t('language_changed', new_lang),
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t('menu_button', new_lang))]], resize_keyboard=True),
        parse_mode="HTML"
    )
    await callback.message.answer(
        t('menu_text', new_lang),
        reply_markup=get_main_menu_inline(new_lang), # Нижняя клава
        parse_mode="HTML"
    )
    await callback.answer()


@common_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    """Возврат в главное меню."""
    lang = await get_user_lang(callback.from_user.id)
    kb = get_main_menu_inline(lang)
    await callback.message.edit_text(
        t('menu_text', lang),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()


@common_router.callback_query(F.data == "menu_categories")
async def show_categories(callback: types.CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)

    await callback.message.edit_text(t('channels_list', lang), parse_mode="HTML")
    await callback.answer()