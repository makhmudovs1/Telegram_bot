import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from create import dp
from config import support_ids

# Параметры кнопок: 1 - префикс (имя), 2.. - функциональные: то, что мы хотим сохранить о наших кнопках
# messages - параметр, который определяет, будет ли вестись диалог между пользователем и модератором
# или будет обмен одним сообщением
# as_user определяет, кто нажал данную кнопку: модератор или пользователь
support_callback = CallbackData("ask_support", "messages", "user_id", "as_user")
cancel_support_callback = CallbackData("cancel_support", "user_id")

async def support_keyboard(messages, user_id = None):
    """Функция, которая передает нужную клавиатуру"""
    if user_id:
        # Если указан user_id, то данная клавиатура передается модератору
        contact_id = int(user_id)
        text = "Ответить"
        as_user = "no"
    else:
        # Данная клавиатура передается пользователю
        as_user = "yes"
        contact_id = await get_support_moderator()

        if messages == "one":
            text = "Написать 1 сообщение модератору"
            contact_id = random.choice(support_ids)
        else:
            if not contact_id:
                # Если не нашли свободного оператора - выходим и говорим, что его нет
                return False
            text = "Начать диалог с модератором"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            # В инлайн-кнопках важно передавать callback_data или другой дополнительный параметр
            # Если передавать просто текст работать не будет
            callback_data=support_callback.new(
                messages=messages,
                user_id=contact_id,
                as_user=as_user
            )
        )
    )
    #print(contact_id)
    return keyboard

async def check_state_moderator(support_id):
    """Функция, проверяющая занятость модератора"""
    # Узнаем статус модератора
    state = dp.current_state(chat=support_id, user=support_id)
    state_str = str(await state.get_state())
    if state_str == "in_support":
        return False
    else:
        return True

async def get_support_moderator():
    """Функция, возвращающая рандомного модератора"""
    # Перемешиваем массив id модераторов
    random.shuffle(support_ids)
    for id in support_ids:
        # Проверим если модератор в данное время не занят
        if await check_state_moderator(id):
            return id
    return False

def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить сеанс",
                    callback_data=cancel_support_callback.new(
                        user_id=user_id
                    )
                )
            ]
        ]
    )