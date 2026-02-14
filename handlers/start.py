from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.inline import yes_no_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(start_time=datetime.utcnow().isoformat())
    await message.answer(
        "Привет! Хотите пройти анкету для вступления в проект?",
        reply_markup=yes_no_keyboard(),
    )
