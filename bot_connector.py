from aiogram.types import Message
from bot_queue_manager import add_user_to_queue, find_match_for_user, remove_user_from_queue

# برای اتصال دو کاربر ناشناس
active_chats = {}

async def try_connect_user(message: Message, user_data: dict):
    add_user_to_queue(message.from_user.id, **user_data)
    match = find_match_for_user(message.from_user.id)
    if match:
        active_chats[message.from_user.id] = match["user_id"]
        active_chats[match["user_id"]] = message.from_user.id
        remove_user_from_queue(message.from_user.id)
        remove_user_from_queue(match["user_id"])
        await message.answer("✅ اتصال برقرار شد! شما اکنون با یک کاربر ناشناس در حال گفتگو هستید.")
    else:
        await message.answer("⏳ منتظر بمانید تا کاربر مناسب پیدا شود...")

def get_partner_id(user_id: int) -> int:
    return active_chats.get(user_id)

def end_chat(user_id: int):
    partner_id = active_chats.get(user_id)
    if partner_id:
        del active_chats[user_id]
        del active_chats[partner_id]
    return partner_id
