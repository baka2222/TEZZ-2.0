import math
import logging
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import (
    ContentType, KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.services.courier_service import CourierService
from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.database.models import Client, CourierOrder, PricingRule, TimeSurcharge

logger = logging.getLogger(__name__)


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


router = Router()
GROUP_CHAT_ID = '-1002265233281'


ORDER_STATUSES = {
    'new': 'Новый',
    'assigned': 'Назначен',
    'to_a': 'В пути до точки А',
    'to_b': 'В пути до точки Б',
    'arrived': 'Приехал',
    'completed': 'Завершён',
}


class DeliveryFSM(StatesGroup):
    point_a = State()
    point_b = State()
    comment_order = State()
    confirm_order = State()


async def get_user_lang(user_id: int) -> str:
    async with async_session_maker() as session:
        service = CourierService(session)
        client = await service.get_client_by_tg(user_id)
        return client.language if client and client.language else 'ru'

def get_main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Клавиатура с единственной кнопкой «Меню»."""
    button = KeyboardButton(text=f"{t('menu_button', lang)}")
    return ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def add_menu_to_keyboard(buttons: list, lang: str, resize=True, one_time=False) -> ReplyKeyboardMarkup:
    """
    Добавляет кнопку «Меню» в переданный список кнопок.
    buttons — список рядов (каждый ряд — список кнопок).
    Возвращает готовую Reply-клавиатуру с дополнительным рядом меню.
    """
    menu_row = [KeyboardButton(text=f"{t('menu_button', lang)}")]
    full_keyboard = buttons + [menu_row]
    return ReplyKeyboardMarkup(
        keyboard=full_keyboard,
        resize_keyboard=resize,
        one_time_keyboard=one_time
    )

async def show_main_menu(chat_id: int, bot, lang: str):
    """Отправляет сообщение с главным меню (вызывается только по команде /start или /menu)."""
    await message.answer(t('going_to_menu', lang), reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=t('menu_button', lang))]], resize_keyboard=True), parse_mode="HTML")
    await bot.send_message(
        chat_id=chat_id,
        text=t('', lang),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML"
    )

async def get_object_or_none(model, session, **kwargs):
    from sqlalchemy import select
    stmt = select(model).filter_by(**kwargs)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_object_or_404(model, tg_obj, session, **kwargs):
    obj = await get_object_or_none(model, session, **kwargs)
    if not obj:
        text = '❌ Объект не найден'
        if isinstance(tg_obj, types.CallbackQuery):
            await tg_obj.answer(text, show_alert=True)
        else:
            await tg_obj.answer(text)
        return None
    return obj

def get_status_keyboard(order_id: int, current_status: str, lang: str) -> InlineKeyboardMarkup:
    """Клавиатура для обновления статуса курьером."""
    buttons = []
    if current_status == 'assigned':
        buttons.append([
            InlineKeyboardButton(text=t('to_a_btn', lang), callback_data=f'status_toa_{order_id}')
        ])
    elif current_status == 'to_a':
        buttons.append([
            InlineKeyboardButton(text=t('to_b_btn', lang), callback_data=f'status_tob_{order_id}')
        ])
    elif current_status == 'to_b':
        buttons.append([
            InlineKeyboardButton(text=t('arrived_btn', lang), callback_data=f'status_arrived_{order_id}')
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

async def calculate_delivery_price(session, point_a: tuple, point_b: tuple):
    lat1, lon1 = point_a
    lat2, lon2 = point_b
    distance = calculate_distance(lat1, lon1, lat2, lon2)

    service = CourierService(session)
    rules = await service.get_pricing_rules()
    base_price = per_km_price = 0
    multiplier = 1.0
    for rule in rules:
        max_dist = rule.max_distance if rule.max_distance > 0 else float('inf')
        if rule.min_distance <= distance < max_dist:
            base_price = float(rule.base_price)
            per_km_price = float(rule.per_km_price)
            multiplier = float(rule.multiplier)
            break
    price = (base_price + distance * per_km_price) * multiplier

    surcharges = await service.get_time_surcharges()
    now = datetime.now().time()
    for surcharge in surcharges:
        if surcharge.start_time <= now <= surcharge.end_time:
            price *= float(surcharge.multiplier)

    return round(price, 2), distance


@router.callback_query(F.data == "delivery")
async def start_delivery(callback: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = CourierService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'
        if not client or client.is_banned:
            await callback.message.answer(t('not_registered_or_banned', lang))
            await state.clear()
            return

    kb = add_menu_to_keyboard(
        [[KeyboardButton(text=t('send_point_a_btn', lang), request_location=True)]],
        lang
    )
    await callback.message.answer(t('send_point_a_text', lang), reply_markup=kb)
    await state.set_state(DeliveryFSM.point_a)
    await callback.answer()


@router.message(DeliveryFSM.point_a, F.content_type == ContentType.LOCATION)
async def get_point_a(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    await state.update_data(point_a=(message.location.latitude, message.location.longitude))

    kb = add_menu_to_keyboard(
        [[KeyboardButton(text=t('send_point_b_btn', lang), request_location=True)]],
        lang
    )
    await message.answer(t('send_point_b_text', lang), reply_markup=kb)
    await state.set_state(DeliveryFSM.point_b)


@router.message(DeliveryFSM.point_b, F.content_type == ContentType.LOCATION)
async def get_point_b(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    await state.update_data(point_b=(message.location.latitude, message.location.longitude))

    kb = add_menu_to_keyboard(
        [[KeyboardButton(text=t('skip_btn', lang))]],
        lang
    )
    await message.answer(t('enter_comment_text', lang), reply_markup=kb)
    await state.set_state(DeliveryFSM.comment_order)


@router.message(DeliveryFSM.comment_order)
async def get_comment(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    skip_text = t('skip_btn', lang)
    text = message.text if message.content_type == ContentType.TEXT and message.text != skip_text else ''
    await state.update_data(comment=text)
    data = await state.get_data()

    async with async_session_maker() as session:
        price, distance = await calculate_delivery_price(session, data['point_a'], data['point_b'])

    preview = (
        f"{t('order_preview', lang)}:\n"
        f"{t('point_a', lang)}: {data['point_a'][0]:.5f}, {data['point_a'][1]:.5f}\n"
        f"{t('point_b', lang)}: {data['point_b'][0]:.5f}, {data['point_b'][1]:.5f}\n"
        f"{t('distance', lang)}: {distance} {t('delivery_distance_unit', lang)}\n"
        f"{t('price', lang)}: {price} {t('delivery_currency', lang)}\n"
        f"{t('comment', lang)}: {text or t('none', lang)}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t('confirm_btn', lang), callback_data='delivery_confirm')],
        [InlineKeyboardButton(text=t('cancel_btn', lang), callback_data='delivery_cancel')]
    ])
    # Убираем временную клавиатуру, оставляя только инлайн-кнопки
    await message.answer(preview, reply_markup=ReplyKeyboardRemove())
    await message.answer(t('confirm_order_text', lang), reply_markup=kb)
    await state.set_state(DeliveryFSM.confirm_order)


@router.callback_query(DeliveryFSM.confirm_order)
async def handle_confirmation(cb: types.CallbackQuery, state: FSMContext):
    await cb.answer()
    
    async with async_session_maker() as session:
        service = CourierService(session)
        client = await service.get_client_by_tg(cb.from_user.id)
        lang = client.language if client and client.language else 'ru'

        if cb.data == 'delivery_cancel':
            await cb.message.edit_text(t('order_cancelled', lang))
            await state.clear()
            # Возвращаем клавиатуру с меню
            await cb.bot.send_message(
                cb.from_user.id,
                t('menu_promt', lang),
                reply_markup=get_main_menu_keyboard(lang),
                parse_mode="HTML"
            )
            return

        if cb.data == 'delivery_confirm':
            data = await state.get_data()
            if not client:
                await cb.message.answer(t('not_registered_or_banned', lang))
                await state.clear()
                await cb.bot.send_message(
                    cb.from_user.id,
                    t('menu_text', lang),
                    reply_markup=get_main_menu_keyboard(lang),
                    parse_mode="HTML"
                )
                return

            price, distance = await calculate_delivery_price(session, data['point_a'], data['point_b'])
            try:
                order = await service.create_courier_order(
                    client_id=client.id,
                    point_a=data['point_a'],
                    point_b=data['point_b'],
                    comment=data.get('comment', ''),
                    price=price,
                    distance=distance
                )
                text = (
                    f"📦 Новый заказ #{order.id}\n"
                    f"📍 https://2gis.kg/geo/{order.point_a_lng:.5f},{order.point_a_lat:.5f}\n"
                    f"💰 Стоимость: {order.price} сом"
                )
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='🚴 Взять заказ', callback_data=f'delivery_take_{order.id}')]
                ])
                await cb.bot.send_message(GROUP_CHAT_ID, text, reply_markup=kb)
                await cb.message.edit_text(t('order_sent_to_couriers', lang))
            except Exception as e:
                logger.error(f"Order creation error: {e}", exc_info=True)
                await cb.message.answer(t('order_creation_error', lang))
            finally:
                await state.clear()
                # Возвращаем клавиатуру с меню
                await cb.bot.send_message(
                    cb.from_user.id,
                    t('menu_promt', lang),
                    reply_markup=get_main_menu_keyboard(lang),
                    parse_mode="HTML"
                )


@router.callback_query(F.data.startswith('delivery_take_'))
async def take_order(cb: types.CallbackQuery):
    await cb.answer()
    order_id = int(cb.data.split('_')[-1])

    async with async_session_maker() as session:
        service = CourierService(session)
        courier = await service.get_client_by_tg(cb.from_user.id)
        lang = courier.language if courier and courier.language else 'ru'
        if not courier or courier.is_banned:
            return await cb.answer(t('cannot_take_order', lang), show_alert=True)

        try:
            order = await service.take_order(order_id, courier.id)
        except ValueError as e:
            return await cb.answer(str(e), show_alert=True)
        except Exception as e:
            logger.error(f"Order take error: {e}", exc_info=True)
            return await cb.answer(t('order_take_error', lang), show_alert=True)

        await cb.message.edit_reply_markup(reply_markup=None)

        details = (
            f"🛵 {t('order', lang)} #{order.id}\n"
            f"👤 {t('client', lang)}: <a href='tg://user?id={order.client.tg_code}'>{order.client.name}</a> - {order.client.phone}\n"
            f"📍 A: https://2gis.kg/geo/{order.point_a_lng:.5f},{order.point_a_lat:.5f}\n"
            f"📍 B: https://2gis.kg/geo/{order.point_b_lng:.5f},{order.point_b_lat:.5f}\n"
            f"📏 {t('distance', lang)}: {order.distance_km} км\n"
            f"💰 {t('price', lang)}: {order.price} сом\n"
            f"📝 {t('comment', lang)}: {order.comment or t('none', lang)}"
        )
        await cb.bot.send_message(cb.from_user.id, details, parse_mode='HTML')

        status_kb = get_status_keyboard(order.id, 'assigned', lang)
        if status_kb.inline_keyboard:
            await cb.bot.send_message(cb.from_user.id, t('update_status_prompt', lang), reply_markup=status_kb)

        # Не показываем меню автоматически, просто оставляем текущую клавиатуру
        # (она либо инлайн, либо у пользователя может быть своя)


@router.callback_query(F.data.regexp(r"^status_(toa|tob|arrived)_[0-9]+$"))
async def update_status(cb: types.CallbackQuery):
    await cb.answer()
    _, action, order_id_str = cb.data.split('_')
    order_id = int(order_id_str)
    status_map = {'toa': 'to_a', 'tob': 'to_b', 'arrived': 'arrived'}
    new_status = status_map.get(action)

    async with async_session_maker() as session:
        service = CourierService(session)
        courier = await service.get_client_by_tg(cb.from_user.id)
        lang = courier.language if courier and courier.language else 'ru'
        
        if not new_status:
            return await cb.answer(t('unknown_action', lang), show_alert=True)
        if not courier:
            return await cb.answer(t('not_registered', lang), show_alert=True)

        order = await service.get_order_by_id(order_id)
        if not order:
            return await cb.answer(t('order_not_found', lang), show_alert=True)

        if order.courier_id != courier.id:
            return await cb.answer(t('not_your_order', lang), show_alert=True)

        await service.update_order_status(order_id, new_status)

        await cb.message.edit_text(
            t('order_status_updated', lang).format(
                order_id=order.id,
                status=t(f'status_{new_status}', lang)
            )
        )

        client_lang = await get_user_lang(int(order.client.tg_code))
        await cb.bot.send_message(
            chat_id=int(order.client.tg_code),
            text=t('order_status_updated', client_lang).format(
                order_id=order.id,
                status=t(f'status_{new_status}', client_lang)
            )
        )

        new_kb = get_status_keyboard(order.id, new_status, lang)
        if new_kb.inline_keyboard:
            await cb.bot.send_message(cb.from_user.id, t('next_step_prompt', lang), reply_markup=new_kb)
        # Если статус конечный, не показываем меню автоматически


# ---------- Общий хэндлер для кнопки «Меню» ----------
# Должен быть после всех FSM-хэндлеров
@router.message(F.text.in_([t('menu_button', lang) for lang in ['ru', 'kg', 'en', 'cn']]))
async def handle_menu_button(message: types.Message, state: FSMContext):
    await state.clear()
    lang = await get_user_lang(message.from_user.id)
    text = t('menu_text', lang)
    kb = get_main_menu_inline(lang)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")