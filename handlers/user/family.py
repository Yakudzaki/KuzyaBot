from loader import dp, bot
from aiogram import types
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import re
from aiogram.dispatcher.filters import IsReplyFilter
from ..f_lib.other import message_user_get
from utils.db import *
import html
from .base_text import final_text

@dp.message_handler(commands=["загс"], commands_prefix="/!.")
async def rp_spis(message: types.Message):
    nick = html.escape(message.from_user.first_name)
    await message.reply(f"<a href='tg://user?id={message.from_user.id}'>{nick}</a>, вот список команд для постройки отношений:\n\n\
▷ <code>Брак</code> — Сделать предложение брака или согласиться на него. Отправлять по правилам РП команд.\n\
▷ <code>Развод</code> — Отозвать предложение брака, или разорвать его со своей стороны. Отправлять по правилам РП команд.\n\
▷ <code>Сойтись</code> — Сделать предложение интимных отношений или согласиться на него. Отправлять по правилам РП команд.\n\
▷ <code>Бросить</code> — Отозвать предложение интимных отношений, или разорвать его со своей стороны. Отправлять по правилам РП команд.\n\
▷ <code>Брад</code> — Сделать предложение породниться или согласиться на него. Отправлять по правилам РП команд.\n\
▷ <code>Небрад</code> — Отозвать предложение родственной связи, или разорвать её со своей стороны. Отправлять по правилам РП команд.\n\
▷ <code>Отклонить</code> — Разорвать все отношения с другим пользователем. Отправлять по правилам РП команд.\n\
▷ <code>Отношения</code> — Узнать своё реальное семейное положение. Если написать в ответ на чужое сообщение, то Кузя расскажет уже не про вас.\n\
▷ <code>Предложения</code> — Узнать своё возможное семейное положение. Если написать в ответ на чужое сообщение, то Кузя расскажет уже не про вас.\n\
▷ <code>Бросить всех</code> — Отозвать все предложения и расторгнуть все отношения со своей стороны.\n")


#ТВОЯ/МОЯ Семья
@dp.message_handler(lambda message: message.text.lower() == "предложения")
async def my_family(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.reply_to_message:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        us = message.reply_to_message.from_user
        user = create_user(us.id, us.username, us.first_name)
        msg = "💍 Ваша семья потенциально состоит из:\n\n"
        alone = 0


#ЛЮБОВНИКИ
        bradstvo = get_wlovers(user[0])
        for tup in bradstvo:
            if tup != 0 and tup != None:
                for brad in tup:
                    user2 = get_user(brad)
                    msg += f"<a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> хочет стать {str(user2[4]).replace('1', 'вашим любовником').replace('2', 'вашей любовницей').replace('0', 'вашим секс-партнером').replace('3', 'вашим секс-партнером').replace('4', 'вашим секс-партнером')}\n"
                    alone = 1
        bradoses = get_wloves(user[0])
        for tup in bradoses:
            if tup != 0 and tup != None:
                for brad in tup:
                    if brad != 0 and brad != None:
                        user2 = get_user(brad)
                        msg += f"Вами предложено <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> стать {str(user2[4]).replace('1', 'вашим  любовником').replace('2', 'вашей любовницей').replace('0', 'вашим секс-партнером').replace('3', 'вашим секс-партнером').replace('4', 'вашим секс-партнером')}\n"
                        alone = 1


#СУПРУГИ
        bradstvo = get_wmarryers(user[0])
        for tup in bradstvo:
            if tup != 0 and tup != None:
                for brad in tup:
                    user2 = get_user(brad)
                    msg += f"<a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> хочет стать {str(user2[4]).replace('1', 'вашим мужем').replace('2', 'вашей женой').replace('0', 'вашим супругом').replace('3', 'вашим супругом').replace('4', 'вашим супругом')}\n"
                    alone = 1
        bradoses = get_wmarrys(user[0])
        for tup in bradoses:
            if tup != 0 and tup != None:
                for brad in tup:
                    if brad != 0 and brad != None:
                        user2 = get_user(brad)
                        msg += f"Вами предложено <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> стать {str(user2[4]).replace('1', 'вашим  мужем').replace('2', 'вашей женой').replace('0', 'вашим супругом').replace('3', 'вашим супругом').replace('4', 'вашим супругом')}\n"
                        alone = 1


#БРАДЫ!!!
        bradstvo = get_wsiblers(user[0])
        for tup in bradstvo:
            if tup != 0 and tup != None:
                for brad in tup:
                    user2 = get_user(brad)
                    msg += f"<a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> хочет стать {str(user2[4]).replace('1', 'вашим братом').replace('2', 'вашей сестрой').replace('0', 'вашим брадом').replace('3', 'вашим брадом').replace('4', 'вашим брадом')}\n"
                    alone = 1
        bradoses = get_wsibles(user[0])
        for tup in bradoses:
            if tup != 0 and tup != None:
                for brad in tup:
                    if brad != 0 and brad != None:
                        user2 = get_user(brad)
                        msg += f"Вами предложено <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> стать {str(user2[4]).replace('1', 'вашим  братом').replace('2', 'вашей сестрой').replace('0', 'вашим брадом').replace('3', 'вашим брадом').replace('4', 'вашим брадом')}\n"
                        alone = 1
        id = message.reply_to_message.message_id
        msg_info = "\n▷ <code>!Загс</code> — список команд.\n"
        if alone == 1:
            msg = msg
            await bot.send_message(message.chat.id, msg, reply_to_message_id=id)
            return
        else:
            msg = "😞 У вас нет вариантов!" + msg_info
            await bot.send_message(message.chat.id, msg, reply_to_message_id=id)


    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        msg = "💍 Ваша семья потенциально состоит из:\n\n"
        alone = 0


#ЛЮБОВНИКИ
        bradstvo = get_wlovers(user[0])
        for tup in bradstvo:
            if tup != 0 and tup != None:
                for brad in tup:
                    user2 = get_user(brad)
                    msg += f"<a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> хочет стать {str(user2[4]).replace('1', 'вашим любовником').replace('2', 'вашей любовницей').replace('0', 'вашим секс-партнером').replace('3', 'вашим секс-партнером').replace('4', 'вашим секс-партнером')}\n"
                    alone = 1
        bradoses = get_wloves(user[0])
        for tup in bradoses:
            if tup != 0 and tup != None:
                for brad in tup:
                    if brad != 0 and brad != None:
                        user2 = get_user(brad)
                        msg += f"Вами предложено <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> стать {str(user2[4]).replace('1', 'вашим  любовником').replace('2', 'вашей любовницей').replace('0', 'вашим секс-партнером').replace('3', 'вашим секс-партнером').replace('4', 'вашим секс-партнером')}\n"
                        alone = 1


#СУПРУГИ
        bradstvo = get_wmarryers(user[0])
        for tup in bradstvo:
            if tup != 0 and tup != None:
                for brad in tup:
                    user2 = get_user(brad)
                    msg += f"<a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> хочет стать {str(user2[4]).replace('1', 'вашим мужем').replace('2', 'вашей женой').replace('0', 'вашим супругом').replace('3', 'вашим супругом').replace('4', 'вашим супругом')}\n"
                    alone = 1
        bradoses = get_wmarrys(user[0])
        for tup in bradoses:
            if tup != 0 and tup != None:
                for brad in tup:
                    if brad != 0 and brad != None:
                        user2 = get_user(brad)
                        msg += f"Вами предложено <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> стать {str(user2[4]).replace('1', 'вашим  мужем').replace('2', 'вашей женой').replace('0', 'вашим супругом').replace('3', 'вашим супругом').replace('4', 'вашим супругом')}\n"
                        alone = 1


#БРАДЫ!!!
        bradstvo = get_wsiblers(user[0])
        for tup in bradstvo:
            if tup != 0 and tup != None:
                for brad in tup:
                    user2 = get_user(brad)
                    msg += f"<a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> хочет стать {str(user2[4]).replace('1', 'вашим братом').replace('2', 'вашей сестрой').replace('0', 'вашим брадом').replace('3', 'вашим брадом').replace('4', 'вашим брадом')}\n"
                    alone = 1
        bradoses = get_wsibles(user[0])
        for tup in bradoses:
            if tup != 0 and tup != None:
                for brad in tup:
                    if brad != 0 and brad != None:
                        user2 = get_user(brad)
                        msg += f"Вами предложено <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> стать {str(user2[4]).replace('1', 'вашим  братом').replace('2', 'вашей сестрой').replace('0', 'вашим брадом').replace('3', 'вашим брадом').replace('4', 'вашим брадом')}\n"
                        alone = 1
        msg_info = "\n▷ <code>!Загс</code> — список команд.\n"
        if alone == 1:
            msg = msg
            await message.reply(msg)
            return
        else:
            msg = "😞 У вас нет вариантов!" + msg_info
            await message.reply(msg)


#ТВОЯ/МОЯ Семья
@dp.message_handler(lambda message: message.text.lower() == "отношения")
async def my_family(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.reply_to_message:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        us = message.reply_to_message.from_user
        user = create_user(us.id, us.username, us.first_name)
        msg = "💍 Ваша семья состоит из:\n\n"
        alone = 0


#ЛЮБОВНИКИ   
        brads = get_love(user[0])
        for tup in brads:
            for brad in tup:
                if brad != user[0]:
                    user2 = get_user(brad)
                    msg += f"{str(user2[4]).replace('1', 'Любовник').replace('2', 'Любовница').replace('0', 'Секс-парнтнер').replace('3', 'Секс-парнтнер').replace('4', 'Секс-парнтнер')} - <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>\n"
                    alone = 1


#СУПРУГИ
        brads = get_marry(user[0])
        for tup in brads:
            for brad in tup:
                if brad != user[0]:
                    user2 = get_user(brad)
                    msg += f"{str(user2[4]).replace('1', 'Муж').replace('2', 'Жена').replace('0', 'Супруг').replace('3', 'Супруг').replace('4', 'Супруг')} - <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>\n"
                    alone = 1


#БРАДЫ!!!
        brads = get_sibl(user[0])
        for tup in brads:
            for brad in tup:
                if brad != user[0]:
                    user2 = get_user(brad)
                    msg += f"{str(user2[4]).replace('1', 'Брат').replace('2', 'Сестра').replace('0', 'Брад').replace('3', 'Брад').replace('4', 'Брад')} - <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>\n"
                    alone = 1
        id = message.reply_to_message.message_id
        msg_info = "\n▷ <code>!Загс</code> — список команд.\n"
        if alone == 1:
            msg = msg
            await bot.send_message(message.chat.id, msg, reply_to_message_id=id)
            return
        else:
            msg = "😞 Вы одиноки!" + msg_info
            await bot.send_message(message.chat.id, msg, reply_to_message_id=id)


    else:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        msg = "💍 Ваша семья состоит из:\n\n"
        alone = 0


#ЛЮБОВНИКИ
        brads = get_love(user[0])
        if brads != None and brads != 0:
            for tup in brads:
                for brad in tup:
                    if brad != user[0]:
                        user2 = get_user(brad)
                        msg += f"{str(user2[4]).replace('1', 'Любовник').replace('2', 'Любовница').replace('0', 'Секс-парнтнер').replace('3', 'Секс-парнтнер').replace('4', 'Секс-парнтнер')} - <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>\n"
                        alone = 1


#СУПРУГИ
        brads = get_marry(user[0])
        if brads != None and brads != 0:
            for tup in brads:
                for brad in tup:
                    if brad != user[0]:
                        user2 = get_user(brad)
                        msg += f"{str(user2[4]).replace('1', 'Муж').replace('2', 'Жена').replace('0', 'Супруг').replace('3', 'Супруг').replace('4', 'Супруг')} - <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>\n"
                        alone = 1


#БРАДЫ!!!
        brads = get_sibl(user[0])
        if brads != None and brads != 0:
            for tup in brads:
                for brad in tup:
                    if brad != user[0]:
                        user2 = get_user(brad)
                        msg += f"{str(user2[4]).replace('1', 'Брат').replace('2', 'Сестра').replace('0', 'Брад').replace('3', 'Брад').replace('4', 'Брад')} - <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>\n"
                        alone = 1
        msg_info = "\n▷ <code>!Загс</code> — список команд.\n"
        if alone == 1:
            msg = msg
            await message.reply(msg)
            return
        else:
            msg = "😞 Вы одиноки!" + msg_info
            await message.reply(msg)


#Брак
@dp.message_handler(lambda message: message.text.lower().startswith("брак ") or message.text.lower() == "брак")
async def marry(message: types.Message):
    if message.text.lower() != "брак":
        stop = await final_text(message)
        if stop != None:
            return
    
        if message.reply_to_message:
            if len(message.text.split()) > 1:
                return
            elif message.reply_to_message.from_user.id in no_rp_list:
                return
        elif message.entities:
            ent = False
            leng = 0
            offs = 0
            for entity in message.entities:
                if entity.type in ["text_mention", "mention"]:
                    ent = True
                    leng = len(message.text[entity.offset + entity.length:])
                    offs = entity.offset
                    break
                else:
                    continue
            if ent == False:
                return
            elif leng > 0:
                return
            elif offs > 6:
                return
        else:
            return
    
    
    
    user2 = await message_user_get(message)
    if user2 == None:
        return
    
    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        if check_marry(user[0], user2[0]) == False:
            if user[0] == user2[0]:
                await message.reply(f"❌ Невозможно вступить в отношения.")
                return
            if check_wmarry(user[0], user2[0]):
                await message.reply("❌ Предложение брака уже было сделано ранее!")
                return
            if check_wmarry(user2[0], user[0]) == False:
                create_wmarry(user[0], user2[0])
                await message.reply(f"❤️ Брак <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> успешно предложен!\nЧтобы согласиться, нужно сделать встречное предложение.")
                return
            if check_wmarry(user2[0], user[0]):
                delete_wmarry(user2[0], user[0])
                create_marry(user[0], user2[0])
                if check_love(user[0], user2[0]):
                    delete_love(user[0], user2[0])
                if check_wlove(user[0], user2[0]):
                    delete_wlove(user[0], user2[0])
                if check_wlove(user2[0], user[0]):
                    delete_wlove(user2[0], user[0])
                await message.reply(f"❤️ Брак c <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> успешно заключен!")
                return
        if check_marry(user[0], user2[0]):
            await message.reply(f"❌ Вы уже в официальном браке.")
            return

    
#Развод
@dp.message_handler(lambda message: message.text.lower().startswith("развод ") or message.text.lower() == "развод")
async def marry(message: types.Message):
    if message.text.lower() != "развод":
        stop = await final_text(message)
        if stop != None:
            return
        
        if message.reply_to_message:
            if len(message.text.split()) > 1:
                return
            elif message.reply_to_message.from_user.id in no_rp_list:
                return
        elif message.entities:
            ent = False
            leng = 0
            offs = 0
            for entity in message.entities:
                if entity.type in ["text_mention", "mention"]:
                    ent = True
                    leng = len(message.text[entity.offset + entity.length:])
                    offs = entity.offset
                    break
                else:
                    continue
            if ent == False:
                return
            elif leng > 0:
                return
            elif offs > 8:
                return
        else:
            return
    
    user2 = await message_user_get(message)
    if user2 == None:
        return
    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        if check_marry(user[0], user2[0]) == False:
            if check_wmarry(user[0], user2[0]) == False:
                await message.reply(f"❌ Нечего расторгать с <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>!")
                return
        if check_wmarry(user[0], user2[0]):
            delete_wmarry(user[0], user2[0])
            await message.reply(f"💔 Предложение брака <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> расторгнуто!")
            return
        if check_marry(user[0], user2[0]):
            delete_marry(user[0], user2[0])
            await message.reply(f"💔 Брак c <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> успешно расторгнут вами!")
            return


#ГРАЖДАНСКИЙ Брак
@dp.message_handler(lambda message: message.text.lower().startswith("сойтись ") or message.text.lower() == "сойтись")
async def marry(message: types.Message):
    if message.text.lower() != "сойтись":
        stop = await final_text(message)
        if stop != None:
            return
    
        if message.reply_to_message:
            if len(message.text.split()) > 1:
                return
            elif message.reply_to_message.from_user.id in no_rp_list:
                return
        elif message.entities:
            ent = False
            leng = 0
            offs = 0
            for entity in message.entities:
                if entity.type in ["text_mention", "mention"]:
                    ent = True
                    leng = len(message.text[entity.offset + entity.length:])
                    offs = entity.offset
                    break
                else:
                    continue
            if ent == False:
                return
            elif leng > 0:
                return
            elif offs > 9:
                return
        else:
            return
    
    
    user2 = await message_user_get(message)
    if user2 == None:
        return
    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        if user[0] == user2[0]:
            await message.reply(f"❌ Невозможно вступить в отношения.")
            return
        if check_love(user[0], user2[0]) == False:
            if check_marry(user[0], user2[0]):
                await message.reply(f"❌ Вы уже в официальном браке.")
                return
            if check_wlove(user[0], user2[0]):
                await message.reply("❌ Предложение интима уже было сделано ранее!")
                return
            if check_wlove(user2[0], user[0]) == False:
                create_wlove(user[0], user2[0])
                await message.reply(f"❤️ Интим <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> успешно предложен!\nЧтобы согласиться, нужно сделать встречное предложение.")
                return
            if check_wlove(user2[0], user[0]):
                delete_wlove(user2[0], user[0])
                create_love(user[0], user2[0])
                await message.reply(f"❤️ Гражданский брак c <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> успешно заключен!")
                return
        if check_love(user[0], user2[0]):
            await message.reply(f"❌ Вы уже в гражданском браке.")
            return


#ГРАЖДАНСКИЙ Развод
@dp.message_handler(lambda message: message.text.lower().startswith("бросить ") or message.text.lower() == "бросить")
async def marry(message: types.Message):
    if message.text.lower() != "бросить":
        stop = await final_text(message)
        if stop != None:
            return
        
        if message.reply_to_message:
            if len(message.text.split()) > 1:
                return
            elif message.reply_to_message.from_user.id in no_rp_list:
                return
        elif message.entities:
            ent = False
            leng = 0
            offs = 0
            for entity in message.entities:
                if entity.type in ["text_mention", "mention"]:
                    ent = True
                    leng = len(message.text[entity.offset + entity.length:])
                    offs = entity.offset
                    break
                else:
                    continue
            if ent == False:
                return
            elif leng > 0:
                return
            elif offs > 9:
                return
        else:
            return
    
    
    user2 = await message_user_get(message)
    if user2 == None:
        return
    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        if check_wlove(user[0], user2[0]) == False:
            if check_love(user[0], user2[0]) == False:
                await message.reply(f"❌ Нечего расторгать с <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>!")
                return
        if check_wlove(user[0], user2[0]):
            delete_wlove(user[0], user2[0])
            await message.reply(f"💔 Предложение интима <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> расторгнуто!")
        if check_love(user[0], user2[0]):
            delete_love(user[0], user2[0])
            await message.reply(f"💔 Гражданский брак c <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a> успешно расторгнут вами!")
        return


#БРОСИТЬ ВСЕХ
@dp.message_handler(lambda message: message.text.lower() == "бросить всех")
async def my_family(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    us = message.from_user
    user = create_user(us.id, us.username, us.first_name)
    delete_all_marry(user[0])
    delete_all_love(user[0])
    delete_all_sibl(user[0])
    delete_all_wmarry(user[0])
    delete_all_wlove(user[0])
    delete_all_wsibl(user[0])
    msg = "Вы всех послали!"
    await message.reply(msg)


#РАЗРЫВ СВЯЗЕЙ
@dp.message_handler(lambda message: message.text.lower().startswith("отклонить ") or message.text.lower() == "отклонить")
async def marry(message: types.Message):
    if message.text.lower() != "отклонить":
        stop = await final_text(message)
        if stop != None:
            return
        
        if message.reply_to_message:
            if len(message.text.split()) > 1:
                return
            elif message.reply_to_message.from_user.id in no_rp_list:
                return
        elif message.entities:
            ent = False
            leng = 0
            offs = 0
            for entity in message.entities:
                if entity.type in ["text_mention", "mention"]:
                    ent = True
                    leng = len(message.text[entity.offset + entity.length:])
                    offs = entity.offset
                    break
                else:
                    continue
            if ent == False:
                return
            elif leng > 0:
                return
            elif offs > 11:
                return
        else:
            return
    
    
    user2 = await message_user_get(message)
    if user2 == None:
        return
    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        delete_all_marry(user[0])
        delete_all_love(user[0])
        delete_all_sibl(user[0])
        delete_all_wmarry(user[0])
        delete_all_wlove(user[0])
        delete_all_wsibl(user[0])
        delete_wlove(user2[0], user[0])
        delete_wsibl(user2[0], user[0])
        delete_wmarry(user2[0], user[0])
        await message.reply(f"Вы успешно исчезли со всех радаров <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>!")


#БРАД ТЫ МНЕ
@dp.message_handler(lambda message: message.text.lower().startswith("брад ") or message.text.lower() == "брад")
async def marry(message: types.Message):
    if message.text.lower() != "брад":
        stop = await final_text(message)
        if stop != None:
            return
        
        if message.reply_to_message:
            if len(message.text.split()) > 1:
                return
            elif message.reply_to_message.from_user.id in no_rp_list:
                return
        elif message.entities:
            ent = False
            leng = 0
            offs = 0
            for entity in message.entities:
                if entity.type in ["text_mention", "mention"]:
                    ent = True
                    leng = len(message.text[entity.offset + entity.length:])
                    offs = entity.offset
                    break
                else:
                    continue
            if ent == False:
                return
            elif leng > 0:
                return
            elif offs > 6:
                return
        else:
            return
    
    
    user2 = await message_user_get(message)
    if user2 == None:
        return
    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        if user[0] == user2[0]:
            await message.reply("<b>❌ Вы по умолчанию родственны сами себе!</b>")
            return
        if check_wsibl(user[0], user2[0]):
            await message.reply("<b>❌ Вы уже предложили ранее родственные отношения!</b>")
            return
        if check_sibl(user[0], user2[0]):
            await message.reply("<b>❌ Вы уже состоите в родственных отношениях!</b>")
            return
        if check_wsibl(user2[0], user[0]) == False:
            create_wsibl(user[0], user2[0])
            await message.reply(f"<b>✅ Вы успешно предложили породниться <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>!</b>\nЧтобы согласиться, нужно сделать встречное предложение.")
            return
        if check_wsibl(user2[0], user[0]):
            delete_wsibl(user2[0], user[0])
            create_sibl(user[0], user2[0])
            await message.reply(f"<b>🫂 Вы успешно породнились с <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>!</b>")
            return


#НЕ БРАД
@dp.message_handler(lambda message: message.text.lower().startswith("небрад ") or message.text.lower() == "небрад")
async def marry(message: types.Message):
    if message.text.lower() != "небрад":
        stop = await final_text(message)
        if stop is not None:
            return

        if message.reply_to_message:
            if len(message.text.split()) > 1:
                return
            elif message.reply_to_message.from_user.id in no_rp_list:
                return
        elif message.entities:
            ent = False
            leng = 0
            offs = 0
            for entity in message.entities:
                if entity.type in ["text_mention", "mention"]:
                    ent = True
                    leng = len(message.text[entity.offset + entity.length:])
                    offs = entity.offset
                    break
                else:
                    continue
            if ent == False:
                return
            elif leng > 0:
                return
            elif offs > 8:
                return
        else:
            return
    
    
    user2 = await message_user_get(message)
    if user2 == None:
        return
    else:
        us = message.from_user
        user = create_user(us.id, us.username, us.first_name)
        if check_wsibl(user[0], user2[0]) == False:
            if check_sibl(user[0], user2[0]) == False:
                await message.reply(f"<b>🚫 Нечего отзывать и разрывать!</b>")
                return
        if check_wsibl(user[0], user2[0]):
            delete_wsibl(user[0], user2[0])
            await message.reply(f"<b>🚫 Вы успешно отозвали предложение родственных отношений с <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>!</b>")
        if check_sibl(user[0], user2[0]):
            delete_sibl(user[0], user2[0])
            await message.reply(f"<b>🚫 Вы успешно разорвали родственные отношения с <a href='tg://user?id={user2[0]}'>{html.escape(user2[2])}</a>!</b>")
