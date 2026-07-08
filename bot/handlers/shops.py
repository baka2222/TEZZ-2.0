import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton, ContentType, ReplyKeyboardRemove,
    InputMediaPhoto, FSInputFile
)
from sqlalchemy.ext.asyncio import AsyncSession
from .delivery import calculate_delivery_price, GROUP_CHAT_ID
from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.services.shop_service import ShopService


logger = logging.getLogger(__name__)

shops_router = Router()
ITEMS_PER_PAGE = 5


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

async def show_menu_prompt(chat_id: int, bot, lang: str):
    """Отправляет подсказку нажать кнопку «Меню» и саму клавиатуру."""
    await bot.send_message(
        chat_id=chat_id,
        text=t('press_menu_button', lang),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML"
    )

# ---------- Класс состояний ----------
class CartFSM(StatesGroup):
    category = State()
    shop = State()
    choosing_type = State()
    choosing_items = State()
    confirm = State()
    delivery_question = State()
    delivery_point_b = State()
    delivery_confirm = State()


@shops_router.callback_query(F.data == "stores")
async def start_stores(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

        await state.clear()
        cats = await service.get_categories()
        if not cats:
            await callback.message.answer(t('no_categories', lang), parse_mode="HTML")
            await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            await callback.answer()
            return

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=service.get_localized(cat, 'name', lang),
                                  callback_data=f"cat_{cat.id}")]
            for cat in cats
        ])
        await callback.message.answer(
            t('shops_title', lang),
            reply_markup=kb,
            parse_mode="HTML"
        )
        await state.set_state(CartFSM.category)
        await callback.answer()

@shops_router.callback_query(lambda c: c.data.startswith("cat_"))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

        await callback.answer()
        cat_id = int(callback.data.split("_")[1])
        shops = await service.get_shops_by_category(cat_id)
        if not shops:
            await callback.message.edit_text(t('no_shops', lang), parse_mode="HTML")
            await state.clear()
            await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            return

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=service.get_localized(shop, 'name', lang),
                                  callback_data=f"shop_{shop.id}")]
            for shop in shops
        ])
        await callback.message.edit_text(
            t('choose_shop', lang),
            reply_markup=kb,
            parse_mode="HTML"
        )
        await state.set_state(CartFSM.shop)

@shops_router.callback_query(lambda c: c.data.startswith("shop_"))
async def handle_shop_selection(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

        await callback.answer()
        shop_id = int(callback.data.split("_")[1])
        shop = await service.get_shop_by_id(shop_id)
        if not shop:
            await callback.message.edit_text(t('shop_not_found', lang), parse_mode="HTML")
            await state.clear()
            await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            return

        await state.update_data(shop_id=shop_id)
        products = await service.get_products(shop_id)
        services = await service.get_services(shop_id)

        text = (
            f"🏪 <b>{service.get_localized(shop, 'name', lang)}</b>\n"
            f"👤 <b>{t('owner', lang)}:</b> {shop.owner.name}\n"
            f"📍 <b>{t('address', lang)}:</b> {shop.address or t('not_specified', lang)}\n"
            f"ℹ️ <b>{t('description', lang)}:</b> {service.get_localized(shop, 'description', lang) or t('no_description', lang)}\n\n"
            f"📌 <b>{t('choose_type', lang)}:</b>"
        )

        buttons = []
        if products:
            buttons.append(InlineKeyboardButton(text=f"🛒 {t('products', lang)}", callback_data="type_products"))
        if services:
            buttons.append(InlineKeyboardButton(text=f"🛠 {t('services', lang)}", callback_data="type_services"))

        kb = InlineKeyboardMarkup(inline_keyboard=[buttons])
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        await state.set_state(CartFSM.choosing_type)

@shops_router.callback_query(lambda c: c.data in ("type_products", "type_services"))
async def handle_type_selection(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

        await callback.answer()
        data = await state.get_data()
        chosen_type = callback.data.split("_")[1]

        if 'cart_products' not in data:
            data['cart_products'] = {}
        if 'cart_services' not in data:
            data['cart_services'] = {}

        await state.update_data(
            chosen_type=chosen_type,
            current_page=0,
            cart_products=data.get('cart_products', {}),
            cart_services=data.get('cart_services', {})
        )
        await state.set_state(CartFSM.choosing_items)
        await show_items_page(callback, state, 0, lang, session)

async def show_items_page(callback: CallbackQuery, state: FSMContext, page: int, lang: str, session: AsyncSession):
    service = ShopService(session)
    await callback.answer()
    data = await state.get_data()
    shop_id = data["shop_id"]
    chosen = data["chosen_type"]
    if chosen == "products":
        all_items = await service.get_products(shop_id)
    else:
        all_items = await service.get_services(shop_id)

    total = len(all_items)
    start = page * ITEMS_PER_PAGE
    end = min(start + ITEMS_PER_PAGE, total)
    items_slice = all_items[start:end]

    item_type = f"🛠 {t('services', lang)}" if chosen == 'services' else f"🛒 {t('products', lang)}"
    text = f"📋 <b>{t('choose_type', lang).replace('Выберите тип товаров', '')} {item_type}:</b>\n\n"

    for item in items_slice:
        text += f"• {service.get_localized(item, 'name', lang)} — <b>{item.price} KGS</b>\n"

    keyboard_buttons = []
    if chosen == 'products':
        for item in items_slice:
            cart_key = f"cart_{chosen}"
            cart = data.get(cart_key, {})
            qty = cart.get(item.id, 0)
            btn_text = f"➕ {service.get_localized(item, 'name', lang)} ({qty})" if qty > 0 else f"➕ {service.get_localized(item, 'name', lang)}"
            keyboard_buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"preview_{chosen}_{item.id}")])
    else:
        for item in items_slice:
            cart_key = f"cart_{chosen}"
            cart = data.get(cart_key, {})
            qty = cart.get(item.id, 0)
            btn_text = f"➕ {service.get_localized(item, 'name', lang)} ({qty})" if qty > 0 else f"➕ {service.get_localized(item, 'name', lang)}"
            keyboard_buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"add_{chosen}_{item.id}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️ " + t('back', lang), callback_data=f"page_{page-1}"))
    if end < total:
        nav.append(InlineKeyboardButton(text=t('forward', lang) + " ➡️", callback_data=f"page_{page+1}"))

    buttons_row = []
    if data.get('cart_products') or data.get('cart_services'):
        buttons_row.append(InlineKeyboardButton(text=t('cart', lang), callback_data="items_done"))
    buttons_row.append(InlineKeyboardButton(text=t('back_to_type', lang), callback_data="back_to_type"))

    if nav:
        keyboard_buttons.append(nav)
    if buttons_row:
        keyboard_buttons.append(buttons_row)
    if keyboard_buttons:
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons_row])

    page_count = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    text += f"\n\n{t('page_indicator', lang).format(current=page + 1, total=page_count)}"

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(current_page=page)

@shops_router.callback_query(lambda c: c.data.startswith(("add_", "page_", "items_done", "back_to_type", "preview_", "photo_")))
async def handle_item_callbacks(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

        data = await state.get_data()

        if callback.data == "items_done":
            await confirm_cart(callback, state, lang, session)
            return

        if callback.data == "back_to_type":
            await back_to_type_selection(callback, state, lang, session)
            return

        if callback.data.startswith("page_"):
            page = int(callback.data.split("_")[1])
            await show_items_page(callback, state, page, lang, session)
            return

        if callback.data.startswith("preview_add_"):
            await callback.answer(t('added_to_cart', lang))
            _, _, chosen, item_id = callback.data.split("_")
            item_id = int(item_id)
            cart_key = f"cart_{chosen}"
            cart = data.get(cart_key, {})
            cart[item_id] = cart.get(item_id, 0) + 1
            await state.update_data(**{cart_key: cart})
            await back_to_type_selection(callback, state, lang, session)
            return

        if callback.data == "preview_cancel":
            await callback.answer(t('preview_cancelled', lang))
            await back_to_type_selection(callback, state, lang, session)
            return

        if callback.data.startswith("preview_"):
            _, chosen, item_id = callback.data.split("_")
            item_id = int(item_id)
            item = await service.get_product_by_id(item_id) if chosen == 'products' else await service.get_service_by_id(item_id)
            if not item:
                await callback.message.answer(t('product_not_found', lang), parse_mode="HTML")
                await show_items_page(callback, state, data["current_page"], lang, session)
                return

            await callback.answer(t('preview_item', lang).format(service.get_localized(item, 'name', lang)))

            if chosen == 'products':
                product_paths = await service.get_images_for_product(item_id, 'backend/media')
                if product_paths:
                    await send_product_preview_with_photos(callback, item, product_paths, lang, service)
                else:
                    await send_product_preview_text(callback, item, lang, service)
            else:
                await send_product_preview_text(callback, item, lang, service)
            return

        if callback.data.startswith("photo_prev_"):
            await callback.answer()
            _, _, item_id, index = callback.data.split("_")
            item_id = int(item_id)
            index = int(index) - 1
            product_paths = await service.get_images_for_product(item_id, 'backend/media')
            await edit_photo_page(callback, item_id, index, product_paths, lang, service)
            return

        if callback.data.startswith("photo_next_"):
            await callback.answer()
            _, _, item_id, index = callback.data.split("_")
            item_id = int(item_id)
            index = int(index) + 1
            product_paths = await service.get_images_for_product(item_id, 'backend/media')
            await edit_photo_page(callback, item_id, index, product_paths, lang, service)
            return

        parts = callback.data.split("_")
        cart_key = f"cart_{parts[1]}"
        item_id = int(parts[2])

        cart = data.get(cart_key, {})
        cart[item_id] = cart.get(item_id, 0) + 1
        await state.update_data(**{cart_key: cart})

        await show_items_page(callback, state, data["current_page"], lang, session)

async def back_to_type_selection(callback: CallbackQuery, state: FSMContext, lang: str, session: AsyncSession):
    service = ShopService(session)
    data = await state.get_data()
    shop_id = data["shop_id"]
    shop = await service.get_shop_by_id(shop_id)
    products = await service.get_products(shop_id)
    services = await service.get_services(shop_id)

    text = (
        f"🏪 <b>{service.get_localized(shop, 'name', lang)}</b>\n"
        f"👤 <b>{t('owner', lang)}:</b> {shop.owner.name}\n"
        f"📍 <b>{t('address', lang)}:</b> {shop.address or t('not_specified', lang)}\n"
        f"ℹ️ <b>{t('description', lang)}:</b> {service.get_localized(shop, 'description', lang) or t('no_description', lang)}\n\n"
        f"📌 <b>{t('choose_type', lang)}:</b>"
    )

    buttons = []
    if products:
        buttons.append(InlineKeyboardButton(text=f"🛒 {t('products', lang)}", callback_data="type_products"))
    if services:
        buttons.append(InlineKeyboardButton(text=f"🛠 {t('services', lang)}", callback_data="type_services"))
    if data.get('cart_products') or data.get('cart_services'):
        buttons.append(InlineKeyboardButton(text=f"{t('cart', lang)}", callback_data="items_done"))

    kb = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await state.set_state(CartFSM.choosing_type)

async def confirm_cart(callback: CallbackQuery, state: FSMContext, lang: str, session: AsyncSession):
    service = ShopService(session)
    data = await state.get_data()
    shop = await service.get_shop_by_id(data.get("shop_id"))

    cart_products = data.get("cart_products", {})
    cart_services = data.get("cart_services", {})

    all_products = {p.id: p for p in await service.get_products(data["shop_id"])}
    all_services = {s.id: s for s in await service.get_services(data["shop_id"])}

    selected_products = []
    selected_services = []
    total_price = 0

    for pid, qty in cart_products.items():
        if pid in all_products:
            item = all_products[pid]
            selected_products.append((item, qty))
            total_price += item.price * qty

    for sid, qty in cart_services.items():
        if sid in all_services:
            item = all_services[sid]
            selected_services.append((item, qty))
            total_price += item.price * qty

    if not selected_products and not selected_services:
        await callback.message.answer(t('cart_empty', lang), parse_mode="HTML")
        await show_menu_prompt(callback.from_user.id, callback.bot, lang)
        return

    text = f"<b>{t('cart', lang)}:</b>\n\n"
    for item, qty in selected_products:
        text += f"• {service.get_localized(item, 'name', lang)} — <b>{item.price} KGS</b> x{qty} = <b>{item.price * qty} KGS</b>\n"
    for item, qty in selected_services:
        text += f"• {service.get_localized(item, 'name', lang)} — <b>{item.price} KGS</b> x{qty} = <b>{item.price * qty} KGS</b>\n"
    text += f"\n💰 <b>{t('cart_total', lang).format(total=total_price)}</b>\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t('order_confirm', lang), callback_data="cart_confirm"),
        InlineKeyboardButton(text=t('continue_shopping', lang), callback_data="back_to_type"),
        InlineKeyboardButton(text=t('cart_cancel', lang), callback_data="cart_cancel")
    ]])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await state.set_state(CartFSM.confirm)

@shops_router.callback_query(lambda c: c.data in ("cart_confirm", "cart_cancel", "back_to_type"))
async def finalize_order(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

        await callback.answer()
        data = await state.get_data()

        if callback.data == "cart_cancel":
            await callback.message.edit_text(t('cart_cancel', lang), parse_mode="HTML")
            await state.clear()
            await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            return

        if callback.data == "back_to_type":
            await back_to_type_selection(callback, state, lang, session)
            return

        if not client:
            await callback.message.edit_text(t('order_error', lang), parse_mode="HTML")
            await state.clear()
            await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            return

        shop = await service.get_shop_by_id(data["shop_id"])

        cart_products = data.get("cart_products", {})
        cart_services = data.get("cart_services", {})

        all_products = {p.id: p for p in await service.get_products(data["shop_id"])}
        all_services = {s.id: s for s in await service.get_services(data["shop_id"])}

        total_price = 0
        selected_products = []
        selected_services = []

        for pid, qty in cart_products.items():
            if pid in all_products:
                item = all_products[pid]
                total_price += item.price * qty
                selected_products.append((item, qty))

        for sid, qty in cart_services.items():
            if sid in all_services:
                item = all_services[sid]
                total_price += item.price * qty
                selected_services.append((item, qty))

        order = await service.create_order(shop.id, client.id, total_price)

        if selected_products:
            await service.add_order_items(order.id, selected_products, 'products')
        if selected_services:
            await service.add_order_items(order.id, selected_services, 'services')

        text = (
            f"✅ <b>{t('order_done', lang).format(order_id=order.id)}</b>\n\n"
            f"🏪 <b>{t('owner', lang)}:</b> {shop.owner.name}\n"
            f"💰 <b>{t('price', lang)}:</b> {total_price} KGS\n\n"
            f"{t('delivery_question', lang)}"
        )

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t('delivery_yes', lang), callback_data="delivery_yes")],
            [InlineKeyboardButton(text=t('delivery_no', lang), callback_data="delivery_no")]
        ])

        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        await state.update_data(order_id=order.id, shop_id=shop.id)
        await state.set_state(CartFSM.delivery_question)

@shops_router.callback_query(CartFSM.delivery_question, F.data.in_(["delivery_yes", "delivery_no"]))
async def handle_delivery_choice(callback: CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'

        await callback.answer()
        data = await state.get_data()

        if callback.data == "delivery_no":
            try:
                order_id = data['order_id']
                shop_id = data['shop_id']

                order = await service.get_order_with_items(order_id)
                shop = await service.get_shop_by_id(shop_id)

                owner_message = (
                    f"📦 <b>{t('order', lang)} #{order.id}</b>\n"
                    f"👤 {t('client', lang)}: <a href='tg://user?id={client.tg_code}'>{client.name}</a> ({client.phone})\n"
                    f"📅 {t('date', lang)}: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"<b>{t('order_items', lang)}:</b>\n"
                )

                for item in order.items:
                    if item.product:
                        owner_message += f"  - {service.get_localized(item.product, 'name', lang)} × {item.quantity} = {item.product.price * item.quantity} KGS\n"
                    elif item.service:
                        owner_message += f"  - {service.get_localized(item.service, 'name', lang)} × {item.quantity} = {item.service.price * item.quantity} KGS\n"

                owner_message += f"\n💰 <b>{t('cart_total', lang).format(total=order.total_price)}</b>"

                await callback.bot.send_message(
                    chat_id=shop.owner.tg_code,
                    text=owner_message,
                    parse_mode="HTML"
                )

                await callback.message.edit_text(
                    t('order_completed', lang),
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Order notification error: {e}", exc_info=True)
                await callback.message.edit_text(
                    t('order_error', lang),
                    parse_mode="HTML"
                )
            finally:
                await state.clear()
                await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            return

        shop = await service.get_shop_by_id(data['shop_id'])

        if not shop.point_a_lat or not shop.point_a_lng:
            await callback.message.answer(t('shop_delivery_not_configured', lang))
            await state.clear()
            await show_menu_prompt(callback.from_user.id, callback.bot, lang)
            return

        # Клавиатура с геолокацией + кнопка меню
        kb = add_menu_to_keyboard(
            [[KeyboardButton(text=t('send_point_b', lang), request_location=True)]],
            lang
        )
        await callback.message.answer(
            t('send_point_b_text', lang),
            reply_markup=kb
        )
        await state.set_state(CartFSM.delivery_point_b)

@shops_router.message(CartFSM.delivery_point_b, F.content_type == ContentType.LOCATION)
async def get_delivery_point_b(message: types.Message, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(message.from_user.id)
        lang = client.language if client and client.language else 'ru'

        try:
            data = await state.get_data()
            shop = await service.get_shop_by_id(data['shop_id'])
            order_id = data['order_id']

            order = await service.get_order_with_items(order_id)
            comment = await service.generate_comment(order_id)

            point_a = (shop.point_a_lat, shop.point_a_lng)
            point_b = (message.location.latitude, message.location.longitude)
            price, distance = await calculate_delivery_price(session, point_a, point_b)

            await state.update_data(
                point_b=point_b,
                comment=comment,
                price=price,
                distance=distance
            )

            preview = (
                f"📦 {t('order_preview', lang)} #{order.id}\n"
                f"🏪 {t('shop', lang)}: {service.get_localized(shop, 'name', lang)}\n"
                f"📍 {t('point_a', lang)}: {shop.address or t('shop', lang)}\n"
                f"📍 {t('point_b', lang)}: {t('your_location', lang)}\n"
                f"📏 {t('distance', lang)}: {distance:.2f} км\n"
                f"💰 {t('price', lang)}: {price:.2f} сом"
            )

            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t('confirm_btn', lang), callback_data='delivery_confirm')],
                [InlineKeyboardButton(text=t('cancel_btn', lang), callback_data='delivery_cancel')]
            ])

            await message.answer(preview, reply_markup=ReplyKeyboardRemove())
            await message.answer(t('confirm_order_text', lang), reply_markup=kb)
            await state.set_state(CartFSM.delivery_confirm)

        except Exception as e:
            logger.error(f"Delivery location error: {e}", exc_info=True)
            await message.answer(t('order_error', lang))
            await state.clear()
            await show_menu_prompt(message.chat.id, message.bot, lang)

@shops_router.callback_query(CartFSM.delivery_confirm, F.data.in_(['delivery_confirm', 'delivery_cancel']))
async def handle_delivery_confirmation(cb: types.CallbackQuery, state: FSMContext):
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(cb.from_user.id)
        lang = client.language if client and client.language else 'ru'

        await cb.answer()

        if cb.data == 'delivery_cancel':
            await cb.message.edit_text(t('delivery_cancelled', lang))
            await state.clear()
            await show_menu_prompt(cb.from_user.id, cb.bot, lang)
            return

        try:
            data = await state.get_data()
            shop = await service.get_shop_by_id(data['shop_id'])
            point_b = data['point_b']

            courier_order = await service.create_courier_order(
                client_id=client.id,
                shop=shop,
                point_b=point_b,
                comment=data['comment'],
                price=data['price'],
                distance=data['distance']
            )

            text = (
                f"📦 {t('new_order', lang)} #{courier_order.id}\n"
                f"🏪 {t('shop', lang)}: {service.get_localized(shop, 'name', lang)}\n"
                f"📍 {t('point_a', lang)}: {t('shop', lang)}\n"
                f"📍 {t('point_b', lang)}: {t('client', lang)}\n"
                f"💰 {t('price', lang)}: {courier_order.price:.2f} сом\n"
                f"📏 {t('distance', lang)}: {courier_order.distance_km:.2f} км"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='🚴 ' + t('take_order', lang), callback_data=f'delivery_take_{courier_order.id}')]
            ])
            await cb.bot.send_message(GROUP_CHAT_ID, text, reply_markup=kb)

            await cb.message.edit_text(t('order_sent_to_couriers', lang))

        except Exception as e:
            logger.error(f"Delivery order error: {e}", exc_info=True)
            await cb.message.answer(t('order_creation_error', lang))
        finally:
            await state.clear()
            await show_menu_prompt(cb.from_user.id, cb.bot, lang)

async def send_product_preview_text(callback: CallbackQuery, item, lang: str, service: ShopService):
    preview_text = (
        f"🛒 <b>{service.get_localized(item, 'name', lang)}</b>\n"
        f"💰 <b>{item.price} KGS</b>\n"
        f"📌 <b>{t('description', lang)}:</b> {service.get_localized(item, 'description', lang) or t('no_description', lang)}\n"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t('preview_add_to_cart', lang), callback_data=f"preview_add_{'products' if hasattr(item, 'images') else 'services'}_{item.id}")],
        [InlineKeyboardButton(text=t('preview_cancel', lang), callback_data="preview_cancel")]
    ])
    await callback.message.edit_text(preview_text, reply_markup=kb, parse_mode="HTML")

async def send_product_preview_with_photos(callback: CallbackQuery, item, product_paths: list, lang: str, service: ShopService):
    caption = service.get_localized(item, 'name', lang)
    kb_buttons = []
    if len(product_paths) > 1:
        kb_buttons.append([InlineKeyboardButton(text=t('photo_next', lang), callback_data=f"photo_next_{item.id}_0")])
    kb_buttons.append([
        InlineKeyboardButton(text=t('preview_add_to_cart', lang), callback_data=f"preview_add_products_{item.id}"),
        InlineKeyboardButton(text=t('preview_cancel', lang), callback_data="preview_cancel")
    ])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
    await callback.message.delete()
    await callback.message.answer_photo(photo=FSInputFile(product_paths[0]), caption=caption, reply_markup=kb, parse_mode="HTML")

async def edit_photo_page(callback: CallbackQuery, item_id: int, index: int, paths: list, lang: str, service: ShopService):
    item = await service.get_product_by_id(item_id)
    caption = service.get_localized(item, 'name', lang)
    kb_buttons = []
    if index > 0 or index < len(paths) - 1:
        row = []
        if index > 0:
            row.append(InlineKeyboardButton(text=t('photo_prev', lang), callback_data=f"photo_prev_{item_id}_{index}"))
        if index < len(paths) - 1:
            row.append(InlineKeyboardButton(text=t('photo_next', lang), callback_data=f"photo_next_{item_id}_{index}"))
        kb_buttons.append(row)
    kb_buttons.append([
        InlineKeyboardButton(text=t('preview_add_to_cart', lang), callback_data=f"preview_add_products_{item.id}"),
        InlineKeyboardButton(text=t('preview_cancel', lang), callback_data="preview_cancel")
    ])
    kb = InlineKeyboardMarkup(inline_keyboard=kb_buttons)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(paths[index])), caption=caption, reply_markup=kb)

@shops_router.callback_query(
    lambda c: c.data.startswith(
        ("cat_", "shop_", "add_", "page_", "items_done", "back_to_type",
         "delivery_", "cart_", "type_", "order_")
    )
)
async def catch_all(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    async with async_session_maker() as session:
        service = ShopService(session)
        client = await service.get_client_by_tg(callback.from_user.id)
        lang = client.language if client and client.language else 'ru'
    await show_menu_prompt(callback.from_user.id, callback.bot, lang)