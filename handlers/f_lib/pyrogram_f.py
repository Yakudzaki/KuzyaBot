from pyrogram import Client  #pip install pyrogram
from data import config
import logging
import asyncio

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