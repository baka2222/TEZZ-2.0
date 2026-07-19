import logging
from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove
)

from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.handlers.menu_handler import get_main_menu_inline, get_available_markets_links
from bot.services.sellbuy_service import SellBuyService
from bot.services.profile_service import ProfileService

logger = logging.getLogger(__name__)

commands_router = Router()


class RegistrationStates(StatesGroup):
    language = State()
    name = State()
    phone = State()


async def add_favorite_deeplink(message: types.Message, ad_id_str: str, lang: str):
    try:
        ad_id = int(ad_id_str)
    except ValueError:
        await message.answer(t('favorite_not_found', lang))
        return
    async with async_session_maker() as session:
        service = ProfileService(session)
        client = await service.get_client_by_tg(message.from_user.id)
        ad = await service.get_ad(ad_id)
        if not ad:
            await message.answer(t('favorite_not_found', lang))
            return
        added = await service.add_favorite(client.id, ad.id)
    await message.answer(
        t('favorite_added', lang) if added else t('already_favorite', lang),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=t('menu_button', lang))]],
            resize_keyboard=True
        )
    )


@commands_router.message(Command('start'))
async def greeting(message: types.Message, state: FSMContext, command: CommandObject):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(message.from_user.id)

        if client:
            lang = client.language if client.language else 'ru'

            arg = command.args if command else None
            if arg and arg.startswith('addfav_'):
                await add_favorite_deeplink(message, arg.removeprefix('addfav_'), lang)
                return

            await message.answer_sticker('CAACAgIAAxkBAAEQqd9ppqYGgpxhWK2uuQ7L3S5d1zqDvAACAQEAAladvQoivp8OuMLmNDoE')
            await message.answer(
                t('remembered_client', lang),
                parse_mode="HTML",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text=t('menu_button', lang))]],
                    resize_keyboard=True
                )
            )
            return
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="strtlang_ru")],
            [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="strtlang_kg")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="strtlang_en")],
            [InlineKeyboardButton(text="🇨🇳 中文", callback_data="strtlang_cn")],
        ])
        await message.answer_sticker(
            "CAACAgIAAxkBAAEQtzhpruHmYB8h_ZAGLpOPGdYCYvziAwACdEkAAqAn-Ep7XyQ4GdeaIDoE"
        )
        await message.answer(
            "🌐 Please choose your language / Пожалуйста, выберите язык:",
            reply_markup=kb
        )
        await state.set_state(RegistrationStates.language)


@commands_router.callback_query(RegistrationStates.language, F.data.startswith("strtlang_"))
async def process_language(callback: CallbackQuery, state: FSMContext):
    """Сохранение выбранного языка и запрос имени."""
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)
    await callback.message.edit_text(f"✏️ {t('registration_name', lang)}")
    await state.set_state(RegistrationStates.name)
    await callback.answer()


@commands_router.message(RegistrationStates.name, ~F.text.in_({"/menu", "/start", "/market"}))
async def ask_phone(message: types.Message, state: FSMContext):
    """Получение имени, запрос телефона."""
    data = await state.get_data()
    lang = data.get('language', 'ru')
    await state.update_data(name=message.text)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t('send_phone_btn', lang), request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        f"📱 {t('registration_phone', lang)}",
        reply_markup=kb
    )
    await state.set_state(RegistrationStates.phone)


def is_own_contact(message: types.Message) -> bool:
    if not message.contact:
        return False
    if message.forward_origin is not None:
        return False
    return message.contact.user_id == message.from_user.id


@commands_router.message(RegistrationStates.phone, F.contact)
async def finish_registration(message: types.Message, state: FSMContext):
    """Завершение регистрации, сохранение в БД и показ главного меню."""
    data = await state.get_data()
    lang = data.get('language', 'ru')

    if not is_own_contact(message):
        await message.answer(t('phone_not_yours', lang), parse_mode="HTML")
        return

    async with async_session_maker() as session:
        service = SellBuyService(session)
        name = data.get('name')
        phone = message.contact.phone_number
        tg_code = str(message.from_user.id)
        username = message.from_user.username

        await service.save_client(name, phone, tg_code, username, lang)

        kb_menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=t('menu_button', lang))]],
            resize_keyboard=True
        )

        await message.answer(
            t('registration_complete', lang),
            reply_markup=kb_menu,
            parse_mode="HTML"
        )
        await message.answer(
            t('channels_list', lang),
            reply_markup=get_available_markets_links(lang),
            parse_mode="HTML"
        )
        await message.answer(
            t('menu_text', lang),
            parse_mode="HTML",
            reply_markup=get_main_menu_inline(lang)
        )
        await state.clear()