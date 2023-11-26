from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.keyboard_moderator import support_keyboard, support_callback, check_state_moderator, get_support_moderator, \
    cancel_support, cancel_support_callback
from create import dp, bot


@dp.message_handler(Command("support_call"))
async def ask_support_call(message):
    text = "Хотите начать диалог с модератором? Нажмите на кнопку ниже!"
    keyboard = await support_keyboard(messages="many")
    if not keyboard:
        await message.answer("К сожалению, сейчас нет свободных модераторов. Попробуйте позже.")
        return
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="yes"))
async def send_to_support_call(call, state, callback_data):
    """Функция, отвечающая за обработку событий после нажатия пользователем кнопки support_call и поддвержения действия"""
    await call.message.edit_text("Вы начали диалог с модератором. Ждем ответа!")
    user_id = int(callback_data.get("user_id"))

    if not await check_state_moderator(user_id):
        # Проверяем готов (свободен) ли модератор к переписке
        support_id = await get_support_moderator()
    else:
        support_id = user_id

    if not support_id:
        # Обрабатываем ситуацию, если все модераторы заняты
        await call.message.edit_text("К сожалению, сейчас нет свободных модераторов. Попробуйте позже.")
        await state.reset_state()
        return False

    # Если все хорошо, то переводим пользователя в состояние ожидания модератора
    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    # Создаем клавиатуру для модератора
    keyboard = await support_keyboard(messages="many", user_id=call.from_user.id)

    await bot.send_message(support_id,
                           f"С вами хочет связаться пользователь {call.from_user.full_name}",
                           reply_markup=keyboard
                           )


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="no"))
async def answer_support_call(call, state, callback_data):
    """Обработка событий после того, как модератору пришло сообщение о начале диалога"""
    # Получаем состояние пользователя, который хочет связаться с модератором
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != "wait_in_support":
        await call.message.edit_text("К сожалению, пользователь уже передумал.")
        return

    # Если и пользователь и модератор готовы, переводим их в состояние общения
    await state.set_state("in_support")
    await user_state.set_state("in_support")

    # В данных модератора сохранием id пользователя
    await state.update_data(second_id=second_id)

    # Создаем клавиатуры для отмены общения для модератора и пользователя
    keyboard = cancel_support(second_id)
    keyboard_second_user = cancel_support(call.from_user.id)

    await call.message.edit_text("Вы на связи с пользователем!\n"
                                 "Чтобы завершить общение нажмите на кнопку.",
                                 reply_markup=keyboard
                                 )
    await bot.send_message(second_id,
                           "Модератор на связи! Можете писать сюда свое сообщение. \n"
                           "Чтобы завершить общение нажмите на кнопку.",
                           reply_markup=keyboard_second_user
                           )


@dp.callback_query_handler(cancel_support_callback.filter(), state=["in_support", "wait_in_support", None])
async def exit_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    """Функция завершения сеанса"""
    user_id = int(callback_data.get("user_id"))
    # По первому пользователю узнаем состояние другого
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id:
            # Проверка на случай, если пользователь уже с кем-то общается
            await second_state.reset_state()
            await bot.send_message(user_id, "Пользователь завершил сеанс техподдержки")

    await call.message.edit_text("Вы завершили сеанс")
    await state.reset_state()

@dp.message_handler(state="wait_in_support", content_types=types.ContentTypes.ANY)
async def not_supported(message, state):
    """Обработка событий, если пользователь начинает писать раньше, чем связался с модератором"""
    data = await state.get_data()
    second_id = data.get("second_id")

    keyboard = cancel_support(second_id)
    await message.answer("Дождитесь ответа модератора или отмените сеанс", reply_markup=keyboard)