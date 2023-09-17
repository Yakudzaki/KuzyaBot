from pyrogram import Client, filters  #pip install pyrogram
from data import config
import logging
import asyncio

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
import shutil
import requests
import json
import os
import re
from bs4 import BeautifulSoup as bs
import time
from datetime import timedelta
import math
import base64

TOKEN = config.TOKEN
API_ID = config.API_ID
API_HASH = config.API_HASH

api_id = API_ID
api_hash = API_HASH
bot_token = TOKEN

#Для фикса варнинга о ТгКрипто
# pip3 install --upgrade --user tgcrypto
# pip3 install --upgrade --user pyrogram[fast]
# или
# pip3 install --U --user tgcrypto
# pip3 install --U --user pyrogram[fast]

async def get_chat_members(chat_id):
    app = Client("Кузя | Бот", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    
    await app.start()
    
    chat_members_in = []    
    chat_members_del = []
    async for member in app.get_chat_members(chat_id):

        if member.user.is_deleted == False:
            chat_members_in = chat_members_in + [member.user.id]
        else:
            chat_members_del = chat_members_del + [member.user.id]
    
    await app.stop()
    chat_members = [chat_members_in, chat_members_del]
    return chat_members
    
async def get_delete_members(chats):
    app = Client("Кузя | Бот", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    
    await app.start()
    chat_members = [] 
    for chat_id in chats:
        await asyncio.sleep(60)
        async for member in app.get_chat_members(chat_id):
            if member.user.is_deleted == True:
                chat_members = chat_members + [member.user.id]
    await app.stop()
    
    return chat_members



async def pyro_get_chat_member(chat_id, username):
    app = Client("Кузя | Бот", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    
    await app.start()
    
    member = await app.get_chat_member(chat_id, username)

    await app.stop()
    
    return member
    
async def pyro_tiktok(message):
    if message.text.startswith('https://vm.tiktok.com') or message.text.startswith('https://www.tiktok.com'):
        app = Client("Кузя | Бот", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
        stop = None
        await app.start()
        try:
            stop = await tiktok_dl(app, message)
        except:
            pass
        await app.stop()
        return stop


async def tiktok_dl(app, message):

    
    
    a = await app.send_message(chat_id=message.chat.id,
                         text='__Downloading File to the Server__')
    link = re.findall(r'\bhttps?://.*[(tiktok|douyin)]\S+', message.text)[0]
    link = link.split("?")[0]

    print(link)

    
    params = {
      "link": link
    }
    headers = {
      'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
      'x-rapidapi-key': "f9d65af755msh3c8cac23b52a5eep108a33jsnbf7de971bb72"
    }
    
    ### Get your Free TikTok API from https://rapidapi.com/TerminalWarlord/api/tiktok-info/
    #Using the default one can stop working any moment 
    
    api = f"https://tiktok-info.p.rapidapi.com/dl/"
    rere = requests.get(api, params=params, headers=headers).json()
    print(f"{rere}")
    try:
        if rere['status'] == "failed":
            await a.edit(f'Не вышло!')
            return
    except:
        pass
    r = rere['videoLinks']['download']
    directory = str(round(time.time()))
    filename = str(int(time.time()))+'.mp4'
    size = int(requests.head(r).headers['Content-length'])
    total_size = "{:.2f}".format(int(size) / 1048576)
    try:
        os.mkdir(directory)
    except:
        pass
    with requests.get(r, timeout=(50, 10000), stream=True) as r:
        r.raise_for_status()
        with open(f'./{directory}/{filename}', 'wb') as f:
            chunk_size = 1048576
            dl = 0
            show = 1
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                dl = dl + chunk_size
                percent = round(dl * 100 / size)
                if percent > 100:
                    percent = 100
                if show == 1:
                    try:
                        await a.edit(f'__**URL :**__ __{message.text}__\n'
                               f'__**Total Size :**__ __{total_size} MB__\n'
                               f'__**Downloaded :**__ __{percent}%__\n',
                               disable_web_preview=False)
                    except:
                        pass
                    if percent == 100:
                        show = 0

        await a.edit(f'__Downloaded to the server!\n'
               f'Uploading to Telegram Now ⏳__')
        start = time.time()
        title = filename
        await app.send_document(chat_id=message.chat.id,
                          document=f"./{directory}/{filename}",
                          caption=f"**File :** __{filename}__\n"
                          f"**Size :** __{total_size} MB__\n\n",
                          file_name=f"{directory}")
        await a.delete()
        try:
            shutil.rmtree(directory)
        except:
            pass
