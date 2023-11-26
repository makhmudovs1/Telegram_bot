from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from keyboards.keyboard_moderator import support_keyboard
from create import dp, bot
from keyboards.keyboard_moderator import support_callback

@dp.message_handler(Command("support"))
async def ask_support(message: types.Message):
    """Сообщение отправки одного сообщения модератору"""
    text = "Хотите написать сообщение модератору? Нажмите на кнопку ниже!"
    # messages - параметр, который определяет, будет ли вестись диалог между пользователем и модератором
    # или будет обмен одним сообщением
    keyboard = await support_keyboard(messages="one")
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="one"))
# Декоратор оборачивает функцию, когда нажимается кнопка с отправкой одного сообщения модератору
async def click_on_the_button(call, state, callback_data):
    """Функция, которая обрабатывает нажатие на кнопку отправки сообщения"""
    user_id = int(callback_data.get("user_id"))
    # останавливаем видимость обработки действия
    await call.answer()
    await call.message.answer("Пришлите ваше сообщение, которым вы хотите поделиться")
    # Записываем в состояние пользователя, которому будет отправляться сообщение
    await state.set_state("write_message")
    await state.update_data(second_id=user_id)


@dp.message_handler(state="write_message")
# Декоратор оборачивает функцию, когда машина состояний находится в статусе "write_message"
# То есть события будут происходить в тот момент, когда пользователь напишет нужное сообщения, после нажатия кнопки
async def get_support_message(message, state):
    # Узнаем кому передавать сообщение
    data = await state.get_data()
    second_id = data.get("second_id")
    keyboard = await support_keyboard(messages="one", user_id=message.from_user.id)

    # Передаем пользователю/модератору, что все хорошо
    await message.answer("Вы отправили это сообщение!")
    # Передаем данные модератору/пользователю
    await bot.send_message(second_id, f"Вам письмо! Ваш собеседник сказал:")
    await message.copy_to(second_id, reply_markup=keyboard)
    await state.reset_state()