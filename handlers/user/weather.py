import aiohttp
import random

from loader import dp, bot
from aiogram import types
from datetime import datetime
from ..f_lib.other import as_del_msg
from settings import time_del, kuzya_news_link
from utils.db.db_utils_warning import *


async def get_weather(city):
    code_to_smile = { 
        "Clear": "Ясно \U00002600", 
        "Clouds": "Облачно \U00002601", 
        "Rain": "Дождь \U00002614", 
        "Drizzle": "Дождь \U00002614", 
        "Thunderstorm": "Гроза \U000026A1", 
        "Snow": "Снег \U0001F328", 
        "Mist": "Туман \U0001F32B" 
    }
        
    async with aiohttp.ClientSession() as session:
        async with session.get( 
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=4d9c68ba051733b61d30fa2406658670&units=metric&lang=ru") as response:
            data = await response.json()
            
            weather_status = data["weather"][0]["main"]
        
            if weather_status in code_to_smile:
                wd = code_to_smile[weather_status]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"
            
            vis = data['visibility']
            vis = round((vis / 1000), 1)
            press = data['main']['pressure'] * 0.750064
            text = (
                f"🏙️ <b>Город</b>: <b>{data['name']}</b>\n\n"
                f"🔍 <b>Статус</b> - <em>{wd}</em>\n"
                f"🌡 Температура: <code>{data['main']['temp']}</code>\n"
                f"🤔 ️<b>Ощущается как</b>: <code>{data['main']['feels_like']} °C</code>\n\n"
                f"⏲️ <b>Давление</b>: <code>{press:.2f} мм.рт.ст</code>\n"
                f"💧 <b>Влажность</b>: <code>{data['main']['humidity']}%</code>\n"
                f"💨 <b>Скорость ветра</b>: <code>{data['wind']['speed']} м/с</code>\n"
                f"☁️ <b>Облачность</b>: <code>{data['clouds']['all']}%</code>\n\n"
                f"🔭 <b>Видимость</b>: <code>{vis} км.</code>\n\n"
                f"🌇 Восход солнца: <b>{datetime.fromtimestamp(data['sys']['sunrise'])}</b>\n"
                f"🌅 Закат солнца: <b>{datetime.fromtimestamp(data['sys']['sunset'])}</b>\n\n"
                f"Продолжительность дня: <b>{datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(data['sys']['sunrise'])}</b>\n"
                )

            if random.choice([True, False]):
                text += f"\n<a href='{kuzya_news_link}'>🗞 Канал с новостями</a>"
            return text



@dp.message_handler(commands=['погода', 'w', 'weather', 'пагода'], commands_prefix="/!.")
async def send_weather(message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    try:
        command = message.text.split()[0]
        city = message.text.replace(f'{command} ', '')
        
        if city == command:
            msg = await message.reply("<b>❌ Укажите запрос!</b>")
            await as_del_msg(message.chat.id, msg.message_id, 30)
            await as_del_msg(message.chat.id, message.message_id, 30)
            return
        
        text = await get_weather(city)

        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        msg = await bot.send_message(message.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)
    except:
        msg = await message.reply("☹ ️Не удалось найти такой город.\nПопробуйте снова.")
        await as_del_msg(message.chat.id, msg.message_id, 30)
        await as_del_msg(message.chat.id, message.message_id, 30)
        return
    
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    await as_del_msg(message.chat.id, message.message_id, time_del)
