from loader import dp, bot
from data.config import ADMINS
import globales
import logging
from settings import logal_chat
from app import server_dir

async def on_startup(dp):
    for admin in ADMINS:
        await bot.send_message(admin, '✅ Бот запущен!')
    globales.init_glob()
    print('| Кузя успешно запущен!')
    logging.info('Кузя успешно запущен!')
    await bot.send_document(logal_chat, open(server_dir + f"\logging0.log", "rb"))