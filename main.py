from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import logging
import asyncio
import os
from dotenv import load_dotenv

from handler import router
from database import create_table

load_dotenv()  # .env fayldan TOKEN oladi

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("❌ TOKEN is not set in .env file!")

# Bot va Dispatcher
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()
dp.include_router(router)

async def main():
    create_table()  # Jadvalni server ishga tushganda yaratadi
    logging.info("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
