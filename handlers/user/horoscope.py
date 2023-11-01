import requests
import json
from aiogram import types
from loader import dp, bot
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from utils.db.db_utils_сhats import *

@dp.message_handler(commands=['гороскоп'], commands_prefix="/!.")
async def command_horoscope(message: types.Message):
    users = message.from_user
    
    if message.chat.type != 'private':
        chats = message.chat.id #Отсюда и далее, до пустой строки - выключатель этого прикола.
        chat = get_chat(chats)
        if check_chat(message.chat.id):
            create_chat(message.chat.id)
            chat = get_chat(chats)
    
        funny = chat[4] #проверка разрешения приколов
        if not funny:
            await message.answer("❌ В этом чате игры с ботом запрещены!")
            return
        
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text="Овен ♈", callback_data='horoscope_aries'),
        types.InlineKeyboardButton(text="Телец ♉", callback_data='horoscope_taurus')
    )
    keyboard.row(
        types.InlineKeyboardButton(text="Близнецы ♊", callback_data='horoscope_gemini'),
        types.InlineKeyboardButton(text="Рак ♋", callback_data='horoscope_cancer')
    )
    keyboard.row(
        types.InlineKeyboardButton(text="Лев ♌️", callback_data='horoscope_leo'),
        types.InlineKeyboardButton(text="Дева ♍️", callback_data='horoscope_virgo')
    )
    keyboard.row(
        types.InlineKeyboardButton(text="Весы ♎️", callback_data='horoscope_libra'),
        types.InlineKeyboardButton(text="Скорпион ♏️", callback_data='horoscope_scorpio')
    )
    keyboard.row(
        types.InlineKeyboardButton(text="Стрелец ♐️", callback_data='horoscope_sagittarius'),
        types.InlineKeyboardButton(text="Козерог ♑️", callback_data='horoscope_capricorn')
    )
    keyboard.row(
        types.InlineKeyboardButton(text="Водолей ♒️", callback_data='horoscope_aquarius'),
        types.InlineKeyboardButton(text="Рыбы ♓️", callback_data='horoscope_pisces')
    )
    
    await message.reply("Выбери свой гороскоп:", reply_markup=keyboard)
    await bot.delete_message(message.chat.id, message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('horoscope_'))
async def process_horoscope(callback: types.CallbackQuery):
   
    if callback.message.chat.type != 'private':
        chats = callback.message.chat.id #Отсюда и далее, до пустой строки - выключатель этого прикола.
        chat = get_chat(chats)
        if check_chat(callback.message.chat.id):
            create_chat(callback.message.chat.id)
            chat = get_chat(chats)
    
        funny = chat[4] #проверка разрешения приколов
        if not funny:
            await callback.message.answer("❌ В этом чате игры с ботом запрещены!")
            return
        
        warner = get_warner(callback.message.chat.id, callback.from_user.id)
        if warner == None:
            warner = [callback.message.chat.id, callback.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    horoscope_name = callback.data.split('_')[1]
    link = f'https://horoscopes.rambler.ru/api/front/v1/horoscope/today/{horoscope_name}/'
    response = requests.get(link)
    data = json.loads(response.text)
    img_url = data['meta']['og_image']
    date = data['source']
    h1 = data['h1'].replace('сегодня', date)
    text = data['text']
    
    await bot.send_photo(callback.message.chat.id, img_url, caption=f"<b>{h1}</b>\n\n{text}", parse_mode="html")
