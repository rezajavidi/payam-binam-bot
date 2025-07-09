from aiogram.types import Message
from bot_queue_manager import add_user_to_queue, find_match_for_user, remove_user_from_queue

# active_chats: user_id -> {"partner_id": int, "self_emoji": str}
active_chats = {}

async def try_connect_user(message: Message, user_data: dict):
    add_user_to_queue(message.from_user.id, **user_data)
    match = find_match_for_user(message.from_user.id)
    if match:
        uid = message.from_user.id
        oid = match["user_id"]
        ue = user_data["emoji"]
        oe = match["emoji"]
        # تنظیم نقشه گفتگو با ایموجی کاربر
        active_chats[uid] = {"partner_id": oid, "self_emoji": ue}
        active_chats[oid] = {"partner_id": uid, "self_emoji": oe}
        remove_user_from_queue(uid)
        remove_user_from_queue(oid)
        # اطلاع‌رسانی به هر دو طرف
        await message.answer(
            f"✅ اتصال برقرار شد!\n🎭 ایموجی شما: {ue}\n🎭 ایموجی طرف مقابل: {oe}\nحالا برای ارسال پیام آماده‌اید."
        )
        await message.bot.send_message(
            oid,
            f"✅ اتصال برقرار شد!\n🎭 ایموجی شما: {oe}\n🎭 ایموجی طرف مقابل: {ue}\nحالا برای ارسال پیام آماده‌اید."
        )
    else:
        await message.answer("⏳ در صف انتظار قرار گرفتید. به محض یافتن کاربر مناسب مطلع می‌شوید.")

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
