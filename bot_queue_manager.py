from typing import Dict, Optional, List

waiting_users: List[Dict] = []

def add_user_to_queue(user_id: int, age: int, gender: str, city: str, target_gender: str, target_city: str):
    waiting_users.append({
        "user_id": user_id,
        "age": age,
        "gender": gender,
        "city": city,
        "target_gender": target_gender,
        "target_city": target_city
    })

def match_filter(u, v):
    # ساده: فقط city و gender هدف را بررسی می‌کنیم
    city_ok = (u["target_city"] == "any" or v["city"] == u["target_city"])                       and (v["target_city"] == "any" or u["city"] == v["target_city"])
    gender_ok = (u["target_gender"] == "any" or v["gender"] == u["target_gender"])                         and (v["target_gender"] == "any" or u["gender"] == v["target_gender"])
    return city_ok and gender_ok

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