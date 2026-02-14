import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN
from db.database import init_db
from handlers import cancel, questions, start
from middlewares.session_timeout import SessionTimeoutMiddleware

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(cancel.router)
dp.include_router(questions.router)
dp.update.middleware(SessionTimeoutMiddleware())


async def main():
    init_db()
    print("Бот запущен 🚀")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
