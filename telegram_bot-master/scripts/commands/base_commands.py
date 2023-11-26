
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from create import dp, bot

@dp.message_handler(CommandHelp())
async def bot_help(message):
    """Базовая команда \help, дающая краткую сводку о боте"""
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/support - Написать сообщение (одно) модератору",
            "/support_call - Пообщаться с модератором (переписка)",
            "/help - Получить справку")

    await message.answer("\n".join(text))

@dp.message_handler(CommandStart())
async def bot_start(message):
    """Базовая команда начала общения с пользователем: приветствие"""
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await bot.send_sticker(chat_id=message.from_user.id,
                     sticker=r"CAACAgIAAxkBAAEFGHNiskY51VxAZge3B8ZMf31aOcN4TQAChwIAAladvQpC7XQrQFfQkCkE")