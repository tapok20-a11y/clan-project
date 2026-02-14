from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from datetime import datetime

from config import CHAT_LINKS, FORM_LINK, MAX_AGE
from db import repository
from handlers.states import Form
from keyboards.inline import cancel_keyboard
from utils import logger, validators
from utils.profiles import save_participant_profile

router = Router()


@router.callback_query(F.data == "yes")
async def start_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ваше имя:")
    await callback.message.answer("Можно прервать анкету кнопкой ниже:", reply_markup=cancel_keyboard())
    await state.update_data(start_time=datetime.utcnow().isoformat())
    await state.set_state(Form.name)
    await callback.answer()


@router.callback_query(F.data == "no")
async def reject_form(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Хорошо, если передумаете — нажмите /start 🙂")
    await callback.answer()


@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    if (message.text or "").startswith("/"):
        return
    if not validators.valid_name(message.text or ""):
        await message.answer("Имя должно быть осмысленным и не короче 2 символов.")
        return

    await state.update_data(name=message.text.strip())
    await message.answer("Введите ваш возраст:", reply_markup=cancel_keyboard())
    await state.set_state(Form.age)


@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    if (message.text or "").startswith("/"):
        return
    age_text = (message.text or "").strip()
    if not validators.valid_age(age_text):
        await message.answer("Возраст должен быть числом от 1 до 119.")
        return

    age = int(age_text)
    if age > MAX_AGE:
        await message.answer("Ваша анкета отклонена ❌")
        await state.clear()
        return

    await state.update_data(age=age)
    await message.answer("Расскажите кратко о себе / чем увлекаетесь:", reply_markup=cancel_keyboard())
    await state.set_state(Form.hobby)


@router.message(Form.hobby)
async def process_hobby(message: Message, state: FSMContext):
    if (message.text or "").startswith("/"):
        return
    if not validators.valid_nonempty(message.text or "", min_len=3):
        await message.answer("Ответ должен быть осмысленным (минимум 3 символа).")
        return

    await state.update_data(hobby=message.text.strip())
    await message.answer("Введите дату и месяц рождения (например 12.05):", reply_markup=cancel_keyboard())
    await state.set_state(Form.birth)


@router.message(Form.birth)
async def process_birth(message: Message, state: FSMContext):
    if (message.text or "").startswith("/"):
        return
    birth = (message.text or "").strip()
    if not validators.valid_birth_date(birth):
        await message.answer("Формат неверный. Используйте ДД.ММ, например 12.05")
        return

    await state.update_data(birth=birth)
    await message.answer("Кто пригласил вас в проект?", reply_markup=cancel_keyboard())
    await state.set_state(Form.inviter)


@router.message(Form.inviter)
async def process_inviter(message: Message, state: FSMContext):
    if (message.text or "").startswith("/"):
        return
    inviter = (message.text or "").strip()
    if not validators.valid_nonempty(inviter):
        await message.answer("Укажите, кто пригласил вас в проект.")
        return

    await state.update_data(inviter=inviter)
    data = await state.get_data()

    user_data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "name": data["name"],
        "age": data["age"],
        "hobby": data["hobby"],
        "birth": data["birth"],
        "inviter": data["inviter"],
    }

    duplicate = repository.is_duplicate(
        user_id=user_data["user_id"],
        birth_date=user_data["birth"],
        full_name=user_data["name"],
    )
    if duplicate:
        await message.answer("Похоже, такая анкета уже есть (дубликат).")
        await state.clear()
        return

    saved = repository.save_accepted_form(user_data)
    if not saved:
        await message.answer("Похоже, такая анкета уже есть (дубликат).")
        await state.clear()
        return

    logger.log_accepted(user_data)
    save_participant_profile(user_data)

    chat_links = "\n".join(CHAT_LINKS)
    await message.answer(
        "Вы приняты ✅\n\n"
        "Ссылки на чаты:\n"
        f"{chat_links}\n\n"
        f"Форма: {FORM_LINK}"
    )
    await state.clear()
