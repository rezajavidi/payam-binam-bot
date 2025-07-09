from aiogram.types import Message
from bot_queue_manager import add_user_to_queue, find_match_for_user, remove_user_from_queue

active_chats = {}

async def try_connect_user(message: Message, user_data: dict):
    add_user_to_queue(message.from_user.id, **user_data)
    match = find_match_for_user(message.from_user.id)
    if match:
        active_chats[message.from_user.id] = match["user_id"]
        active_chats[match["user_id"]] = message.from_user.id
        remove_user_from_queue(message.from_user.id)
        remove_user_from_queue(match["user_id"])
        await message.answer("✅ اتصال برقرار شد! می‌توانید پیام بفرستید.")
        await message.bot.send_message(match["user_id"], "✅ شما با یک کاربر ناشناس متصل شدید، گفتگو کنید!")
    else:
        await message.answer("⏳ در صف انتظار قرار گرفتید. به محض یافتن کاربر مناسب مطلع می‌شوید.")

def get_partner_id(user_id: int):
    return active_chats.get(user_id)

def end_chat(user_id: int):
    partner_id = active_chats.pop(user_id, None)
    if partner_id:
        active_chats.pop(partner_id, None)
    return partner_id