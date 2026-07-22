import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.services.base import BaseService

from bot.channels import CHANNELS, get_category_label, get_channel_link, CATEGORY_TO_SLUG

logger = logging.getLogger(__name__)

common_router = Router()


NOT_REGISTERED_STICKER = 'CAACAgIAAxkBAAERh39qUgW9j3XviXxGrdO3X95E0RBbpgACPA4AAryrWEslKJiOAc6xfTwE'
NOT_REGISTERED_TEXT = (
    '🤷 You are not registered yet. Tap the command below to start 👇\n'
    'Вы ещё не зарегистрированы. Нажмите команду ниже, чтобы начать 👇\n\n'
    '/start'
)


def get_available_markets_links(lang: str) -> InlineKeyboardMarkup:
    buttons = []

    for name in CHANNELS.keys():
        button_text = get_category_label(name, lang)
        link = get_channel_link(name)

        buttons.append([InlineKeyboardButton(text=button_text, url=link)])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb


async def send_not_registered(event) -> None:
    target = event.message if isinstance(event, types.CallbackQuery) else event
    await target.answer_sticker(NOT_REGISTERED_STICKER)
    await target.answer(NOT_REGISTERED_TEXT)


async def get_user_lang(user_id: int) -> str:
    async with async_session_maker() as session:
        service = BaseService(session)
        return await service.get_user_lang(user_id)


async def update_user_lang(user_id: int, lang_code: str) -> None:
    async with async_session_maker() as session:
        service = BaseService(session)
        await service.set_language(user_id, lang_code)


def get_main_menu_inline(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=t('menu_market', lang), callback_data="sellbuy")],
        [InlineKeyboardButton(text=t('profile_inline_button', lang), callback_data="check_profile")],
        [InlineKeyboardButton(text=t('menu_categories', lang), callback_data="menu_categories")],
        [
            InlineKeyboardButton(text=t('menu_stores', lang), callback_data="stores"),
            InlineKeyboardButton(text=t('menu_delivery', lang), callback_data="delivery")
        ],
        [InlineKeyboardButton(text=t('menu_change_lang', lang), callback_data="change_lang")],
        [InlineKeyboardButton(text=t('menu_support', lang), callback_data="support")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    button = KeyboardButton(text=t('menu_button', lang))
    return ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def add_menu_to_keyboard(buttons: list, lang: str, resize: bool = True,
                         one_time: bool = False) -> ReplyKeyboardMarkup:
    menu_row = [KeyboardButton(text=t('menu_button', lang))]
    return ReplyKeyboardMarkup(
        keyboard=buttons + [menu_row],
        resize_keyboard=resize,
        one_time_keyboard=one_time
    )


async def show_menu_prompt(chat_id: int, bot, lang: str) -> None:
    await bot.send_message(
        chat_id=chat_id,
        text=t('press_menu_button', lang),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML"
    )


#TODO Delete this later
@common_router.callback_query(F.data.in_(['stores', 'delivery']))
async def fhjfbfkds(cb: types.CallbackQuery):
    await cb.answer('В разработке...')


@common_router.message(F.text.in_([t('menu_button', lang) for lang in ['ru', 'kg', 'en', 'cn']]))
async def cmd_main_menu(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = BaseService(session)
        client = await service.get_client_by_tg(message.from_user.id)
        if not client:
            await send_not_registered(message)
            return
        await state.clear()
        text = t('menu_text', client.language)
        kb = get_main_menu_inline(client.language)
        await message.answer(t('going_to_menu', client.language), reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t('menu_button', client.language))]], resize_keyboard=True), parse_mode="HTML")
        await message.answer(text, reply_markup=kb, parse_mode="HTML")


@common_router.message(Command("menu"))
async def cmd_main_menu_command(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = BaseService(session)
        client = await service.get_client_by_tg(message.from_user.id)
        if not client:
            await send_not_registered(message)
            return
        await state.clear()
        text = t('menu_text', client.language)
        kb = get_main_menu_inline(client.language)
        await message.answer(t('going_to_menu', client.language), reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t('menu_button', client.language))]], resize_keyboard=True), parse_mode="HTML")
        await message.answer(text, reply_markup=kb, parse_mode="HTML")


@common_router.callback_query(F.data == "change_lang")
async def change_language(callback: types.CallbackQuery):
    async with async_session_maker() as session:
        service = BaseService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        if not client:
            await send_not_registered(callback)
            return
        lang = client.language
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="lang_kg")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton(text="🇨🇳 中文", callback_data="lang_cn")],
            [InlineKeyboardButton(text=t('back', lang), callback_data="back_to_menu")],
        ])
        await callback.message.edit_text(
            t('choose_language', lang),
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

    await callback.message.edit_text(t('channels_list', lang), reply_markup=get_available_markets_links(lang), parse_mode="HTML")
    await callback.answer()