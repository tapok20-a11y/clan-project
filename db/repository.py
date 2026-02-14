import json
import sqlite3
from datetime import datetime
from typing import Any

from db.database import get_connection


def is_duplicate(user_id: int, birth_date: str, full_name: str) -> bool:
    with get_connection() as conn:
        by_id = conn.execute(
            "SELECT 1 FROM accepted_forms WHERE user_id = ? LIMIT 1", (user_id,)
        ).fetchone()
        if by_id:
            return True

        by_identity = conn.execute(
            """
            SELECT 1
            FROM accepted_forms
            WHERE lower(full_name) = lower(?) AND birth_date = ?
            LIMIT 1
            """,
            (full_name.strip(), birth_date.strip()),
        ).fetchone()
        return by_identity is not None


def save_accepted_form(data: dict[str, Any]) -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO accepted_forms (
                    user_id, username, full_name, age, hobby, birth_date, inviter, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["user_id"],
                    data.get("username"),
                    data["name"],
                    data["age"],
                    data["hobby"],
                    data["birth"],
                    data["inviter"],
                    datetime.utcnow().isoformat(),
                ),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def save_draft(user_id: int, username: str | None, data: dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO draft_forms (user_id, username, data_json, cancelled_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, username, json.dumps(data, ensure_ascii=False), datetime.utcnow().isoformat()),
        )


def get_accepted_forms() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT user_id, username, full_name, age, hobby, birth_date, inviter, created_at
            FROM accepted_forms
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def get_total_accepted() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM accepted_forms").fetchone()
    return int(row["cnt"])
