import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

import bot_user
import bot_message_router

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")

logging.basicConfig(level=logging.INFO)

# توجه: در Aiogram 3.7 به بعد باید از default=DefaultBotProperties استفاده کنیم
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(bot_user.router)
dp.include_router(bot_message_router.router)
dp.message.middleware(CallbackAnswerMiddleware())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
