from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp_socks import SocksConnector
from data import config
import asyncio


# PROXY_URL = 'socks5://127.0.0.1:9050'  #адрес локального тор (у меня запущен как служба)
storage = MemoryStorage()
# bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML, proxy=PROXY_URL) #, proxy=PROXY_URL — прокси
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

#pip install aiohttp_socks - Нужно установить для работы сокс тора.