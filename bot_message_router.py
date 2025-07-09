from aiogram import Router, F
from aiogram.types import Message
from bot_connector import get_partner_id, end_chat

router = Router()

@router.message(F.text == "/end")
async def end_chat_cmd(msg: Message):
    partner_id = end_chat(msg.from_user.id)
    if partner_id:
        await msg.answer("✅ گفتگو پایان یافت.")
        await msg.bot.send_message(partner_id, "⛔️ طرف مقابل گفتگو را پایان داد.")
    else:
        await msg.answer("شما در حال حاضر در گفتگویی نیستید.")

@router.message(F.text)
async def relay(msg: Message):
    partner_id = get_partner_id(msg.from_user.id)
    if partner_id:
        await msg.bot.send_message(partner_id, msg.text)
    else:
        await msg.answer("⏳ هنوز به کسی متصل نشده‌ای. لطفا کمی صبر کن!")