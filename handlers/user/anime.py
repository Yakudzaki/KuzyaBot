import requests
from loader import dp, bot
from aiogram import types


# Обработчик команды
@dp.message_handler(commands=['аниме', 'тян'], commands_prefix="/!.")
async def send_image(message: types.Message):
    url = "https://pic.re/image"
    response = requests.post(url)
    data = response.json()
    await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_PHOTO)
    # Получение данных о фотографии
    file_url = data["file_url"]
    source = data["source"]
    author = data["author"]
    
    # Отправка фотографии и описания
    await bot.send_photo(message.chat.id, file_url, caption=f"Источник: {source}\nАвтор: {author}")
