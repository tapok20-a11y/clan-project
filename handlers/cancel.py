from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db import repository

router = Router()


async def _save_and_cancel(state: FSMContext, user_id: int, username: str | None) -> bool:
    data = await state.get_data()
    current_state = await state.get_state()
    if data or current_state:
        repository.save_draft(user_id=user_id, username=username, data=data)
        await state.clear()
        return True
    return False


@router.callback_query(F.data == "cancel")
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    cancelled = await _save_and_cancel(state, callback.from_user.id, callback.from_user.username)
    if cancelled:
        await callback.message.edit_text("Анкета отменена. Черновик сохранён 📝")
    else:
        await callback.message.edit_text("Нет активной анкеты для отмены.")
    await callback.answer()


@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    cancelled = await _save_and_cancel(state, message.from_user.id, message.from_user.username)
    if cancelled:
        await message.answer("Анкета отменена. Черновик сохранён 📝")
    else:
        await message.answer("Сейчас нет активной анкеты.")
