from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def yes_no_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("Да ✅", callback_data="yes"),
        InlineKeyboardButton("Нет ❌", callback_data="no")
    )
    return kb

def cancel_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("Отмена ❌", callback_data="cancel"))
    return kb