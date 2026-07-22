import asyncio
from conf import bot, dp
from handlers.commands import commands_router
from handlers.sellbuy import sellbuy_router
from aiogram.types import BotCommand
from aiogram import F
from aiogram.enums import ChatType
from handlers.sell_buy_admin import admin_sell_router
from handlers.menu_handler import common_router
from bot.database.session import scheduler
from handlers.profile import profile_router
from handlers.faq import faq_router
import os


async def set_commands(bot):
    commands = [
        BotCommand(command="menu", description="Перейти в меню / Go to menu"),
        BotCommand(command="market", description="Создать объявление / Create ad"),
    ]
    await bot.set_my_commands(commands)


async def main():
    await set_commands(bot)
    for r in (common_router, commands_router, sellbuy_router, admin_sell_router, profile_router, faq_router):
        r.message.filter(F.chat.type == ChatType.PRIVATE)
    dp.include_router(common_router)
    dp.include_router(commands_router)
    dp.include_router(sellbuy_router)
    dp.include_router(admin_sell_router)
    dp.include_router(profile_router)
    dp.include_router(faq_router)
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
