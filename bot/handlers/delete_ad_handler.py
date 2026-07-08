import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Any, Awaitable, List
from aiogram import BaseMiddleware, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message
from bot.database.session import async_session as session
from bot.database.session import scheduler
from bot.handlers.sellbuy import CHANNELS
from bot.services.sellbuy_service import SellBuyService
from bot.translations import t


delete_ad_router = Router()
waiting_album_lock = asyncio.Lock()


def get_tg_id_caption(caption: str) -> str:
    if not caption:
        return None
    return caption.split('\n')[1].split('|')[1].strip()


def generate_new_caption(caption: str, tg_id: str) -> str:
    if not caption:
        return None
    lines = caption.split('\n')
    new_cap = ''
    for i in range(len(lines)):
        if i == 0:
            new_cap += f'<b>{lines[0].strip()}</b>\n'
        elif i == 1:
            new_cap += f"<b>{lines[1].strip()} | ❌ПРОДАНО</b>\n"
        elif i == 2:
            new_cap += f"<b>{lines[2].strip()}</b>\n"
        elif i == 3:
            new_cap += f"<b>{lines[3].strip()}</b>\n"
        elif i == len(lines) - 2:
            new_cap += f"✉️ <a href='tg://user?id={tg_id}'>Написать продавцу</a>\n"
        elif i == len(lines) - 1:
            new_cap += f"📢 <a href='https://t.me/tez4917_bot'>Разместить объявление</a>"
        else:
            new_cap += lines[i] + '\n'
    return new_cap.strip()


def check_is_sold(caption: str) -> bool:
    if not caption:
        return False

    if caption.split('\n')[1].split('|')[-1].strip() == '❌ПРОДАНО':
        return True
    else:
        return False


class DeleteAdStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirm = State()


@delete_ad_router.callback_query(F.data == 'delete_ad')
async def start_deletion(callback: types.CallbackQuery, state: FSMContext):
    async with session() as sess:
        service = SellBuyService(sess)
        lang = await service.get_user_lang(callback.from_user.id)

    await callback.message.answer_sticker('CAACAgIAAxkBAAERRElqEHuQtMsH1poiR3icIwueR_596wAChXUAAmPXaUo-iahbpWQs3jsE')
    await callback.message.answer(t('ask_for_message_to_delete', lang=lang))
    await state.set_state(DeleteAdStates.waiting_for_message)
    await callback.answer()


@delete_ad_router.message(DeleteAdStates.waiting_for_message)
async def receive_message_to_delete(message: Message, state: FSMContext):
    async with waiting_album_lock:
        async with session() as sess:
            service = SellBuyService(sess)
            user = await service.get_client_by_tg(message.from_user.id)
            lang = user.language if user and user.language else 'ru'

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

        if get_tg_id_caption(original_caption) != str(message.from_user.id):
            await message.answer(t("delete_ad_not_your_ad", lang))
            return

        await message.answer(t("delete_confirmation", lang), parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t("delete_yes", lang), callback_data="confirm_delete")],
            [InlineKeyboardButton(text=t("delete_no", lang), callback_data="cancel_delete")]
        ]))

        await state.update_data(
            channel_message_id=original_message_id,
            channel_id=original_chat_id,
            original_caption=original_caption,
            user_id=message.from_user.id
        )
        await state.set_state(DeleteAdStates.waiting_for_confirm)


@delete_ad_router.callback_query(DeleteAdStates.waiting_for_confirm, F.data == "confirm_delete")
async def confirm_deletion(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel_id = data.get("channel_id")
    channel_message_id = data.get("channel_message_id")
    original_caption = data.get("original_caption", "")
    
    async with session() as sess:
        service = SellBuyService(sess)
        user = await service.get_client_by_tg(callback.from_user.id)
        lang = user.language if user and user.language else 'ru'

    if check_is_sold(original_caption):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(t("delete_already_sold", lang))
        await callback.answer()
        await state.clear()
        return
    
    new_caption = generate_new_caption(original_caption, str(callback.from_user.id))
    
    try:
        await callback.bot.edit_message_caption(
            chat_id=channel_id,
            message_id=channel_message_id,
            caption=new_caption,
            parse_mode="HTML"
        )
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(t("delete_success", lang))
    except Exception as e:
        await callback.message.answer(e)
    
    await callback.answer()
    await state.clear()


@delete_ad_router.callback_query(DeleteAdStates.waiting_for_confirm, F.data == "cancel_delete")
async def cancel_deletion(callback: types.CallbackQuery, state: FSMContext):
    async with session() as sess:
        service = SellBuyService(sess)
        user = await service.get_client_by_tg(callback.from_user.id)
        lang = user.language if user and user.language else 'ru'
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(t("delete_ad_cancelled", lang))
    await callback.answer()
    await state.clear()