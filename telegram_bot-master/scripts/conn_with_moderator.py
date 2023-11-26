import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from create import dp

class SupportMiddleware(BaseMiddleware):
    """Класс, которыц перехватывает сообщения пользователей, находящихся в переписке"""
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Для начала достанем состояние текущего пользователя,
        # так как state: FSMContext нам сюда не прилетит
        state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)

        # Сравняем состояние пользователя
        state_str = str(await state.get_state())
        if state_str == "in_support":

            # Заберем id второго пользователя и отправим ему сообщение
            data = await state.get_data()
            second_id = data.get("second_id")
            await message.copy_to(second_id)

            # Не пропускаем дальше обработку в хендлеры
            raise CancelHandler()