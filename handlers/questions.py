from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.inline import cancel_keyboard
from utils import validators, storage
from config import MAX_AGE, CHAT_LINKS, FORM_LINK

router = Router()

class Form(StatesGroup):
    name = State()
    age = State()
    hobby = State()
    birth = State()
    inviter = State()


# Нажали "Да"
@router.callback_query(F.data == "yes")
async def start_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ваше имя:")
    await callback.message.answer("Вы можете отменить анкету:", reply_markup=cancel_keyboard())
    await state.set_state(Form.name)
    await callback.answer()


# Имя
@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    if not validators.valid_name(message.text):
        await message.answer("Имя слишком короткое (минимум 2 символа). Попробуйте снова.")
        return

    await state.update_data(name=message.text)
    await message.answer("Введите ваш возраст:", reply_markup=cancel_keyboard())
    await state.set_state(Form.age)


# Возраст
@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом.")
        return

    age = int(message.text)

    if age > MAX_AGE:
        await message.answer("Ваша анкета отклонена ❌")
        await state.clear()
        return

    await state.update_data(age=age)
    await message.answer("Ваше хобби / чем увлекаетесь?", reply_markup=cancel_keyboard())
    await state.set_state(Form.hobby)


# Хобби
@router.message(Form.hobby)
async def process_hobby(message: Message, state: FSMContext):
    if not validators.valid_nonempty(message.text):
        await message.answer("Ответ не может быть пустым.")
        return

    await state.update_data(hobby=message.text)
    await message.answer("Введите дату и месяц рождения (например 12.05):", reply_markup=cancel_keyboard())
    await state.set_state(Form.birth)


# Дата рождения
@router.message(Form.birth)
async def process_birth(message: Message, state: FSMContext):
    if not validators.valid_nonempty(message.text):
        await message.answer("Дата не может быть пустой.")
        return

    await state.update_data(birth=message.text)
    await message.answer("Кто пригласил вас в проект?", reply_markup=cancel_keyboard())
    await state.set_state(Form.inviter)


# Кто пригласил
@router.message(Form.inviter)
async def process_inviter(message: Message, state: FSMContext):
    if not validators.valid_nonempty(message.text):
        await message.answer("Ответ не может быть пустым.")
        return

    await state.update_data(inviter=message.text)

    data = await state.get_data()

    user_data = {
        "user_id": message.from_user.id,
        "name": data["name"],
        "age": data["age"],
        "hobby": data["hobby"],
        "birth": data["birth"],
        "inviter": data["inviter"]
    }

    saved = storage.save_user(user_data)

    if saved:
        await message.answer(
            "Вы приняты ✅\n\n"
            "Ссылки на чаты:\n"
            + "\n".join(CHAT_LINKS)
            + f"\n\nФорма: {FORM_LINK}"
        )
    else:
        await message.answer("Вы уже проходили анкету.")

    await state.clear()