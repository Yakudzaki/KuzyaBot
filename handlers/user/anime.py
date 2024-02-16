import aiohttp

from loader import dp, bot
from aiogram import types
from utils.db.db_utils_users import *
from utils.db.db_utils_сhats import *
from utils.db.db_utils_warning import *


@dp.message_handler(commands=['аниме', 'тян'], commands_prefix="/!.")
async def send_image(message: types.Message):
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
    
    
    url = "https://pic.re/image"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            data = await response.json()
            await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_PHOTO)
            # Получение данных о фотографии
            file_url = data["file_url"]
            source = data["source"].replace("", "Неизвестно")
            author = data["author"].replace("", "Неизвестно")
    
            # Отправка фотографии и описания
            if file_url == "" or file_url is None:
                await message.reply("Что-то пошло не так! Попробуйте ещё раз.")
                return
            await bot.send_photo(message.chat.id, file_url, caption=f"Источник: {source}\nАвтор: {author}")
