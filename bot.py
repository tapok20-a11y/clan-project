from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN
from handlers import start, questions, cancel
from middlewares.session_timeout import SessionTimeoutMiddleware
import asyncio

# Инициализация бота
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

# Подключаем роутеры
dp.include_router(start.router)
dp.include_router(questions.router)
dp.include_router(cancel.router)

# Подключаем middleware таймаута
dp.update.middleware(SessionTimeoutMiddleware())

async def main():
    print("Бот запускается... 🚀")  # Сообщение при старте
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
