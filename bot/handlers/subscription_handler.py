import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.database.session import async_session as async_session_maker
from bot.services.sellbuy_service import SellBuyService
from bot.translations import t


subscription_router = Router()
ADMIN_ID = 5837210969


class SubscriptionStates(StatesGroup):
    waiting_for_payment = State()


@subscription_router.callback_query(F.data == "subscription")
async def subscribe_callback(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(callback.from_user.id)

    if not client:
        await callback.message.answer(t('not_registered', 'ru'))
        await callback.answer()
        return

    lang = client.language if client.language else 'ru'

    qr_path = Path(__file__).resolve().parent.parent / "assets" / "mbank_qr100.jpg"
    photo_qr = FSInputFile(qr_path)

    await callback.message.answer_sticker('CAACAgIAAxkBAAEQ5Ltp1-L_l06cpCPVip7jgW5RFd0JLwACbgAD5KDOByc3KCA4N217OwQ')
    await callback.message.answer(t('subscription_start', lang), parse_mode="HTML")
    await callback.message.answer_photo(
        photo=photo_qr,
        caption=t('subscription_pls_send_payment', lang),
        parse_mode="HTML"
    )
    await state.set_state(SubscriptionStates.waiting_for_payment)
    await callback.answer()


@subscription_router.message(SubscriptionStates.waiting_for_payment, F.photo)
async def process_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("receipt_sent"):
        return

    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(message.from_user.id)

    file_id = message.photo[-1].file_id

    user_link = f'tg://user?id={message.from_user.id}'
    caption = (
        f"💎 Новый чек на оплату подписки\n\n"
        f"👤 <a href=\"{user_link}\">@{message.from_user.username or message.from_user.full_name or message.from_user.id}</a>\n"
        f"🆔 <code>{message.from_user.id}</code>\n"
        f"📅 {(datetime.now(timezone.utc) + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')}"
    )

    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить подписку", callback_data=f"sub_confirm|{message.from_user.id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"sub_decline|{message.from_user.id}")
        ]
    ])

    try:
        await message.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=ikb
        )
        await message.answer(t("subscription_receipt_sent", lang))
        await state.update_data(receipt_sent=True)
        await state.clear()
    except Exception as e:
        await message.answer(t("error_sending_receipt", lang).format(error=str(e)))


@subscription_router.callback_query(F.data.startswith("sub_confirm|"))
async def admin_confirm_subscription(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Только админ может подтверждать.", show_alert=True)
        return

    try:
        _, user_id = callback.data.split("|", 1)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    user_id = int(user_id)

    async with async_session_maker() as session:
        service = SellBuyService(session)
        client = await service.get_client_by_tg(user_id)
        if client:
            await service.set_next_subscription_disable(client.id, days=30)
            lang = client.language or 'ru'
            await callback.bot.send_message(
                user_id,
                t("subscription_payment_confirmed", lang).format(days=30)
            )
            await callback.answer("Подписка активирована.")
        else:
            await callback.answer("Пользователь не найден.", show_alert=True)

    await callback.message.edit_reply_markup(reply_markup=None)


@subscription_router.callback_query(F.data.startswith("sub_decline|"))
async def admin_decline_subscription(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Только админ может отклонять.", show_alert=True)
        return

    try:
        _, user_id = callback.data.split("|", 1)
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    user_id = int(user_id)

    async with async_session_maker() as session:
        service = SellBuyService(session)
        lang = await service.get_user_lang(user_id)

    await callback.bot.send_message(user_id, t("subscription_payment_declined", lang))
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Подписка отклонена.")