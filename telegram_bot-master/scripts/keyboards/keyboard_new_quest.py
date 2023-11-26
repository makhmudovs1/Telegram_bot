from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

support_callback = CallbackData("ask_support", "messages")

async def keyboard_new(messages):
    """Функция, которая передает клавиатуру new quest"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Начать добавление нового вопроса",
            callback_data=support_callback.new(
                messages=messages
            )
        )
    )
    return keyboard