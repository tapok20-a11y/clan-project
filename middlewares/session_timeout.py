from datetime import datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware

from config import SESSION_TIMEOUT
from db import repository


class SessionTimeoutMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        state = data.get("state")
        if state:
            state_data = await state.get_data()
            raw_start = state_data.get("start_time")
            if raw_start:
                try:
                    started_at = datetime.fromisoformat(raw_start)
                except ValueError:
                    started_at = None

                if started_at and datetime.utcnow() - started_at > SESSION_TIMEOUT:
                    user = getattr(event, "from_user", None)
                    if state_data:
                        repository.save_draft(
                            user_id=user.id if user else 0,
                            username=user.username if user else None,
                            data=state_data,
                        )
                    await state.clear()
        return await handler(event, data)
