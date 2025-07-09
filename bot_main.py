# bot_main.py
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# روتـرهای جداگانهٔ بات
from bot_user import router as user_router          # هندلرهای مربوط به /start و ...
from bot_message_router import router as msg_router  # هندلر پیام‌ها / چت ناشناس

# ------------------------------------------------------------------
# 1) توکن را از متغیر محیطی می‌خوانیم
# ------------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ متغیر محیطی BOT_TOKEN تنظیم نشده!")

# ------------------------------------------------------------------
# 2) ساخت Bot با شیوهٔ سازگار با Aiogram 3.7
# ------------------------------------------------------------------
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # ← به‌جای پارامتر parse_mode
)

# ------------------------------------------------------------------
# 3) Dispatcher و استوریج FSM
# ------------------------------------------------------------------
dp = Dispatcher(storage=MemoryStorage())

# ثبت روتـرها
dp.include_router(user_router)
dp.include_router(msg_router)

# ------------------------------------------------------------------
# 4) تابع main برای اجرای Polling
# ------------------------------------------------------------------
async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

# ------------------------------------------------------------------
# 5) Entry-point
# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
