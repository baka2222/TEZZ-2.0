import logging
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove
)
from sqlalchemy import select, update

from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.database.models import Client
from bot.handlers.menu_handler import get_main_menu_inline

logger = logging.getLogger(__name__)

commands_router = Router()


class RegistrationStates(StatesGroup):
    language = State()
    name = State()
    phone = State()


async def get_client_by_tg(tg_code: str) -> Client | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Client).where(Client.tg_code == tg_code)
        )
        return result.scalar_one_or_none()


async def get_user_lang(tg_code: str) -> str:
    client = await get_client_by_tg(tg_code)
    return client.language if client and client.language else 'ru'


async def save_client(name: str, phone: str, tg_code: str, username: str | None = None, language: str = 'ru') -> Client:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Client).where(Client.tg_code == tg_code)
        )
        client = result.scalar_one_or_none()

        if client:
            updated = False
            if client.name != name:
                client.name = name
                updated = True
            if client.phone != phone:
                client.phone = phone
                updated = True
            if username and client.username != username:
                client.username = username
                updated = True
            if client.language != language:
                client.language = language
                updated = True
            if updated:
                await session.commit()
        else:
            client = Client(
                tg_code=tg_code,
                name=name,
                phone=phone,
                username=username,
                language=language
            )
            session.add(client)
            await session.commit()
            await session.refresh(client)

        return client


@commands_router.message(Command('start'))
async def greeting(message: types.Message, state: FSMContext):
    """Начало регистрации: выбор языка."""
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


@commands_router.message(RegistrationStates.name)
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


@commands_router.message(RegistrationStates.phone)
async def finish_registration(message: types.Message, state: FSMContext):
    """Завершение регистрации, сохранение в БД и показ главного меню."""
    data = await state.get_data()
    name = data.get('name')
    lang = data.get('language', 'ru')
    phone = message.contact.phone_number if message.contact else message.text
    tg_code = str(message.from_user.id)
    username = message.from_user.username

    await save_client(name, phone, tg_code, username, lang)

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
        parse_mode="HTML"
    )
    await message.answer(
        t('menu_text', lang),
        parse_mode="HTML",
        reply_markup=get_main_menu_inline(lang)
    )
    await state.clear()