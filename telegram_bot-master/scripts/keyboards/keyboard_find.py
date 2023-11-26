from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

support_callback = CallbackData("ask_support", "messages")

async def keyboard_find(messages):
    """Функция, которая передает клавиатуру find"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Начать поиск",
            callback_data=support_callback.new(
                messages=messages
            )
        )
    )
    return keyboard
