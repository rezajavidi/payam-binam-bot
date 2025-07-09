from typing import Dict, Optional

# ساختار صف انتظار بر اساس جنسیت و شهر و سن
waiting_users = []

def add_user_to_queue(user_id: int, age: int, gender: str, city: str, target_gender: str, target_city: str) -> None:
    user_data = {
        "user_id": user_id,
        "age": age,
        "gender": gender,
        "city": city,
        "target_gender": target_gender,
        "target_city": target_city
    }
    waiting_users.append(user_data)

def find_match_for_user(user_id: int) -> Optional[Dict]:
    for user in waiting_users:
        if user["user_id"] != user_id:
            return user
    return None

def remove_user_from_queue(user_id: int):
    global waiting_users
    waiting_users = [u for u in waiting_users if u["user_id"] != user_id]
