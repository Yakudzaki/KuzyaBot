from loader import dp, bot
from aiogram import types
from random import randint, choice
import time
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter
from .mats import *
from settings import *
import html
from .other import similaring, matex

                
#АНТИРЕКЛАМА

async def text_shield(message: types.Message, mrm, cor_tx, user_in_base, userwarn):
    ent = 0
    for entity in message.entities:
        ent = ent + 1
    if ent == 0:
        return
    else:
        repost = 0
        users = message.from_user
        if message.forward_from_chat:
            try:
                if message.forward_from_chat.id not in whitelist:
                    repost = 1
            except:
                pass
        if message.forward_from:
            try:
                if message.forward_from.id not in whitelist:   
                    repost = 1
            except:
                pass
        if message.forward_sender_name:
                repost = 1
        ignore = 0
        if repost == 1: #проверка на репост.
            etype = ["url", "text_link", "mention", "text_mention"] #Правила для репоста
            stop = await anti_advert_t(message, etype, user_in_base, userwarn)
            ignore = 1
            if stop != None:
                return stop
        if not ignore:
            if user_in_base == False:
                if ent > 2:
                    etype = ["url", "text_link", "mention", "text_mention"] #Правила для особо новых юзеров, если они сделали более двух кликабельных ссылок
                    stop = await anti_advert_t(message, etype, user_in_base, userwarn)  
                    ignore = 1
                    if stop != None:
                        return stop
                
                if mrm == True and ent > 1 and not ignore:
                    etype = ["url", "text_link", "mention", "text_mention"] #Правила для особо новых юзеров, если они вставили больше одного кликабельного контента в ответ на какое либо сообщение
                    stop = await anti_advert_t(message, etype, user_in_base, userwarn)  
                    ignore = 1
                    if stop != None:
                        return stop
                
                if not ignore and message.text != None:
                    trigger_words = ['ссылк', 'проходит', 'ссылка', 'пройдит', 'ссылка', 'проходите', 'пройдите']
                    
                    for word in trigger_words:
                        if word in message.text.lower():
                            etype = ["url", "text_link", "mention", "text_mention"]
                            stop = await anti_advert_t(message, etype, user_in_base, userwarn) 
                            ignore = 1
                            if stop != None:
                                return stop
                    
                    if not ignore:
                        message_split = message.text.lower().split()
                        for word in message_split:
                            if len(word) > 4:
                                if similaring(word, trigger_words, 85, 2):
                                    etype = ["url", "text_link", "mention", "text_mention"]
                                    print(f"Антиреклама: Слово [{word}]")
                                    stop = await anti_advert_t(message, etype, user_in_base, userwarn) 
                                    ignore = 1
                                    if stop != None:
                                        return stop
                                else:
                                    continue
                            else:
                                continue
                if mrm == True and not ignore: #запрет кидать ссылки и упоминания в ответ на сообщения, в том числе из поста канала.
                    etype = ["text_link", "text_mention", "mention"]
                    stop = await anti_advert_t(message, etype, user_in_base, userwarn) 
                    ignore = 1
                    if stop != None:
                        return stop
            else:
                
                if userwarn[2] >= 2:
                    etype = ["url", "text_link", "mention", "text_mention", "bot_command"] #Правила для старых юзеров, если они имеют два варна.
                    stop = await anti_advert_t(message, etype, user_in_base, userwarn) 
                    ignore = 1
                    if stop != None:
                        return stop
                
                
                if ( ( mrm == True and ent > 1 ) or userwarn[2] == 1 ) and not ignore:
                    etype = ["url", "text_link", "bot_command"] #Правила для не новичков, если они делают несколько ентити в ответ или имеют один варн.
                    stop = await anti_advert_t(message, etype, user_in_base, userwarn)
                    ignore = 1
                    if stop != None:
                        return stop
                
                if mrm == True and not ignore:
                    etype = ["text_link"]
                    stop = await anti_advert_t(message, etype, user_in_base, userwarn)  #Запрет кидать гиперссылки(ссылка в виде текста) в ответ на сообщение.
                    if stop != None:
                        return stop


async def media_shield(message: types.Message, mrm, userwarn):
    ent = 0
    for entity in message.caption_entities:
        ent = ent + 1
    
    if ent == 0:
        return
    
    else:
        repost = 0
        users = message.from_user
        if message.forward_from_chat:
            try:
                if message.forward_from_chat.id not in whitelist:
                    repost = 1
            except:
                pass
        if message.forward_from:
            try:
                if message.forward_from.id not in whitelist:   
                    repost = 1
            except:
                pass
        if message.forward_sender_name:
                repost = 1
        ignore = 0
        
        user_in_base = False
        if check_user(users.id) == False:
            user_in_base = True
        
        if repost == 1: #проверка на репост.
            etype = ["url", "text_link", "mention", "text_mention"] #Правила для репоста
            stop = await anti_advert(message, etype, user_in_base, userwarn)
            ignore = 1
            if stop != None:
                return stop
        if not ignore:
            if user_in_base == False:
                
                if ent > 1:
                    etype = ["url", "text_link", "mention", "text_mention"] #Правила для особо новых юзеров, если они сделали более 1 кликабельных ссылок
                    stop = await anti_advert(message, etype, user_in_base, userwarn)  
                    ignore = 1
                    if stop != None:
                        return stop
                
                if mrm == True and not ignore: #запрет кидать ссылки в ответ на сообщения, в том числе из поста канала.
                    etype = ["url", "text_link", "mention", "text_mention"]
                    stop = await anti_advert(message, etype, user_in_base, userwarn) 
                    ignore = 1
                    if stop != None:
                        return stop
                
                if not ignore:
                    trigger_words = ['ссылк', 'проходит', 'ссылка', 'пройдит', 'ссылка', 'проходите', 'пройдите']
                    if message.text != None:
                        for word in trigger_words:
                            if word in message.text.lower():
                                etype = ["url", "text_link", "mention", "text_mention"]
                                stop = await anti_advert(message, etype, user_in_base, userwarn) 
                                ignore = 1
                                if stop != None:
                                    return stop
                        if message.text != None and not ignore:
                            message_split = message.text.lower().split()
                            for word in message_split:
                                if len(word) > 4:
                                    if similaring(word, trigger_words, 85, 2):
                                        etype = ["url", "text_link", "mention", "text_mention"]
                                        print(f"Антиреклама: Слово [{word}]")
                                        stop = await anti_advert(message, etype, user_in_base, userwarn) 
                                        ignore = 1
                                        if stop != None:
                                            return stop
                                    else:
                                        continue
                                else:
                                    continue
                    
                    if message.caption != None:
                        for word in trigger_words:
                            if word in message.caption.lower():
                                etype = ["url", "text_link", "mention", "text_mention"]
                                stop = await anti_advert(message, etype, user_in_base, userwarn) 
                                ignore = 1
                                if stop != None:
                                    return stop
                        
                        if not ignore:
                            message_split = message.caption.lower().split()
                            for word in message_split:
                                if len(word) > 4:
                                    if similaring(word, trigger_words, 85, 2):
                                        etype = ["url", "text_link", "mention", "text_mention"]
                                        print(f"Антиреклама: Слово [{word}]")
                                        stop = await anti_advert(message, etype, user_in_base, userwarn) 
                                        ignore = 1
                                        if stop != None:
                                            return stop
                                    else:
                                        continue
                                else:
                                    continue
                
                if not ignore:
                    etype = ["text_link", "text_mention", "mention"]
                    stop = await anti_advert(message, etype, user_in_base, userwarn)  #Запрет кидать гиперссылки(ссылка или упоминания) вместе с картинкой или иным медиа сообщением.
                    if stop != None:
                        return stop
            
            else:
                
                if userwarn[2] >= 2:
                    etype = ["url", "text_link", "mention", "text_mention", "bot_command"] #Правила для старых юзеров, если они имеют два варна.
                    stop = await anti_advert(message, etype, user_in_base, userwarn) 
                    ignore = 1
                    if stop != None:
                        return stop
                
                if not ignore and ( mrm == True or userwarn[2] == 1 ):
                    etype = ["url", "text_link", "bot_command"] #Правила для старых юзеров, если они отправляют сообщение в ответ. Или имеют один варн.
                    stop = await anti_advert(message, etype, user_in_base, userwarn)  
                    ignore = 1
                    if stop != None:
                        return stop
                
                if not ignore and ent > 1:
                    etype = ["url", "text_link"] #Правила для не новичков, если они делают несколько ентити за раз.
                    stop = await anti_advert(message, etype, user_in_base, userwarn)
                    ignore = 1
                    if stop != None:
                        return stop
                
                if not ignore:
                    etype = ["text_link"]
                    stop = await anti_advert(message, etype, user_in_base, userwarn)  #Запрет кидать гиперссылки(ссылка в виде текста).
                    if stop != None:
                        return stop
                


#Антибот
async def antibot(message: types.Message):
    if message.chat.type == 'private':
        return
    
  
        
    if message.forward_from:
        us2 = message.forward_from
        us1 = message.from_user
        if message.forward_from.is_bot:
            if int(us1.id) not in whitelist and us2.id != botik_id:
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    await message.answer(f"Это моя территория, <a href='tg://user?id={us1.id}'>человек</a>!")
                    return 3
                except:
                    pass
    
    if message.via_bot:
        us1 = message.from_user
        if int(us1.id) not in whitelist and us1.id != botik_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(f"Это моя территория, <a href='tg://user?id={us1.id}'>бот</a>!")
            return 3
    if message.user_shared:
        us1 = message.from_user
        if int(us1.id) not in whitelist and us1.id != botik_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(f"Это моя территория, <a href='tg://user?id={us1.id}'>человек</a>!")
            return 3
    if message.chat_shared:
        us1 = message.from_user
        if int(us1.id) not in whitelist and us1.id != botik_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(f"Это моя территория, <a href='tg://user?id={us1.id}'>человек</a>!")
            return 3
    
    if message.game:
        us1 = message.from_user
        if int(us1.id) not in whitelist and us1.id != botik_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(f"Это моя территория, <a href='tg://user?id={us1.id}'>человек</a>!")
            return 3
            
    return
        



#АНТИРЕКЛАМА МЕДИА
async def anti_advert(message: types.Message, etype, user_in_base, userwarn):

    if message.chat.type == 'private':
        return

    for entity in message.caption_entities:
        user = message.from_user
        
        if entity.type in etype:
            if user.id in whitelist:
                await message.answer(f"Засвидетельствовано сообщение с {entity.type} от кого-то Великого!")
                return
            
            else:
                users = message.from_user
                if user_in_base == False:
                    try:
                        await bot.delete_message(message.chat.id, message.message_id)
                        # await message.answer(f"Было удалено сообщение с {entity.type} от неизвестного!")
                        return 1
                    except:
                        admins = await message.chat.get_administrators()
                        msg = str("🚨 Так как у меня нет прав банить пользователя и удалять сообщения, вызываю админов!\n\n")
                        for admin in admins:
                            if admin.user.is_bot:
                                continue
                            if admin.user.username == topa_username:   #исключение из команды вызова самого Топы (Кто еще будет?)
                                continue
                            nick = html.escape(admin.user.first_name)
                            msg += f"<a href='tg://user?id={admin.user.id}'>{nick}</a>\n"
                        await message.reply(msg)
                        return
                else:
                    userrek = get_user(users.id)
                       
                    
                    if userrek[5] >= reprekl and userwarn[2] == 0:
                        await message.answer(f"Засвидетельствовано сообщение с {entity.type} от <a href='tg://user?id={user.id}'>человека</a> с высокой репутацией!")
                        return
                    else:
                        try:
                            await bot.delete_message(message.chat.id, message.message_id)
                            await message.answer(f"Было удалено сообщение с {entity.type}!")
                            return 1
                        except:
                            admins = await message.chat.get_administrators()
                            msg = str("🚨 Так как у меня нет прав банить пользователя и удалять сообщения, вызываю админов!\n\n")
                            for admin in admins:
                                if admin.user.is_bot:
                                    continue
                                if admin.user.username == topa_username:   #исключение из команды вызова самого Топы (Кто еще будет?)
                                    continue
                                nick = html.escape(admin.user.first_name)
                                msg += f"<a href='tg://user?id={admin.user.id}'>{nick}</a>\n"
                            await message.reply(msg)
                            return
                            

#ПОЛНАЯ АНТИРЕКЛАМА_ТЕКСТ
async def anti_advert_t(message: types.Message, etype, user_in_base, userwarn):

    if message.chat.type == 'private':
        return
    

    for entity in message.entities:
        user = message.from_user
        
        if entity.type in etype:
            if user.id in whitelist:
                await message.answer(f"Засвидетельствовано сообщение с {entity.type} от кого-то Великого!")
                return
            
            else:
                users = message.from_user
                if user_in_base == False:
                    try:
                        await bot.delete_message(message.chat.id, message.message_id)
                        # await message.answer(f"Было удалено сообщение с {entity.type} от неизвестного!")
                        return 1
                    except:
                        admins = await message.chat.get_administrators()
                        msg = str("🚨 Так как у меня нет прав банить пользователя и удалять сообщения, вызываю админов!\n\n")
                        for admin in admins:
                            if admin.user.is_bot:
                                continue
                            if admin.user.username == topa_username:   #исключение из команды вызова самого Топы (Кто еще будет?)
                                continue
                            nick = html.escape(admin.user.first_name)
                            msg += f"<a href='tg://user?id={admin.user.id}'>{nick}</a>\n"
                        await message.reply(msg)
                        return
                else:
                    userrek = get_user(users.id)
                    
                    if userrek[5] >= reprekl and userwarn[2] == 0:
                        await message.answer(f"Засвидетельствовано сообщение с {entity.type} от <a href='tg://user?id={user.id}'>человека</a> с высокой репутацией!")
                        return
                    else:
                        try:
                            await bot.delete_message(message.chat.id, message.message_id)
                            await message.answer(f"Было удалено сообщение с {entity.type}!")
                            return 1
                        except:
                            admins = await message.chat.get_administrators()
                            msg = str("🚨 Так как у меня нет прав банить пользователя и удалять сообщения, вызываю админов!\n\n")
                            for admin in admins:
                                if admin.user.is_bot:
                                    continue
                                if admin.user.username == topa_username:   #исключение из команды вызова самого Топы (Кто еще будет?)
                                    continue
                                nick = html.escape(admin.user.first_name)
                                msg += f"<a href='tg://user?id={admin.user.id}'>{nick}</a>\n"
                            await message.reply(msg)
                            return
                            


#АНТИМАТ КОД
async def anti_mat(message: types.Message, vermat, matrep, secmat, matnote, user_in_base):
    
    if message.from_user.id == 777000:
        return
    
    mat_in = False
    
    if message.text:
        if matex(message.text.lower()) == True:
            mat_in = True
    
    elif message.caption:
        if matex(message.caption.lower()) == True:
            mat_in = True

#Код антимата
    if mat_in == True:
        users = message.from_user
        
        if message.chat.type == 'private':
            return
        
        if matrep == 1:
            if user_in_base == False:
                create_user_main(users.id, users.username, users.first_name)
        
        user = message.from_user
        result = randint(1, 99)
        if result > vermat:
            return
        if result <= vermat and secmat >= 60:
            try:
                await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user.id,
                                   permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False), until_date=int(time.time() + secmat))
            except:
                if vermat <= matnote and user.id not in no_rp_list: #(список служебных ботов админского типа)
                    await message.answer(f"<a href='tg://user?id={user.id}'>Нарушитель</a> пойман на мате!", parse_mode='html')
                    await message.reply("Я понимаю, что материться может быть весело, но ты ведь знаешь, что я не смогу тебя замутить?")
                    if matrep == 1:
                        badu = message.from_user
                        take_rep(badu.id)
                        await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
                    return
                return
            
            
            if user.id not in no_rp_list:           #(список служебных ботов админского типа)
                await message.answer(f"<a href='tg://user?id={user.id}'>Нарушитель</a> пойман на мате!", parse_mode='html')
                userd = get_user(message.from_user.id)
                await bot.send_message(text=f"<a href='tg://user?id={userd[0]}'>{html.escape(userd[2])}</a> замучивается на {secmat} сек.\nПричина: Мат!", chat_id=message.chat.id, parse_mode='html')
                if matrep == 1:
                    badu = message.from_user
                    take_rep(badu.id)
                    await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
            
            else:
                if vermat <= matnote:
                    await message.answer(f"<a href='tg://user?id={user.id}'>Нарушитель</a> пойман на мате!", parse_mode='html')
                    await message.reply("Я понимаю, что материться может быть весело, но ты ведь знаешь, что я не смогу тебя замутить?")
                    if matrep == 1:
                        badu = message.from_user
                        take_rep(badu.id)
                        await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")    
            return
        
        if result <= vermat and secmat < 60: #
            adminse = await message.chat.get_administrators()  #admino = 1, если юзер админ, и 0 если не админ.
            admino = 0
            for admin in adminse:
                if admin.user.id == user.id:
                    admino = 1
                    continue
            
            
            
            if admino == 0 and user.id not in no_rp_list: # Не админы
                await message.answer(f"<a href='tg://user?id={user.id}'>Нарушитель</a> пойман на мате!", parse_mode='html')
                if matrep == 1:
                    badu = message.from_user
                    take_rep(badu.id)
                    await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
                return
            
            
            
            if admino == 0 and user.id in no_rp_list and vermat <= matnote: #Админы
                await message.answer(f"<a href='tg://user?id={user.id}'>Нарушитель</a> пойман на мате!", parse_mode='html')
                if matrep == 1:
                    badu = message.from_user
                    take_rep(badu.id)
                    await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
                return
            
            if admino == 0 and user.id in no_rp_list and vermat > matnote: #админы
                return
            
            
            if admino == 1 and vermat <= matnote: #Админы
                await message.answer(f"<a href='tg://user?id={user.id}'>Нарушитель</a> пойман на мате!", parse_mode='html')
                if matrep == 1:
                    badu = message.from_user
                    take_rep(badu.id)
                    await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
                return

            if admino == 1 and vermat > matnote: #админ
                return

