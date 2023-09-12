import os, re, configparser, requests
import urllib
from aiogram import Bot, types
from loader import dp, bot
import os, logging, aioschedule, asyncio
from app import server_dir

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .tiktok import getCookie, getDownloadUrl, getDownloadID, getStatus
import urllib.request

 
def download_video(video_url, name):
    r = requests.get(video_url, allow_redirects=True)
    content_type = r.headers.get('content-type')
    if content_type == 'video/mp4':
        open(f'./videos/video{name}.mp4', 'wb').write(r.content)
    else:
        pass
 
@dp.message_handler(content_types=['text'])
async def tiktok(message: types.Message):
    if not os.path.exists('videos'):
        os.makedirs('videos')
    
    if message.text.startswith('https://www.tiktok.com'):
        video_url = message.text
        cookie = getCookie()
        status = getStatus(video_url,cookie)
        if status == False:
            await bot.send_message(chat_id=message.chat.id, text='Неверная ссылка, видео было удалено или я его не нашел.')
            return True
        else:
            await bot.send_message(chat_id=message.chat.id, text='Скачиваю видео')
            url = getDownloadUrl(video_url, cookie)
            video_id = getDownloadID(video_url, cookie)
            download_video(url, video_id)
            path = f'./videos/video{video_id}.mp4'
            with open(f'./videos/video{video_id}.mp4', 'rb') as file:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=file,
                    caption='Держи видео🚀 '
                    )
            os.remove(path)
            return True
    elif message.text.startswith('https://vm.tiktok.com'):
        video_url = message.text
        req = urllib.request.Request(
            video_url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
            }
                    )
        url_v = urllib.request.urlopen(req).geturl()
        if url_v == 'https://www.tiktok.com/':
            await bot.send_message(chat_id=message.chat.id, text='Неверная ссылка, видео было удалено или я его не нашел.')
            return True
        else:
            cookie = getCookie()
            await bot.send_message(chat_id=message.chat.id, text='Скачиваю видео\nЖди⚡️')
            url = getDownloadUrl(url_v, cookie)
            video_id = getDownloadID(url_v, cookie)
            download_video(url, video_id)
            path = f'./videos/video{video_id}.mp4'
            with open(f'./videos/video{video_id}.mp4', 'rb') as file:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=file,
                    caption='Держи видео🚀'
                    )
            os.remove(path)
            return True

    return
