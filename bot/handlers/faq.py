import logging
from html import escape
from math import ceil

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.translations import t
from bot.database.session import async_session as async_session_maker
from bot.services.faq_service import FAQService

logger = logging.getLogger(__name__)

faq_router = Router()

FAQ_PER_PAGE = 6


async def _lang(session, tg_id: int) -> str:
    return await FAQService(session).get_user_lang(tg_id)


def _page_slice(items: list, page: int):
    pages = max(1, ceil(len(items) / FAQ_PER_PAGE))
    page = max(0, min(page, pages - 1))
    start = page * FAQ_PER_PAGE
    return items[start:start + FAQ_PER_PAGE], page, pages


def _nav_row(page: int, pages: int, nav_prefix: str, lang: str) -> list:
    if pages <= 1:
        return []
    row = []
    if page > 0:
        row.append(InlineKeyboardButton(text='◀️', callback_data=f"{nav_prefix}{page - 1}"))
    row.append(InlineKeyboardButton(
        text=t('page_of', lang).format(current=page + 1, total=pages),
        callback_data='faq_noop'
    ))
    if page < pages - 1:
        row.append(InlineKeyboardButton(text='▶️', callback_data=f"{nav_prefix}{page + 1}"))
    return row


def menu_button(lang: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=t('faq_to_menu', lang), callback_data='back_to_menu')


async def render_categories(callback: types.CallbackQuery, page: int):
    async with async_session_maker() as session:
        service = FAQService(session)
        lang = await service.get_user_lang(callback.from_user.id)
        cats = await service.get_categories()
        labels = {c.id: f"{c.emoji + ' ' if c.emoji else ''}{service.localized(c, 'name', lang)}" for c in cats}

    if not cats:
        kb = InlineKeyboardMarkup(inline_keyboard=[[menu_button(lang)]])
        await callback.message.edit_text(t('faq_empty', lang), reply_markup=kb, parse_mode="HTML")
        await callback.answer()
        return

    chunk, page, pages = _page_slice(cats, page)
    rows = [
        [InlineKeyboardButton(text=labels[c.id], callback_data=f"faq_cat_{c.id}")]
        for c in chunk
    ]
    nav = _nav_row(page, pages, "faq_catpg_", lang)
    if nav:
        rows.append(nav)
    rows.append([menu_button(lang)])

    await callback.message.edit_text(
        t('faq_title', lang),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="HTML"
    )
    await callback.answer()


async def render_items(callback: types.CallbackQuery, category_id: int, page: int):
    async with async_session_maker() as session:
        service = FAQService(session)
        lang = await service.get_user_lang(callback.from_user.id)
        category = await service.get_category(category_id)
        if not category:
            await render_categories(callback, 0)
            return
        cat_name = f"{category.emoji + ' ' if category.emoji else ''}{service.localized(category, 'name', lang)}"
        items = await service.get_items(category_id)
        labels = {it.id: service.localized(it, 'question', lang) for it in items}

    if not items:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t('faq_back_categories', lang), callback_data='support')],
            [menu_button(lang)],
        ])
        await callback.message.edit_text(t('faq_no_items', lang), reply_markup=kb, parse_mode="HTML")
        await callback.answer()
        return

    chunk, page, pages = _page_slice(items, page)
    rows = [
        [InlineKeyboardButton(text=f"{labels[it.id]}", callback_data=f"faq_item_{it.id}")]
        for it in chunk
    ]
    nav = _nav_row(page, pages, f"faq_itempg_{category_id}_", lang)
    if nav:
        rows.append(nav)
    rows.append([InlineKeyboardButton(text=t('faq_back_categories', lang), callback_data='support')])
    rows.append([menu_button(lang)])

    await callback.message.edit_text(
        t('faq_category_title', lang).format(category=escape(cat_name)),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="HTML"
    )
    await callback.answer()


@faq_router.callback_query(F.data == "faq_noop")
async def faq_noop(callback: types.CallbackQuery):
    await callback.answer()


@faq_router.callback_query(F.data == "support")
async def faq_categories(callback: types.CallbackQuery):
    await render_categories(callback, 0)


@faq_router.callback_query(F.data.startswith("faq_catpg_"))
async def faq_categories_page(callback: types.CallbackQuery):
    await render_categories(callback, int(callback.data.removeprefix("faq_catpg_")))


@faq_router.callback_query(F.data.startswith("faq_cat_"))
async def faq_category_items(callback: types.CallbackQuery):
    await render_items(callback, int(callback.data.removeprefix("faq_cat_")), 0)


@faq_router.callback_query(F.data.startswith("faq_itempg_"))
async def faq_items_page(callback: types.CallbackQuery):
    payload = callback.data.removeprefix("faq_itempg_")
    category_id, page = payload.split("_", 1)
    await render_items(callback, int(category_id), int(page))


@faq_router.callback_query(F.data.startswith("faq_item_"))
async def faq_answer(callback: types.CallbackQuery):
    item_id = int(callback.data.removeprefix("faq_item_"))
    async with async_session_maker() as session:
        service = FAQService(session)
        lang = await service.get_user_lang(callback.from_user.id)
        item = await service.get_item(item_id)
        if not item:
            await render_categories(callback, 0)
            return
        question = service.localized(item, 'question', lang)
        answer = service.localized(item, 'answer', lang)
        category_id = item.category_id

    text = f"<b>{escape(question)}</b>\n\n{answer}"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t('faq_back_items', lang), callback_data=f"faq_cat_{category_id}")],
        [menu_button(lang)],
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML", disable_web_page_preview=True)
    await callback.answer()
