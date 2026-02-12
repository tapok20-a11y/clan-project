from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime

from keyboards.inline import yes_no_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(start_time=datetime.now())
    await message.answer(
        "Привет! Хотите пройти анкету для вступления в клан?",
        reply_markup=yes_no_keyboard()
    )