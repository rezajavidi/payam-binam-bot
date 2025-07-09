from typing import Dict, List

waiting_users: List[Dict] = []

def add_user_to_queue(user_id: int, age: int, gender: str, city: str, target_gender: str, target_city: str, emoji: str):
    waiting_users.append({
        "user_id": user_id,
        "age": age,
        "gender": gender,
        "city": city,
        "target_gender": target_gender,
        "target_city": target_city,
        "emoji": emoji
    })

def match_filter(u, v):
    # ساده: فقط city و gender هدف را بررسی می‌کنیم
    if u["target_gender"] not in ("any", v["gender"]):
        return False
    if v["target_gender"] not in ("any", u["gender"]):
        return False
    if u["target_city"] not in ("any", v["city"]):
        return False
    if v["target_city"] not in ("any", u["city"]):
        return False
    return True

def find_match_for_user(user_id: int):
    user = next((u for u in waiting_users if u["user_id"] == user_id), None)
    if not user:
        return None
    for other in waiting_users:
        if other["user_id"] == user_id:
            continue
        if match_filter(user, other):
            return other
    return None

def remove_user_from_queue(user_id: int):
    global waiting_users
    waiting_users = [u for u in waiting_users if u["user_id"] != user_id]
