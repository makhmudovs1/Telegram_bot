import logging
from config import ADMINS

async def send_start_to_admin(dp):
    """Функция, отправляющая администраторам сообщение о запуске бота"""
    for admin in ADMINS:
        # Сразу проверяем на потенциальные ошибки
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
        except Exception as err:
            logging.exception(err)