from aiogram import Router, F
from aiogram.types import Message
from bot_connector import get_partner_id, get_self_emoji, end_chat
from database import add_message

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
        # ذخیره پیام در پایگاه داده
        add_message(sender_id=msg.from_user.id, receiver_id=partner_id, text=msg.text)
        # ارسال با پیشوند ایموجی
        emoji = get_self_emoji(msg.from_user.id)
        await msg.bot.send_message(partner_id, f"{emoji} گفت: {msg.text}")
    else:
        await msg.answer("⏳ هنوز به کسی متصل نشده‌ای. لطفا کمی صبر کن!")
