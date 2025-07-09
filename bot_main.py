from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from db.database import add_user_to_db

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user
    add_user_to_db(user.id, user.first_name, user.username)
    await message.answer("🎉 خوش اومدی به پیام بینام!")

if __name__ == "__main__":
    import asyncio
    from aiogram import executor
    from handlers import message_router
    dp.include_router(message_router.router)
    executor.start_polling(dp, skip_updates=True)
