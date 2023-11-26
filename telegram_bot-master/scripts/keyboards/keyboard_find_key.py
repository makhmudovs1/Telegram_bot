from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram import types
keyboard_find_key_s = CallbackData("ask_support", "messages", "answer")

async def keyboard_find_key(messages, count, list_answer):
    """Функция, которая передает клавиатуру find"""
    keyboard = InlineKeyboardMarkup()
    for i in range(count//3+1):
        buttons = []
        for j in range(3):
            if i*3 + j <= count-1:
                buttons.append(types.InlineKeyboardButton(text=str(i*3 + j + 1), callback_data=keyboard_find_key_s.new(messages=messages,answer=list_answer[i*3 + j])))
        keyboard.add(*buttons)
    return keyboard