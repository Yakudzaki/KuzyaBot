import aiohttp
from aiogram import types
from loader import dp, bot
from utils.db.db_utils_warning import get_warner
from utils.db.db_utils_сhats import get_chat, create_chat, check_chat

class AnimeHandler:
    async def __call__(self, message: types.Message):
        if message.chat.type != 'private':
            chat_id = message.chat.id
            chat = get_chat(chat_id)
            if not check_chat(chat_id):
                create_chat(chat_id)
                chat = get_chat(chat_id)
    
            funny = chat[4]  # проверка разрешения приколов
            if not funny:
                await message.reply("❌ В этом чате игры с ботом запрещены!")
                return
        
            warner = get_warner(chat_id, message.from_user.id)
            if not warner:
                warner = [chat_id, message.from_user.id, 0, 0, 0]
            if warner[4] != 0:
                return
    
        url = "https://pic.re/image"
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                data = await response.json()
                await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_PHOTO)
                # Получение данных о фотографии
                file_url = data.get("file_url", "")
                source = data.get("source", "")
                author = data.get("author", "")
    
                # Отправка фотографии и описания
                if not file_url:
                    await message.reply("Что-то пошло не так! Попробуйте ещё раз.")
                    return
                await bot.send_photo(message.chat.id, file_url, caption=f"Источник: {source}\nАвтор: {author}")

anime_handler = AnimeHandler()

@dp.message_handler(commands=['аниме', 'тян'], commands_prefix="/!.")
async def anime_handler_wrapper(message: types.Message):
    await anime_handler(message)