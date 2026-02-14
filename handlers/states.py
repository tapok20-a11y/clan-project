from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    age = State()
    hobby = State()
    birth = State()
    inviter = State()
