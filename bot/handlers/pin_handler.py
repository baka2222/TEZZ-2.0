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


class AlbumMiddleware(BaseMiddleware):
    """Собирает все сообщения из одного альбома в список и передаёт в хендлер."""
    def __init__(self, latency: float = 0.5):
        self.latency = latency
        self.album_data: Dict[str, List[Message]] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        group_id = event.media_group_id
        if group_id not in self.album_data:
            self.album_data[group_id] = []
        self.album_data[group_id].append(event)

        await asyncio.sleep(self.latency)

        album_messages = self.album_data.pop(group_id, [event])
        data['album'] = album_messages
        return await handler(event, data)


pin_router = Router()
ADMIN_ID = 5837210969
waiting_album_lock = asyncio.Lock()

class PinStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_payment = State()


async def unpin_message(chat_id, message_id):
    from bot.main import bot
    channel_link = f'https://t.me/c/{str(chat_id)[4:]}'
    message_link = f'{channel_link}/{message_id}'
    try:
        await bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
        await bot.send_message(
            ADMIN_ID,
            (
                f"📌 Сообщение <a href=\"{message_link}\">{message_id}</a> откреплено автоматически."
            ),
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


@pin_router.callback_query(F.data == "pin_message")
async def pin_message_handler(callback_query: types.CallbackQuery, state: FSMContext):
    async with session() as sess:
        service = SellBuyService(sess)
        lang = await service.get_user_lang(callback_query.from_user.id)

    await callback_query.message.answer_sticker('CAACAgIAAxkBAAEQ5L1p1-PpKJc1KrMcTHB53pOCfXY4PAACswEAAhZCawp4Wn8enz1mxDsE')
    await callback_query.message.answer(t("pin_pls_send_message", lang), parse_mode="HTML")
    await state.set_state(PinStates.waiting_for_message)
    await callback_query.answer()


@pin_router.message(PinStates.waiting_for_message)
async def receive_message_to_pin(message: types.Message, state: FSMContext):
    async with waiting_album_lock:
        async with session() as sess:
            service = SellBuyService(sess)
            lang = await service.get_user_lang(message.from_user.id)

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

        await state.update_data(
            channel_message_id=original_message_id,
            channel_id=original_chat_id
        )

        channel_link = f'<a href="https://t.me/c/{str(original_chat_id)[4:]}">TEZZ</a>'
        await message.answer(t("pin_preview", lang).format(channel_username=channel_link), parse_mode="HTML")

        qr_path = Path(__file__).resolve().parent.parent / "assets" / "mbank_qr100.jpg"
        photo_qr = FSInputFile(qr_path)
        await message.answer_photo(photo_qr, caption=t("pin_payment_instruction", lang))

        await state.set_state(PinStates.waiting_for_payment)


@pin_router.message(PinStates.waiting_for_payment, F.photo)
async def receive_payment_confirmation(
    message: types.Message,
    state: FSMContext,
    album: List[types.Message] = None,
):
    msg = album[0] if album else message

    data = await state.get_data()
    if data.get("receipt_sent"):
        return

    async with session() as sess:
        service = SellBuyService(sess)
        lang = await service.get_user_lang(msg.from_user.id)

    channel_message_id = data.get("channel_message_id")
    channel_id = data.get("channel_id")

    file_id = msg.photo[-1].file_id

    channel_link = f'https://t.me/c/{str(channel_id)[4:]}'
    message_link = f'{channel_link}/{channel_message_id}'
    user_link = f'tg://user?id={msg.from_user.id}'

    caption = (
        f"📌 Новый чек на закрепление\n\n"
        f"Сообщение: <a href=\"{message_link}\">Открыть</a>\n"
        f"👤 <a href=\"{user_link}\">@{msg.from_user.username or msg.from_user.full_name or msg.from_user.id}</a>\n"
        f"🆔 <code>{msg.from_user.id}</code>\n"
        f"📅 {(datetime.utcnow() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')}"
    )

    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("pin_confirm_admin", "ru"), callback_data=f"pin_confirm|{msg.from_user.id}|{channel_id}|{channel_message_id}"),
        InlineKeyboardButton(text=t("pin_decline_admin", "ru"), callback_data=f"pin_decline|{msg.from_user.id}")
    ]])

    try:
        await msg.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=ikb
        )
        await msg.answer(t("pin_receipt_sent", lang))
        await state.update_data(receipt_sent=True)
        await state.clear()
    except Exception as e:
        await msg.answer(t("error_sending_receipt", lang).format(error=str(e)))


@pin_router.callback_query(F.data.startswith("pin_confirm|"))
async def admin_confirm_pin(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Только админ может подтверждать.", show_alert=True)
        return

    try:
        _, user_id, channel_id, message_id = callback.data.split("|", 3)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    async with session() as sess:
        service = SellBuyService(sess)
        lang_user = await service.get_user_lang(int(user_id))

    try:
        await callback.bot.pin_chat_message(chat_id=int(channel_id), message_id=int(message_id))
        unpin_time = datetime.now() + timedelta(days=10)
        scheduler.add_job(unpin_message, "date", run_date=unpin_time, args=[int(channel_id), int(message_id)])
        await callback.bot.send_message(int(user_id), t("pin_payment_confirmed", lang_user))
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Закрепление подтверждено.")
    except Exception as e:
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)


@pin_router.callback_query(F.data.startswith("pin_decline|"))
async def admin_decline_pin(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Только админ может отклонять.", show_alert=True)
        return

    try:
        _, user_id = callback.data.split("|", 1)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    async with session() as sess:
        service = SellBuyService(sess)
        lang_user = await service.get_user_lang(int(user_id))

    try:
        await callback.bot.send_message(int(user_id), t("pin_payment_declined", lang_user))
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Закрепление отклонено.")
    except Exception as e:
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)