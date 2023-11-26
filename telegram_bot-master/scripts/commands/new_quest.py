from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from sql.sql_handling import SQL
from keyword_search.search import search_message
from keyword_search.parsing import parsing

from create import dp, bot
import os

class Test(StatesGroup):
    add_quest = State()
    add_answ = State()
    add_img_step_1 = State()
    add_img_step_2 = State()


@dp.message_handler(Command("new_quest"), state=None)
async def enter_add(message: types.Message):
    await message.answer("Введите вопрос")
    await Test.add_quest.set()


@dp.message_handler(state=Test.add_quest)
async def add_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(quest=answer)
    await message.answer("Введите ответ на вопрос")
    await Test.next()

@dp.message_handler(state=Test.add_answ)
async def add_answ(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer=answer)
    await message.answer("Происходит процесс обработки ключевых слов.Не переживайте, если он займет некоторое время.\n"
                         "Хотите ли добавить изображение?\nНапишите - 'нет', если это не так, иначе - 'да'.")
    await Test.next()

@dp.message_handler(state=Test.add_img_step_1)
async def add_im_1(message: types.Message, state: FSMContext):
    # Достаем переменные
    data = await state.get_data()
    quest = data.get("quest")
    answ = data.get("answer")
    text = message.text
    par = parsing()

    key_word = await search_message(quest)
    key_word_with_syn = []
    for word in key_word:
        key_word_with_syn.append(word)
        dop = par.go_syn(word)
        for dop_word in dop:
            key_word_with_syn.append(dop_word)

    sql = SQL("sql/faq.db")
    sql.add_question(quest, answ)

    for word in key_word_with_syn:
        if not sql.find_key_word(word):
            sql.add_keys(word, sql.get_number(quest)[0])
        else:
            sql.update_number(word, sql.get_number(quest)[0])
    sql.close()

    if text == "нет":
        await state.finish()
        await message.answer("Спасибо за проделанную работу!")
    else:
        await Test.next()
        await message.answer("Отправьте изображение")

@dp.message_handler(content_types=['photo'], state=Test.add_img_step_2)
async def add_im_2(message: types.Message, state: FSMContext):
    """Добавление изображения в бд"""
    await message.photo[-1].download('photo_d.jpg')
    data = await state.get_data()

    #Добавляем изображение в базу данных
    sql = SQL("sql/faq.db")
    sql.insert_blob('photo_d.jpg', sql.get_number(data.get("quest"))[0])
    sql.close()

    os.remove("photo_d.jpg")
    await message.answer("Спасибо за проделанную работу!")
    await state.finish()

