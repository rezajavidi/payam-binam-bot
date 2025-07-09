from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/start")
async def handle_start(msg: Message):
    await msg.answer("سلام! به پیام بی‌نام خوش اومدی.")
