from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from datetime import datetime, timedelta
from config import SESSION_TIMEOUT

class SessionTimeoutMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state = data.get("state")
        if state:
            data_time = await state.get_data()
            start_time = data_time.get("start_time")
            if start_time:
                if datetime.now() - start_time > SESSION_TIMEOUT:
                    await state.finish()
        return await handler(event, data)
