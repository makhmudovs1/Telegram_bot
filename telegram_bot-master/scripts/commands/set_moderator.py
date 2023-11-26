from aiogram import types

async def set_default_commands(dp):
    """Функция, отвечающая за вывод команд-подсказок"""
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("find", "Найти похожий вопрос"),
        types.BotCommand("support", "Написать сообщение (одно) модератору"),
        types.BotCommand("support_call", "Пообщаться с модератором (переписка)"),
        types.BotCommand("help", "Помощь"),
    ])