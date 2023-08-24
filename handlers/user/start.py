from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from loguru import logger
from utils.db.db_utils_users import *

from settings import legal_chats, topa_chat_invite, yakudza_url

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    if message.chat.id not in legal_chats and message.chat.type != 'private':
        await message.answer(f"❌ Я создан исключительно для чата <a href='{topa_chat_invite}'>Опа Это Топа</a>!", parse_mode="html", disable_web_page_preview=True)
        await message.answer(f"Айди вашего чата: [{str(message.chat.id)}]\nДоговаривайтесь с <a href='{yakudza_url}'>создателем</a> бота.", parse_mode="html", disable_web_page_preview=True)

        if check_chat(message.chat.id):
            create_chat_with_info(message.chat.id, f"НЕЛЕГАЛ: {message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
            chat = get_chat(chats)
        await bot.leave_chat(message.chat.id)
        return
    
    user = message.from_user

    users = create_user(user.id, user.username, user.first_name)
    await message.answer(f"Привет, {users[2]}, я Кузя!\n\nИспользуй  /help что-бы ознакомиться с командами.")
    

@dp.message_handler(commands=['перезапуск', 'restart', 'рестарт'],commands_prefix="!./")
async def restart_botovod(message: types.Message):
    if message.from_user.id in botovod_id or message.from_user.id in helpers_ids:
        await message.answer("Кузя идет на перезапуск!")
        from subprocess import call
        call('Kuzya restart.bat')
    else:
        await message.answer("У вас недостаточно полномочий!")