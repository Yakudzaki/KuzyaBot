server_dir = "C:/Games/Soft/KuzyaBot"
db_file = "C:/Games/Soft/KuzyaBot/utils/db/kuzya.db"

import sys
import logging
import handlers
import utils
import globales
from aiogram import executor, types
from loader import dp, bot
from loguru import logger
from utils.notify_admins import on_startup




sys.path.insert(1, server_dir)

logging.basicConfig(
    level=logging.INFO, 
    filename="logging0.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s"
)



if __name__ == '__main__':
    logging.info('Bot is starting!')
    logger.info('Bot is starting!')
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    logging.info('Bot shuts dowm!')
    logger.info('Bot shuts dowm!')