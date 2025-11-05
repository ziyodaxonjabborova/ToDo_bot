from aiogram import Bot,Dispatcher

import logging
import asyncio
import os

from handler import router



dp=Dispatcher()




async def main():
    bot=Bot(token=os.getenv("TOKEN"))
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

    
    