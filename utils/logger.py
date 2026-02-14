import json
from datetime import datetime

from config import LOG_FILE



def log_accepted(data: dict) -> None:
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": data["user_id"],
        "username": data.get("username"),
        "name": data["name"],
        "age": data["age"],
        "birth": data["birth"],
        "inviter": data["inviter"],
    }
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(payload, ensure_ascii=False) + "\n")
