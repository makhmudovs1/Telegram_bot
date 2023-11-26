from aiogram import executor

from commands.set_moderator import set_default_commands
from send_to_admin import send_start_to_admin
from conn_with_moderator import SupportMiddleware

async def on_startup(dp):
    # Уведомляет про запуск
    await set_default_commands(dp)
    await send_start_to_admin(dp)


if __name__ == '__main__':
    # Передаем значение Dispatcher со всеми используемыми функциями
    from commands.handlers import dp

    dp.middleware.setup(SupportMiddleware())
    executor.start_polling(dp, on_startup=on_startup)
