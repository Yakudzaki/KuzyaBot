from loader import dp, bot
from data.config import ADMINS
import globales
import logging

async def on_startup(dp):
    for admin in ADMINS:
        await bot.send_message(admin, '✅ Бот запущен!')
    globales.init_glob()
    print('| Кузя успешно запущен!')
    logging.info('Кузя успешно запущен!')