from aiogram import types
import random
from loader import dp, bot
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from settings import kuzya_news_link

from utils.db.db_utils_сhats import *
from bs4 import BeautifulSoup
import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def anti_flood(*args, **kwargs):

    message = args[0]
    await message.answer("Шутку читай, а не спамь сука!", show_alert=True)


async def get_joke():
    try:
        async with aiohttp.ClientSession() as session:
            joke_html = await session.get('https://nekdo.ru/random/')
            joke_text = (await joke_html.text()).replace("<br>", "\n")
            joke_text = BeautifulSoup(joke_text, features="lxml").find('div', class_='text').get_text()
            return joke_text
    except:
        async with aiohttp.ClientSession() as session:
            joke_html = await session.get('https://nekdo.ru/random/')
            joke_text = (await joke_html.text()).replace("<br>", "\n")
            joke_text = BeautifulSoup(joke_text, features="lxml").find('div', class_='text').get_text()
            if random.choice([True, False]):
                joke_text += f"\n\n<a href='{kuzya_news_link}'>🗞 Канал с новостями</a>"
            return joke_text



@dp.message_handler(commands=["шутка", "анекдот"], commands_prefix="/!.")
@dp.throttled(anti_flood,rate=2)
async def joke(message: types.Message):
    text = await get_joke()
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
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
    
    keyboard = InlineKeyboardMarkup()

    buttons = [
                    InlineKeyboardButton(text="🔄 Обновить", callback_data="updatej"),
                    InlineKeyboardButton(text="🔻 Закрыть", callback_data="closej")
                ]

    keyboard.add(*buttons)
    
    await message.reply(text, disable_web_page_preview=True, reply_markup=keyboard)
    

async def get_citat():
    try:
        async with aiohttp.ClientSession() as session:
            citat_html = await session.get('https://citaty.info/random/')
            citat_text = (await citat_html.text()).replace("<br>", "\n")
            citat_text = BeautifulSoup(citat_text, features="lxml").find('div', class_="field-item even last").get_text()

            return citat_text
    except:
        try:
            async with aiohttp.ClientSession() as session:
                citat_html = await session.get('https://citaty.info/random/')
                citat_text = (await citat_html.text()).replace("<br>", "\n")
                citat_text = BeautifulSoup(citat_text, features="lxml").find('div', class_="field-item even last").get_text()

                return citat_text
        except:
            async with aiohttp.ClientSession() as session:
                citat_html = await session.get('https://citaty.info/random/')
                citat_text = (await citat_html.text()).replace("<br>", "\n")
                citat_text = BeautifulSoup(citat_text, features="lxml").find('div', class_="field-item even last").get_text()
                if random.choice([True, False]):
                    citat_text += f"\n\n<a href='{kuzya_news_link}'>🗞 Канал с новостями</a>"
                return citat_text
    

@dp.message_handler(commands=["цитата"], commands_prefix="/!.")
async def citat(message: types.Message):
    text = await get_citat()
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
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


    create_user(users.id, users.username, users.first_name)

    
    
    await message.reply(text, disable_web_page_preview=True)
