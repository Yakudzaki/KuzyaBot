from loader import dp, bot
from aiogram import types
from random import randint, choice
import time
import globales
from utils.db.db_utils_users import *
from utils.db.db_utils_сhats import *
from utils.db.db_utils_warning import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter
from settings import *
from ..lib.shield import *



#Основная функция видео

async def final_video(message: types.Message):
    user = message.from_user
    
    if message.chat.type == 'private':
        return
    chats = message.chat.id
    chat = get_chat(chats)
    if check_chat(message.chat.id):
        create_chat(message.chat.id)
        chat = get_chat(chats)

    video_limit = chat[10]
    funny = chat[4] #проверка разрешения приколов
    shield = chat[13]
    
    cor = globales.get_cor()
    user_cor_v = cor[0]
    chat_cor_v = cor[1]
    cor_v = cor[2]
    
    user_cor_st = cor[3]
    chat_cor_st = cor[4]
    cor_st = cor[5]
    
    user_cor_a = cor[6]
    chat_cor_a = cor[7]
    cor_a = cor[8]
    
    user_cor_tx = cor[9]
    chat_cor_tx = cor[10]
    cor_tx = cor[11]
    
    user_cor_ph = cor[12]
    chat_cor_ph = cor[13]
    cor_ph = cor[14]
    


    
    if message.from_user.id != user_cor_v:
        user_cor_v = message.from_user.id
        cor_v = 0
    if message.chat.id != chat_cor_v:
        chat_cor_v = message.chat.id
        cor_v = 0
    if cor_v >= video_limit and user.id not in whitelist:
        await bot.delete_message(message.chat.id, message.message_id)

        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0
        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0
        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    if message.from_user.id == user_cor_v and message.chat.id == chat_cor_v:
        cor_v = cor_v + 1

        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0
        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0
        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    if int(message.from_user.id) == int(-1001296725176):
        return
    
    globales.set_cor(user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph)


    warner = get_warner(message.chat.id, message.from_user.id)

    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    
    video = message.video
    if video and ( shield != 0 or warner[2] != 0 ):
        mrm = False
        if message.reply_to_message:
            mrm = True
# АНТИСПАМ И АНТИРЕКЛАМА
        
        stop = await media_shield(message, mrm, warner)
        if stop != None:
            return stop
#Антибот
        if shield == 2:
    
            stop = await antibot(message)
        
            if stop != None:
                return stop

    
    if shield != 0:
        if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
            from ..lib.other import restrict_chat
            await restrict_chat(message)




#Основная функция анимация

async def final_animation(message: types.Message):
    if message.chat.type == 'private':
        return
    user = message.from_user
    animation = message.animation

    chats = message.chat.id
    
    if check_chat(message.chat.id):
        create_chat(message.chat.id)
    chat = get_chat(chats)
        
    anmiation_limit = chat[11]
    funny = chat[4] #проверка разрешения приколов
    shield = chat[13]
    
    cor = globales.get_cor()
    user_cor_v = cor[0]
    chat_cor_v = cor[1]
    cor_v = cor[2]
    
    user_cor_st = cor[3]
    chat_cor_st = cor[4]
    cor_st = cor[5]
    
    user_cor_a = cor[6]
    chat_cor_a = cor[7]
    cor_a = cor[8]
    
    user_cor_tx = cor[9]
    chat_cor_tx = cor[10]
    cor_tx = cor[11]
    
    user_cor_ph = cor[12]
    chat_cor_ph = cor[13]
    cor_ph = cor[14]
    
    
    if message.from_user.id != user_cor_a:
        user_cor_a = message.from_user.id
        cor_a = 0
    if message.chat.id != chat_cor_a:
        chat_cor_a = message.chat.id
        cor_a = 0
    if cor_a >= anmiation_limit and user.id not in whitelist:
        await bot.delete_message(message.chat.id, message.message_id)
        if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
            cor_v = 0
        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0

        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    if message.from_user.id == user_cor_a and message.chat.id == chat_cor_a:
        cor_a = cor_a + 1
        if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
            cor_v = 0
        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0

        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    
    globales.set_cor(user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph)

    warner = get_warner(message.chat.id, message.from_user.id)

    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    
    if int(message.from_user.id) == int(-1001296725176):
        return
    
    if animation and ( shield != 0 or warner[2] != 0 ):
        mrm = False
        if message.reply_to_message:
            mrm = True
# АНТИСПАМ И АНТИРЕКЛАМА


        stop = await media_shield(message, mrm, warner)
        if stop != None:
            return stop
#Антибот
        if shield == 2:
    
            stop = await antibot(message)
        
            if stop != None:
                return stop

    if shield != 0:
        if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
            from ..lib.other import restrict_chat
            await restrict_chat(message)





#Основная функция фото

async def final_photo(message: types.Message):

    if message.chat.type == 'private':
        return
    chats = message.chat.id
    user = message.from_user
    if check_chat(message.chat.id):
        create_chat(message.chat.id)
    
    chat = get_chat(chats)
        
    
    photo_limit = chat[8]
    funny = chat[4] #проверка разрешения приколов
    shield = chat[13]
    
    cor = globales.get_cor()
    
    user_cor_v = cor[0]
    chat_cor_v = cor[1]
    cor_v = cor[2]
    
    user_cor_st = cor[3]
    chat_cor_st = cor[4]
    cor_st = cor[5]
    
    user_cor_a = cor[6]
    chat_cor_a = cor[7]
    cor_a = cor[8]
    
    user_cor_tx = cor[9]
    chat_cor_tx = cor[10]
    cor_tx = cor[11]
    
    user_cor_ph = cor[12]
    chat_cor_ph = cor[13]
    cor_ph = cor[14]
    
    if message.from_user.id != user_cor_ph:
        user_cor_ph = message.from_user.id
        cor_ph = 0
    if message.chat.id != chat_cor_ph:
        chat_cor_ph = message.chat.id
        cor_ph = 0
    if cor_ph >= photo_limit and user.id not in whitelist:
        await bot.delete_message(message.chat.id, message.message_id)
        if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
            cor_v = 0
        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0
        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0

        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    if message.from_user.id == user_cor_ph and message.chat.id == chat_cor_ph:
        cor_ph = cor_ph + 1
        if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
            cor_v = 0
        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0
        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0

        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    
    globales.set_cor(user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph)

    warner = get_warner(message.chat.id, message.from_user.id)

    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    
    photo = message.photo[-1]
    if int(message.from_user.id) == int(-1001296725176):
        return
    if photo and ( shield != 0 or warner[2] != 0 ):
        mrm = False
        if message.reply_to_message:
            mrm = True
# АНТИСПАМ И АНТИРЕКЛАМА


        stop = await media_shield(message, mrm, warner)
        if stop != None:
            return stop
#Антибот
        if shield == 2:
    
            stop = await antibot(message)
        
            if stop != None:
                return stop
    

    
    if shield != 0:
        if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
            from ..lib.other import restrict_chat
            await restrict_chat(message)




#Основная функция стикеры

async def final_sticker(message: types.Message):
    
    if message.chat.type == 'private':
        return
    chats = message.chat.id
    user = message.from_user
    if check_chat(message.chat.id):
        create_chat(message.chat.id)
    chat = get_chat(chats)
        
    sticker_limit = chat[12]
    funny = chat[4] #проверка разрешения приколов
    shield = chat[13]
    
    cor = globales.get_cor()
    
    user_cor_v = cor[0]
    chat_cor_v = cor[1]
    cor_v = cor[2]
    
    user_cor_st = cor[3]
    chat_cor_st = cor[4]
    cor_st = cor[5]
    
    user_cor_a = cor[6]
    chat_cor_a = cor[7]
    cor_a = cor[8]
    
    user_cor_tx = cor[9]
    chat_cor_tx = cor[10]
    cor_tx = cor[11]
    
    user_cor_ph = cor[12]
    chat_cor_ph = cor[13]
    cor_ph = cor[14]
    
    
    if message.from_user.id != user_cor_st:
        user_cor_st = message.from_user.id
        cor_st = 0
    if message.chat.id != chat_cor_st:
        chat_cor_st = message.chat.id
        cor_st = 0
    if cor_st >= sticker_limit and user.id not in whitelist:
        await bot.delete_message(message.chat.id, message.message_id)
        if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
            cor_v = 0

        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0
        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0

    
    if message.from_user.id == user_cor_st and message.chat.id == chat_cor_st:
        cor_st = cor_st + 1
        if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
            cor_v = 0
        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0
        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    globales.set_cor(user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph)

    
    if shield != 0:
        if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
            from ..lib.other import restrict_chat
            await restrict_chat(message)
#Антибот
        if shield == 2:
            await antibot(message)



#Основная функция кругетсы

async def final_videonote(message: types.Message):
    
    if message.chat.type == 'private':
        return
    chats = message.chat.id
    user = message.from_user
    if check_chat(message.chat.id):
        create_chat(message.chat.id)
    chat = get_chat(chats)
        
    video_limit = chat[10]
    funny = chat[4] #проверка разрешения приколов
    shield = chat[13]
    
    cor = globales.get_cor()
    
    user_cor_v = cor[0]
    chat_cor_v = cor[1]
    cor_v = cor[2]
    
    user_cor_st = cor[3]
    chat_cor_st = cor[4]
    cor_st = cor[5]
    
    user_cor_a = cor[6]
    chat_cor_a = cor[7]
    cor_a = cor[8]
    
    user_cor_tx = cor[9]
    chat_cor_tx = cor[10]
    cor_tx = cor[11]
    
    user_cor_ph = cor[12]
    chat_cor_ph = cor[13]
    cor_ph = cor[14]
    
    if message.from_user.id != user_cor_v:
        user_cor_v = message.from_user.id
        cor_v = 0
    if message.chat.id != chat_cor_v:
        chat_cor_v = message.chat.id
        cor_v = 0
    if cor_v >= video_limit and user.id not in whitelist:
        await bot.delete_message(message.chat.id, message.message_id)

        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0
        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0
        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    if message.from_user.id == user_cor_v and message.chat.id == chat_cor_v:
        cor_v = cor_v + 1
        if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
            cor_st = 0
        if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
            cor_a = 0
        if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
            cor_ph = 0
        if user_cor_tx == message.from_user.id and chat_cor_tx == message.chat.id:
            cor_tx = 0
    
    globales.set_cor(user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph)
    


    if shield != 0:
        if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
            from ..lib.other import restrict_chat
            await restrict_chat(message)
        
        if shield == 2:
            await antibot(message)
            
#Основная функция Голоса
async def final_voice(message: types.Message):

    
    mrm = False
    if message.reply_to_message:
        mrm = True
    
    mctp = False  #Чтоб дальше проверять не целую строку type, а простейшую переменную.
    if message.chat.type == 'private':
        mctp = True
    
    if mctp == False:
        chats = message.chat.id
        if check_chat_m(chats):  #Запись чата в оперативку.
            create_chat_m(chats)

        if check_chat(chats) == False:
            chat = get_chat(chats)
        else:
            create_chat_with_info(chats, f"{message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
            chat = get_chat(chats)
        
        

        shield = chat[13]
    
    
        if shield != 0:
            if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
                from ..lib.other import restrict_chat
                await restrict_chat(message)
            
            if shield == 2:
                await antibot(message)

#Основная функция Аудио и музыки
async def final_audio(message: types.Message):
    

    
    mrm = False
    if message.reply_to_message:
        mrm = True
    
    mctp = False  #Чтоб дальше проверять не целую строку type, а простейшую переменную.
    if message.chat.type == 'private':
        mctp = True
    
    if mctp == False:
        chats = message.chat.id
        if check_chat_m(chats):  #Запись чата в оперативку.
            create_chat_m(chats)

        if check_chat(chats) == False:
            chat = get_chat(chats)
        else:
            create_chat_with_info(chats, f"{message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
            chat = get_chat(chats)

        shield = chat[13]
    
    
        if shield != 0:
            if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
                from ..lib.other import restrict_chat
                await restrict_chat(message)
            if shield == 2:
                await antibot(message)

#Основная функция игры

async def final_game(message: types.Message):
    
    
    if message.chat.type == 'private':
        return
    chats = message.chat.id
    user = message.from_user
    if check_chat(chats) == False:
        chat = get_chat(chats)
    else:
        create_chat_with_info(chats, f"{message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
        chat = get_chat(chats)


    shield = chat[13]
    funny = chat[4]

#Антибот
    if shield == 2 or funny == 0:
        await antibot(message)
        