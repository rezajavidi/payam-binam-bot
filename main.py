from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram import F
import asyncio

from config import BOT_TOKEN
from handlers import user, message_router
from db.database import init_db

async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.SIMPLE)
    dp.include_routers(user.router, message_router.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())