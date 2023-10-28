from aiogram import types
import logging
import globales
from loader import bot
from settings import *
from utils.db import *

from ..f_lib.mats import *
from ..f_lib.shield import *
from ..admin.owner import *
from .games import botik_text_other
from .profiles import add_reputation_f, take_reputation_f
from .RP import rp_list
from .tiktok import send_video
#Основная функция ТЕКСТА

async def final_text(message: types.Message):

    user = message.from_user
    if int(message.from_user.id) == int(-1001296725176):
        return
    vermat = 0 
    secmat = 0
    matex = 0
    funny = 1
    text_limit = 100
    matrep = 0
    shield = 0
    
    mrm = False
    if message.reply_to_message:
        mrm = True
    
    mctp = False  #Чтоб дальше проверять не целую строку type, а простейшую переменную.
    if message.chat.type == 'private':
        mctp = True
        chat = ["private"]
        
    user_in_base = False
    if check_user(message.from_user.id) == False:
        user_in_base = True
    
    if mctp == False:
        warner = get_warner(message.chat.id, message.from_user.id)
    
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    
    else:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    
    if mctp == False:
        chats = message.chat.id
        if check_chat_m(chats):  #Запись чата в оперативку.
            create_chat_m(chats)

        if check_chat(chats) == False:
            chat = get_chat(chats)
        else:
            create_chat_with_info(chats, f"{message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
            chat = get_chat(chats)

        
        funny = chat[4] #проверка разрешения приколов
        vermat = chat[1] #Получение шанса антимата из базы   
        secmat = chat[2] #Получение мута антимата из базы
        matrep = chat[7]
        text_limit = chat[9] #получение из баз лимитов спама текста в чате
        shield = chat[13]

#Запись челов в базу мемберов если они уже есть в базе юзеров (в случае если это не ответ на другое сообщение)
        
        if mrm == False and member_add == True:

            if user_in_base == True:
                if check_member(message.chat.id, message.from_user.id) == False:
                    ment = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    if ment.status != "left" and ment.status != "kicked":
                        create_member(message.chat.id, message.from_user.id, ment.status)
                        

#Добавление челов в базы и МЕМБЕРОВ и ЮЗЕРОВ, если они напишут в чате хоть что-нибудь. (в случае если это не ответ на другое сообщение)
            
            elif user_add == True:
                create_user(user.id, user.username, user.first_name)
                if check_member(message.chat.id, message.from_user.id) == False:
                    ment = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    if ment.status != "left" and ment.status != "kicked":
                        create_member(message.chat.id, message.from_user.id, ment.status)
                        
                
    
#АНТИСПАМ
    if mctp == False:
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
        
        stop = None
        if message.from_user.id != user_cor_tx and mctp == False:
            user_cor_tx = message.from_user.id
            cor_tx = 0
        if message.chat.id != chat_cor_tx and mctp == False:
            chat_cor_tx = message.chat.id
            cor_tx = 0
        if cor_tx >= text_limit and mctp == False and user.id not in whitelist:
            await bot.delete_message(message.chat.id, message.message_id)
            if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
                cor_v = 0
    
            if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
                cor_st = 0
            if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
                cor_a = 0
            if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
                cor_ph = 0
            
            stop = 1
    
        
        if message.from_user.id == user_cor_tx and message.chat.id == chat_cor_tx and mctp == False:
            cor_tx = cor_tx + 1
            
            if user_cor_v == message.from_user.id and chat_cor_v == message.chat.id:
                cor_v = 0
                
            if user_cor_st == message.from_user.id and chat_cor_st == message.chat.id:
                cor_st = 0
            if user_cor_a == message.from_user.id and chat_cor_a == message.chat.id:
                cor_a = 0
            if user_cor_ph == message.from_user.id and chat_cor_ph == message.chat.id:
                cor_ph = 0
            
        globales.set_cor(user_cor_v, chat_cor_v, cor_v, user_cor_st, chat_cor_st, cor_st, user_cor_a, chat_cor_a, cor_a, user_cor_tx, chat_cor_tx, cor_tx, user_cor_ph, chat_cor_ph, cor_ph)
    
        if stop == 1:
            return stop
    else:
        cor_tx = 0
    


# АНТИСПАМ И АНТИРЕКЛАМА

    if shield != 0 or warner[2] != 0:
        stop = await text_shield(message, mrm, cor_tx, user_in_base, warner)
        if stop != None:
            return stop
#Антибот
        if shield == 2:
    
            stop = await antibot(message)
        
            if stop != None:
                return stop

#АНТИМАТ
    if mctp == False:
    
        if vermat > 0:
            if warner[3] > vermat:
                await anti_mat(message, warner[3], matrep, secmat, 101, user_in_base)
            else:
                await anti_mat(message, vermat, matrep, secmat, adminmatnote, user_in_base)
        else:
            if warner[3] > 0:
                await anti_mat(message, warner[3], matrep, secmat, 101, user_in_base)


#Удаление Кузей сообщений Кузи, которые кто-то перешлет в чат, в котором вырублены игры.
    if not funny:
        if message.forward_from:
            try: 
                us2 = message.forward_from.id
                if int(us2) == botik_id:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    return
            except:
                pass


#импорт из games.py - гадания, шанса, и отзыва Кузи.

    stop = await botik_text_other(message, funny, cor_tx, user_in_base, warner)
    
    if stop != None:
        return stop
    

    



    if funny != 0 and warner[4] == 0:
#импорт из rp без-префикс-ных рп
        stop = await rp_list(message)
        if stop != None:
            return stop
#ТИКТОК
        if "https://" in message.text:
            stop = send_video(message)
            if stop != None:
                return stop

#Правила
    rules = ["!правила", "/правила", ".правила", "правила", "!rules", "/rules", ".rules"]
    if message.text.lower() in rules and chat[16] != "" and chat[16] != None:
        await message.reply(f"<a href='{chat[16]}'>Правила чата</a>")
        return
    
    if shield != 0:
        if message.from_user.id == 777000 and message.sender_chat and message.forward_from_chat and message.is_automatic_forward:
            from ..f_lib.other import restrict_chat
            await restrict_chat(message)


#Нечеткое сравнение для повышения или понижения репутации
    if mrm == True and mctp == False and message.from_user.id != message.reply_to_message.from_user.id and warner[4] == 0:
        repu = message.reply_to_message.from_user
        if check_user(repu.id) == False:
            
            reper = message.from_user
            
            if user_in_base == False:
                reperr = [0, 0, 0, 0, 0, 0, 0]
            else:
                reperr = get_user(reper.id)
            
            repur = get_user(repu.id)

            adding = await add_reputation_f(message, reperr, repur)
            
            if adding == True:
                print(f"Повышено у {repur[0]} {repur[1]} {repur[2]}")
                logging.info(f"Повышено у {repur[0]} {repur[1]} {repur[2]}")
            
            if adding == None:
                taking = await take_reputation_f(message, reperr, repur)
                if taking == True:
                    print(f"Понижено у {repur[0]} {repur[1]} {repur[2]}")
                    logging.info(f"Понижено у {repur[0]} {repur[1]} {repur[2]}")
#РАЗРАБЫ
    await owner_func(message, mctp, mrm, chat)

#ПРОЩАНИЕ С КЕМ-ТО УШЕДШИМ (По английски!)
    
    if mctp == False and mrm == True and goodbye == True:
        chats = message.chat.id
        m_count = await bot.get_chat_member_count(chats)
        chat = get_chat(chats)
        if m_count < chat[15]:
            print('Где-то случился уход юзера!')
            set_members_count(chats, m_count)
            from ..f_lib.other import some_leave
            
            await some_leave(chats)

#Основная функция Окончательная
async def final_any(message: types.Message):

    shield = 0
    
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
            from ..f_lib.other import restrict_chat
            await restrict_chat(message)
