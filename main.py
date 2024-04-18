from aiogram import Bot, Dispatcher
import asyncio
import logging
import sys
from handlers import players_router, heroes_router, start_router, heroes_meta_router
from os import getenv


TOKEN = getenv('TOKEN')


async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_routers(start_router, heroes_meta_router, heroes_router, players_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

