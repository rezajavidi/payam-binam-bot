from aiogram.types import Message
from database import add_message

# active_chats: user_id -> {"partner_id": int, "self_emoji": str}
active_chats = {}

async def direct_connect_user(message: Message, emoji: str, target_id: int):
    uid = message.from_user.id
    oid = target_id
    # assign active chat
    active_chats[uid] = {"partner_id": oid, "self_emoji": emoji}
    active_chats[oid] = {"partner_id": uid, "self_emoji": ""}
    # notify participants
    await message.answer("✅ اتصال برقرار شد! اکنون می‌توانید پیام ارسال کنید.")
    await message.bot.send_message(oid, "🔔 پیام ناشناس جدید در دسترس است!")

def get_partner_id(user_id: int):
    info = active_chats.get(user_id)
    return info["partner_id"] if info else None

def get_self_emoji(user_id: int):
    info = active_chats.get(user_id)
    return info["self_emoji"] if info else ""

def end_chat(user_id: int):
    partner_info = active_chats.pop(user_id, None)
    if partner_info:
        partner_id = partner_info["partner_id"]
        active_chats.pop(partner_id, None)
        return partner_id
    return None
