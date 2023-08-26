from loader import dp, bot
from aiogram import types
import requests
from datetime import datetime
from ..f_lib.other import as_del_msg
from settings import time_del
from utils.db.db_utils_warning import *



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
            await message.reply("<b>❌ Укажите запрос!</b>")
            return
        
        code_to_smile = { 
        "Clear": "Ясно \U00002600", 
        "Clouds": "Облачно \U00002601", 
        "Rain": "Дождь \U00002614", 
        "Drizzle": "Дождь \U00002614", 
        "Thunderstorm": "Гроза \U000026A1", 
        "Snow": "Снег \U0001F328", 
        "Mist": "Туман \U0001F32B" 
    }
        
        r = requests.get( 
            f"http://api.openweathermap.org/data/2.5/weather?q={promptt}&appid=4d9c68ba051733b61d30fa2406658670&units=metric&lang=ru")
        data = r.json()
        
        weather_status = data["weather"][0]["main"]

        
        if weather_status in code_to_smile:
        	wd = code_to_smile[weather_status]
        else:
        	wd = "Посмотри в окно, не пойму что там за погода!"
        
        
        text = (
            f"🏙️ <b>Город</b>: <b>{data['name']}</b>\n\n"
            f"🔍 <b>Статус</b> - <em>{wd}</em>\n"
            f"🌡 Температура: <code>{data['main']['temp']}</code>\n"
            f"🤔 ️<b>Ощущается как</b>: <code>{data['main']['feels_like']} °C</code>\n\n"
            f"⏲️ <b>Давление</b>: <code>{data['main']['pressure']} мм.рт.ст</code>\n"
            f"💧 <b>Влажность</b>: <code>{data['main']['humidity']}%</code>\n"
            f"💨 <b>Скорость ветра</b>: <code>{data['wind']['speed']} м/с</code>\n"
            f"☁️ <b>Облачность</b>: <code>{data['main']['clouds']}%</code>\n\n"
            f"🌇Восход солнца: <b>{datetime.fromtimestamp(data['sys']['sunrise'])}</b>\n🌅Закат солнца: <b>{datetime.fromtimestamp(data['sys']['sunset'])}</b>\nПродолжительность дня: <b>{datetime.fromtimestamp(data['sys']['sunset']) - datetime.fromtimestamp(data['sys']['sunrise'])}</b>\n"
            )
        
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        msg = await bot.send_message(message.chat.id, text, parse_mode='HTML')
    except:
        msg = await message.reply("☹ ️Не удалось найти такой город.\nПопробуйте снова.")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    await as_del_msg(message.chat.id, message.message_id, time_del)
