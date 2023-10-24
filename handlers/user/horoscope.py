import requests
import json
from aiogram import types
from loader import dp, bot


@dp.message_handler(commands=['гороскоп'], commands_prefix="/!.")
async def command_horoscope(message: types.Message):
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

@dp.callback_query_handler(lambda c: c.data.startswith('horoscope_'))
async def process_horoscope(callback: types.CallbackQuery):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    horoscope_name = callback.data.split('_')[1]
    link = f'https://horoscopes.rambler.ru/api/front/v1/horoscope/today/{horoscope_name}/'
    response = requests.get(link)
    data = json.loads(response.text)
    img_url = data['meta']['og_image']
    date = data['source']
    h1 = data['h1'].replace('сегодня', date)
    text = data['text']
    
    await bot.send_photo(callback.from_user.id, img_url, caption=f"<b>{h1}</b>\n\n{text}", parse_mode="html")
