from loader import dp, bot
from aiogram import types
import pyowm
from pyowm.utils.config import get_default_config
from datetime import datetime
from ..lib.other import as_del_msg
from settings import time_del
from utils.db.db_utils_warning import *

config_dict = get_default_config()

config_dict['language'] = 'ru' 
owm = pyowm.OWM('4d9c68ba051733b61d30fa2406658670')
mgr = owm.weather_manager()



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
        
        observation = mgr.weather_at_place(city)
        w = observation.weather
        
        
        text = f"🏙️ <b>Город</b>: <b>{city}</b>\n"
        text += f"🔍 <b>Статус</b> - <em>{w.detailed_status}</em>\n\n"
        text += f"🌡 <b>️Максимальная температура</b>: <code>{w.temperature('celsius')['temp_max']} °C</code>\n"
        text += f"🌡️ <b>Минимальная температура</b>: <code>{w.temperature('celsius')['temp_min']} °C</code>\n"
        text += f"🌡 ️<b>Ощущается как</b>: <code>{w.temperature('celsius')['feels_like']} °C</code>\n\n"
        text += f"💧 <b>Влажность</b>: <code>{w.humidity}%</code>\n"
        text += f"💨 <b>Скорость ветра</b>: <code>{w.wind()['speed']} м/с</code>\n"
        text += f"☁️ <b>Облачность</b>: <code>{w.clouds}%</code>\n"
        
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        msg = await bot.send_message(message.chat.id, text, parse_mode='HTML')
    except:
        msg = await message.reply("☹ ️Не удалось найти такой город.\nПопробуйте снова.")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    await as_del_msg(message.chat.id, message.message_id, time_del)