import json
from pathlib import Path

DATA_FILE = Path("accepted_users.json")

def load_users():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_user(user_data):
    users = load_users()
    # Проверка на дубликаты по id
    if any(u["user_id"] == user_data["user_id"] for u in users):
        return False
    users.append(user_data)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    return True
