from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import aiohttp
from bs4 import BeautifulSoup

from random import randint, choice
from settings import kuzya_news_link
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from utils.db.db_utils_сhats import *

async def anti_flood(*args, **kwargs):

    message = args[0]
    await message.answer("Мем читай, а не спамь сука!", show_alert=True)



@dp.message_handler(commands=["meme", "mem", "мем"], commands_prefix="/!.")

@dp.throttled(anti_flood,rate=2)

async def meme(message: types.Message):
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
    
    user = create_user(users.id, users.username, users.first_name)

    try:

        random_site = randint(1, 3119)

        url = f"https://www.memify.ru/memes/{random_site}"

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                content = await response.text()

                soup = BeautifulSoup(content, "html.parser")

                items = soup.find_all("div", {"class": "infinite-item card"})

                random_item = choice(items)

                second_a = random_item.find_all("a")[1]

                keyboard = types.InlineKeyboardMarkup()

                buttons = [

                    types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update")

                ]

                keyboard.add(*buttons)
                await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_PHOTO)
                await bot.send_photo(message.chat.id, second_a.get("href"), caption = f'☄️ Лови мем.\n\n<a href="{kuzya_news_link}">Канал с новостями</a>', reply_markup=keyboard, parse_mode="html")

    # except Exception as e:
    except:
        try:
    
            random_site = randint(1, 2857)
    
            url = f"https://www.memify.ru/memes/{random_site}"
    
            async with aiohttp.ClientSession() as session:
    
                async with session.get(url) as response:
    
                    content = await response.text()
    
                    soup = BeautifulSoup(content, "html.parser")
    
                    items = soup.find_all("div", {"class": "infinite-item card"})
    
                    random_item = choice(items)
    
                    second_a = random_item.find_all("a")[1]
    
                    keyboard = types.InlineKeyboardMarkup()
    
                    buttons = [
    
                        types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update")
    
                    ]
    
                    keyboard.add(*buttons)
                    await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_PHOTO)
                    await bot.send_photo(message.chat.id, second_a.get("href"), caption = f'☄️ Лови мем.\n\n<a href="{kuzya_news_link}">Канал с новостями</a>', reply_markup=keyboard, parse_mode="html")
    
        except Exception as e:
            print(f"{e}")
            logging.info(f"{e}")
            return

        
        # except Exception as e:
    
            # print(e)
            