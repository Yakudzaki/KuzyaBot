import re
import aiohttp
from aiogram import types
from loader import bot, dp
from settings import botik_id


async def get_video(link: str, chat_id: int) -> str:
    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

    payload = {
        "url": link,
        "hd": "1"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "b1b83ddcf4msheb310e444c2450ep1ebd82jsnf111d01eea9f",
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            data = await response.json()
            return data["data"]["hdplay"]


async def send_video(message: types.Message) -> None:
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        try:
            video_link = await get_video(message.text, message.chat.id)
            await bot.send_chat_action(message.chat.id, 'upload_video')
            await message.reply_video(video_link, caption=f"✅ Скачано с помощью <a href='tg://user?id={botik_id}'>Кузи</a>\n\n")
        except Exception as e:
            await message.reply("😢 Не удалось скачать видео!")
            return
    return