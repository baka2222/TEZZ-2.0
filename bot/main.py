import asyncio
from conf import bot, dp
from handlers.commands import commands_router
from handlers.sellbuy import sellbuy_router
from handlers.shops import shops_router
from aiogram.types import BotCommand
from handlers.delivery import router as delivery_router
from handlers.sell_buy_admin import admin_sell_router
from handlers.menu_handler import common_router
from handlers.pin_handler import pin_router
from bot.database.session import scheduler
from handlers.pin_handler import pin_router, AlbumMiddleware
from handlers.subscription_handler import subscription_router
from handlers.delete_ad_handler import delete_ad_router
from handlers.edit_ad_handler import edit_router
import os


async def set_commands(bot):
    commands = [
        BotCommand(command="menu", description="Перейти в меню / Go to menu"),
        BotCommand(command="market", description="Создать объявление / Create ad"),
    ]
    await bot.set_my_commands(commands)


async def main():
    await set_commands(bot)
    dp.message.outer_middleware(AlbumMiddleware(latency=0.5))
    dp.include_router(common_router)
    dp.include_router(delete_ad_router)
    dp.include_router(edit_router)
    dp.include_router(pin_router)
    dp.include_router(subscription_router)    
    dp.include_router(delivery_router)
    dp.include_router(commands_router)
    dp.include_router(sellbuy_router)
    dp.include_router(shops_router)
    dp.include_router(admin_sell_router)
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
