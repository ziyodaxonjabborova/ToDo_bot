from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
import logging
import asyncio
import os

from handler import router
from database import create_table

TOKEN = os.getenv("TOKEN")  # ✅ Tokenni serverdagi env variable orqali olamiz

# 🔹 Jadvalni yaratish
create_table()

dp = Dispatcher()

async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")  # ✅ parse_mode HTML bu yerda
    )
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
