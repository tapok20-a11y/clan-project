import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import PROFILES_DIR


def _profiles_dir() -> Path:
    path = Path(PROFILES_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_participant_profile(form_data: dict[str, Any]) -> Path:
    profile = {
        "participant": {
            "user_id": form_data["user_id"],
            "username": form_data.get("username"),
            "name": form_data["name"],
            "age": form_data["age"],
        },
        "questionnaire": {
            "hobby": form_data["hobby"],
            "birth": form_data["birth"],
            "inviter": form_data["inviter"],
        },
        "meta": {
            "status": "accepted",
            "updated_at": datetime.utcnow().isoformat(),
        },
    }

    file_path = _profiles_dir() / f"{form_data['user_id']}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(profile, file, ensure_ascii=False, indent=2)

    return file_path
