from loader import dp, bot
from aiogram import types
from random import randint, choice
import time

from utils.db.db_utils_users import *
from utils.db.db_utils_сhats import *
from utils.db.db_utils_members import *
from utils.db.db_utils_warning import *
from utils.db.relations.db_utils_moniker import *

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter

from settings import *
import html
import logging

#pip install fuzzywuzzy
#pip install python-Levenshtein
from fuzzywuzzy import process, utils, fuzz
from ..f_lib.other import morph_word, years_letter, as_del_msg, botik_leave_chat

#точное соответствие
bad = ["-", "--", "---", "----", "фу", "фуу", "фууу", "фу!", "гавно", "гавно!", "дерьмо", "дерьмо!", "диз", "дизлайк", "👎", "👎👎", "кринж", "кринжатина", "осужд", "осуждаю", "асужд", "асуждаю", "гандон", "гнида", "сука", "чмо", "недостоин", "осу", "асу", "👎🏻", "👎🏻👎🏻", "👎🏼", "👎🏼👎🏼", "👎🏽", "👎🏽👎🏽", "👎🏾", "👎🏾👎🏾", "👎🏽", "👎🏿👎🏿", "страшный"] 

good = ["спасибо", "спасибо большое", "большое спасибо", "благодарю", "благодарствую", "респект", "респект!", "спс", "уважуха", "+", "++", "+++", "++++", "харош", "харош!", "хорош", "уважаю", "👍", "👍🏻", "👍🏼", "👍🏽", "👍🏾", "👍🏿", "👍👍", "👍🏻👍🏻", "👍🏼👍🏼", "👍🏽👍🏽", "👍🏾👍🏾", "👍🏿👍🏿", "одобр", "круто", "круто!", "молодец", "молодец!", "гений", "гений!", "согл", "согласен", "достоин", "мегахарош", "мегахорош", "вау", "вау!", "одобряю", "одобрено", "🫡", "🫡🫡", "f", "ff", "f!", "ff!", "f!!", "ff!!"]



#неточное соответствие
bad2 = ["фуу", "фууу", "гавно", "дерьмо", "диз", "дизлайк", "кринж", "осужд", "осуждаю", "асужд", "асуждаю", "гандон", "гнида", "сука", "чмо", "недостоин", "страшн", "ужас", "злоб"]
    
good2 = ["спасибо", "благодар", "респект", "спс", "уважуха", "харош", "хорош", "уважаю", "одобр", "круто", "молодец", "гений", "согл", "согласен", "достоин", "мегахарош", "мегахорош", "вау"]




who = ["кто ты", "ты кто", "кто ты?", "ты кто?", "а ты кто?", "а кто ты?", "а ты кто", "а кто ты", "ты вообще кто", "ты, вообще, кто?", "ты кто такой?", "кто ты такой", "ты, вообще, кто такой?", "кто ты, вообще, такой?"]

whoiam = ["профиль", "кто я", "кто я?", "я кто", "я кто?", "а кто я", "кто я такой?", "я кто такой?", "кто я такой?", "а я кто?", "я вообще кто", "я, вообще, кто?", "кто я, вообще, такой?", "кто я вообще такой"]


#Мои Варны
@dp.message_handler(lambda message: message.text.lower() == "мои варны")
async def my_warns(message: types.Message):
    
    if message.chat.type == 'private':
        return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    us = message.from_user
    create_user(us.id, us.username, us.first_name)
    

    create_warner(message.chat.id, us.id)
    userwarn = get_warner(message.chat.id, us.id)
    
    await message.reply(f"Количество ваших варнов - {userwarn[2]}")
    return

#Мой баланс
@dp.message_handler(lambda message: message.text.lower() == "баланс")
async def my_balance(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    
    users = message.from_user
    user = create_user(users.id, users.username, users.first_name)
    
    msg = await message.reply(f"💰| Количество ваших кузиров - <b>{user[11]}</b>")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    await as_del_msg(message.chat.id, message.message_id, time_del)

#Чужие варны
@dp.message_handler(lambda message: message.text.lower() == "варны")
async def your_warns(message: types.Message):
    if message.chat.type == 'private':
        return
    us = message.from_user
    adminse = await message.chat.get_administrators()
    admino = 0
    for admin in adminse:
        if admin.user.id == us.id:
            admino = 1
            continue
    if message.reply_to_message:
        rep = message.reply_to_message.from_user
        
        create_user(rep.id, rep.username, rep.first_name)
        
        us = message.from_user
        
        if admino == 1:
            

            create_warner(message.chat.id, rep.id)
            userwarn = get_warner(message.chat.id, rep.id)
            
            id = message.reply_to_message.message_id
            await bot.send_message(message.chat.id, f"Количество варнов пользователя - {userwarn[2]}", reply_to_message_id=id)
    else:
        if admino == 1:
            await message.reply("❌ Это сообщение должно быть ответом на сообщение!")
        return


#Свой пол
@dp.message_handler(lambda message: message.text.lower() == "пол")
async def my_gender(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    users = message.from_user

    user = create_user(users.id, users.username, users.first_name)
    
    msg = await message.reply(f"🚻 Твой пол - {str(user[4]).replace('1', 'Мужской').replace('2', 'Женский').replace('0', '[-]').replace('3', str(html.escape(user[7]))).replace('4', str(html.escape(user[7])))}\n\n<code>+пол</code> текст - вписать пол")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    return


@dp.message_handler(lambda message: message.text.lower() == "вид")
async def my_gender(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    users = message.from_user
    
    user = create_user(users.id, users.username, users.first_name)
    msg = await message.reply(f"♾ Твой вид - {str(user[4]).replace('1', str(html.escape(user[7]))).replace('2', str(html.escape(user[7]))).replace('0', str(html.escape(user[7]))).replace('3', 'Иной').replace('4', 'Чеширский')}\n\n<code>+вид</code> текст - вписать вид")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    return



#Своё био
@dp.message_handler(lambda message: message.text.lower() == "био")
async def my_bio(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    users = message.from_user

    user = create_user(users.id, users.username, users.first_name)
    msg = await message.reply(f"📝 Твоё био - {html.escape(user[3])}\n\n<code>+био</code> текст - заполнить био")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    return



#Свой ник
@dp.message_handler(lambda message: message.text.lower() == "ник")
async def my_nick(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    users = message.from_user

    user = create_user(users.id, users.username, users.first_name)
    nicks = morph_word(user[0], user[2], user[4])
    msg = await message.reply(f"🏷️ Твой ник - {html.escape(user[2])}\n—\nПадежи:\
    \n{html.escape(nicks[0])} — именительный. (<code>+ник-и</code> ник)\
    \n{html.escape(nicks[1])} — родительный. (<code>+ник-р</code> ник)\
    \n{html.escape(nicks[2])} — дательный. (<code>+ник-д</code> ник)\
    \n{html.escape(nicks[3])} — винительный. (<code>+ник-в</code> ник)\
    \n{html.escape(nicks[4])} — творительный. (<code>+ник-т</code> ник)\
    \n{html.escape(nicks[5])} — предложный. (<code>+ник-п</code> ник)\
    \n—\
    \n<code>падежи</code> — вызвать справку по падежам.\
    \n<code>+ник</code> ник - сменить основной ник")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    return


#Своё прозвище
@dp.message_handler(lambda message: message.text.lower() == "прозвища")
async def all_monikers(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.reply_to_message:
        if message.chat.type != 'private':
            warner = get_warner(message.chat.id, message.reply_to_message.from_user.id)
            if warner == None:
                warner = [message.chat.id, message.reply_to_message.from_user.id, 0, 0, 0]
            if warner[4] != 0:
                return
        
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        id = message.reply_to_message.message_id
        us = message.reply_to_message.from_user
        user = create_user(us.id, us.username, us.first_name)
        msg = "🎭 Вот все прозвища:\n——\n"
        msg2 = ""

        if check_moniks(user[0]):
            moniks = get_all_moniks(user[0])
            for monik in moniks:
                msg2 += f"<code>{html.escape(monik[1])}</code> ({monik[2]})\n"
        else:
            msg = "🎭 Нет прозвищ.\n"
    
    else:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        us = message.from_user
        id = message.message_id

        user = create_user(us.id, us.username, us.first_name)
        
        msg = "🎭 Вот все ваши прозвища:\n——\n"
        msg2 = ""
        
        if check_moniks(user[0]):
            moniks = get_all_moniks(user[0])

            for monik in moniks:
                msg2 += f"<code>{html.escape(monik[1])}</code> ({monik[2]})\n"
        
        else:
            msg = "🎭 У вас нет прозвищ.\n"

    msg3 = "——\n<code>+ты</code> (прозвище) - сменить прозвище собеседнику."
    msg = msg + msg2 + msg3
    msg = await bot.send_message(message.chat.id, msg, reply_to_message_id=id)
    await as_del_msg(message.chat.id, msg.message_id, time_del)

#Профиль чужой
@dp.message_handler(lambda message: message.text.lower() in who)
async def your_profile(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.reply_to_message:
        
        usern = message.reply_to_message.from_user
        
        if usern.id == botik_id:
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            await message.reply("Я Кузя 🙃")
            return
        if usern.id in no_rp_list:
            return
        
        if check_user(usern.id):
            if message.reply_to_message.from_user.first_name == "":
                return
            create_user_main(usern.id, usern.username, usern.first_name)
            if usern.is_bot == True:
                set_specie(usern.id, "Бот")
            
            user = get_user(usern.id)

        else:
            username = usern.username
            if username == None:
                username = usern.id
            if message.reply_to_message.from_user.is_bot == True:
                set_specie(message.reply_to_message.from_user.id, "Бот")
            set_username(usern.id, username)
            user = get_user(usern.id)
        
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        if message.chat.type != 'private':
            try:
                if check_member(message.chat.id, usern.id) == False:
                    ment = await bot.get_chat_member(message.chat.id, usern.id)
                    if ment.status != "left" and ment.status != "kicked":
                        create_member(message.chat.id, usern.id, ment.status)
                        
            except:
                pass
                

            warner = get_warner(message.chat.id, usern.id)
            if warner == None:
                warner = [message.chat.id, usern.id, 0, 0, 0]
            if warner[4] != 0:
                return
        
        if message.chat.type == 'private':
            userwarn = ["—", "—", "—", "—"]
        else:
            userwarn = warner

        if user[6] > 100000:
            age = "Неизмеримо"
        else:
            age = str(user[6])
        
        bio = user[3]
        if bio.startswith("html: "):
            bio = bio.replace("html: ", "")
        else:
            bio = f"<em>{html.escape(bio)}</em>"
        
        name = usern.first_name
        if usern.last_name != None and usern.last_name != "":
            name = usern.first_name + " " + usern.last_name
        
        rep = await string_rep(user[5], user[4])
        response_text = f"Это пользователь <a href='tg://user?id={user[0]}'>{html.escape(name)}</a>\
        \n\n<b>🆔 ID</b>: <code>{user[0]}</code>\
        \n<b>👤 Username</b>: @{user[1]}\
        \n<b>🏷️ Ник</b>: {html.escape(user[2])}\
        \n<b>🎭 Прозвище</b>: {html.escape(user[8])}\
        \n<b>📝 Био</b>: {bio}\
        \n<b>🚻 Пол</b>: {str(user[4]).replace('1', 'Мужской').replace('2', 'Женский').replace('0', '—').replace('3', str(html.escape(user[7]))).replace('4', str(html.escape(user[7])))}\
        \n<b>♾ Вид</b>: {str(user[4]).replace('1', str(html.escape(user[7]))).replace('2', str(html.escape(user[7]))).replace('0', str(html.escape(user[7]))).replace('3', '<tg-spoiler>Иной</tg-spoiler>').replace('4', '<tg-spoiler>Чеширский</tg-spoiler>')}\
        \n<b>⏳ Возраст</b>: {age} {years_letter(age)}\
        \n<b>👑 Репутация</b>: {rep} ({user[5]})\
        \n<b>💰 Баланс</b>: {user[11]}\
        \n<b>️⚠️ Варны</b>: {userwarn[2]}"
        id = message.reply_to_message.message_id
        if choice([True, False]):
            response_text += f"\n\n<a href='{kuzya_news_link}'>🗞 Канал с новостями</a>"
        
        msg = await bot.send_message(message.chat.id, response_text, parse_mode='html', reply_to_message_id=id, disable_web_page_preview=True)
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        
        if message.reply_to_message.from_user.first_name == "":
            delete_user(message.reply_to_message.from_user.id)
            await bot.send_message(message.chat.id, f'<a href="tg://user?id={user[0]}">{html.escape(user[2])}</a> попадает в некролог!😭', parse_mode='html')

        try:
            usern2 = message.reply_to_message.forward_from
            if usern2.id == botik_id:
                await message.reply("Я Кузя 🙃")
                return
            
            if usern2.id in no_rp_list:
                return
            
            if check_user(usern2.id):
                create_user_main(usern2.id, usern2.username, usern2.first_name)
                if usern2.is_bot == True:
                    set_specie(usern2.id, "Бот")
                user2 = get_user(usern2.id)

            else:
                username = usern2.username
                if username == None:
                    username = usern2.id
                if usern2.is_bot == True:
                    set_specie(usern2.id, "Бот")
                set_username(usern2.id, username)
                user2 = get_user(usern2.id)
            
            if message.chat.type != 'private':
                warner2 = get_warner(message.chat.id, usern2.id)
                if warner2 == None:
                    warner2 = [message.chat.id, usern2.id, 0, 0, 0]
                if warner2[4] != 0:
                    return
            
            if message.chat.type == 'private':
                userwarn2 = ["—", "—", "—", "—"]
            else:
                userwarn2 = warner2
            

           
            if user2[6] > 100000:
                age2 = "Неизмеримо"
            else:
                age2 = str(user2[6])
            
            bio = user2[3]
            if bio.startswith("html: "):
                bio = bio.replace("html: ", "")
            else:
                bio = f"<em>{html.escape(bio)}</em>"
            
            name2 = usern2.first_name
            if usern2.last_name != None and usern2.last_name != "":
                name2 = usern2.first_name + " " + usern2.last_name
            
            rep = await string_rep(user2[5], user2[4])
            response_text = f"Цитируется пользователь <a href='tg://user?id={user2[0]}'>{html.escape(name2)}</a>\
            \n\n<b>🆔 ID</b>: <code>{user2[0]}</code>\
            \n<b>👤 Username</b>: @{user2[1]}\
            \n<b>🏷️ Ник</b>: {html.escape(user2[2])}\
            \n<b>🎭 Прозвище</b>: {html.escape(user2[8])}\
            \n<b>📝 Био</b>: {bio}\
            \n<b>🚻 Пол</b>: {str(user2[4]).replace('1', 'Мужской').replace('2', 'Женский').replace('0', '—').replace('3', str(html.escape(user2[7]))).replace('4', str(html.escape(user2[7])))}\
            \n<b>♾ Вид</b>: {str(user2[4]).replace('1', html.escape(user2[7])).replace('2', html.escape(user2[7])).replace('0', html.escape(user2[7])).replace('3', '<tg-spoiler>Иной</tg-spoiler>').replace('4', '<tg-spoiler>Чеширский</tg-spoiler>')}\
            \n<b>⏳ Возраст</b>: {age2} {years_letter(age2)}\
            \n<b>👑 Репутация</b>: {rep} ({user2[5]})\
            \n<b>💰 Баланс</b>: {user2[11]}\
            \n<b>️⚠️ Варны</b>: {userwarn2[2]}"
            id = message.reply_to_message.message_id
            if choice([True, False]):
                response_text += f"\n\n<a href='{kuzya_news_link}'>🗞 Канал с новостями</a>"
        
            msg = await bot.send_message(message.chat.id, response_text, parse_mode='html', reply_to_message_id=id, disable_web_page_preview=True)
            await as_del_msg(message.chat.id, msg.message_id, time_del)
        except:
            return


#Профиль свой
@dp.message_handler(lambda message: message.text.lower() in whoiam)
async def my_profile(message: types.Message):
    users = message.from_user
    
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, users.id)
        if warner == None:
            warner = [message.chat.id, users.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)

    if check_user(users.id):
        user = create_user(users.id, users.username, users.first_name)

    else:
        username = users.username
        if username == None:
            username = users.id
            set_username(users.id, username)
        
        set_username(users.id, username)
        
        user = get_user(users.id)
    
    if message.chat.type != 'private':
        if check_member(message.chat.id, users.id) == False:
            ment = await bot.get_chat_member(message.chat.id, users.id)
            if ment.status != "left" and ment.status != "kicked":
                create_member(message.chat.id, users.id, ment.status)
    

    
    if message.chat.type == 'private':
        userwarn = ["—", "—", "—", "—"]
    else:
        userwarn = warner
    
    if user[6] > 100000:
        age = "Неизмеримо"
    else:
        age = str(user[6])
    
    bio = user[3]
    if bio.startswith("html: "):
        bio = bio.replace("html: ", "")
    else:
        bio = f"<em>{html.escape(bio)}</em>"
        
    name = users.first_name
    if users.last_name != None and users.last_name != "":
        name = users.first_name + " " + users.last_name
    
    rep = await string_rep(user[5], user[4])
    response_text = f"Это пользователь <a href='tg://user?id={user[0]}'>{html.escape(name)}</a>\
    \n\n<b>🆔 ID</b>: <code>{user[0]}</code>\
    \n<b>👤 Username</b>: @{user[1]}\
    \n<b>🏷️ Ник</b>: {html.escape(user[2])}\
    \n<b>🎭 Прозвище</b>: {html.escape(user[8])}\
    \n<b>📝 Био</b>: {bio}\
    \n<b>🚻 Пол</b>: {str(user[4]).replace('1', 'Мужской').replace('2', 'Женский').replace('0', '—').replace('3', str(html.escape(user[7]))).replace('4', str(html.escape(user[7])))}\
    \n<b>♾ Вид</b>: {str(user[4]).replace('1', str(html.escape(user[7]))).replace('2', str(html.escape(user[7]))).replace('0', str(html.escape(user[7]))).replace('3', '<tg-spoiler>Иной</tg-spoiler>').replace('4', '<tg-spoiler>Чеширский</tg-spoiler>')}\
    \n<b>⏳ Возраст</b>: {age} {years_letter(age)}\
    \n<b>👑 Репутация</b>: {rep} ({user[5]})\
    \n<b>💰 Баланс</b>: {user[11]}\
    \n<b>️⚠️ Варны</b>: {userwarn[2]}"
    if choice([True, False]):
            response_text += f"\n\n<a href='{kuzya_news_link}'>🗞 Канал с новостями</a>"
        
    msg = await message.reply(response_text, parse_mode='html', disable_web_page_preview=True)
    await as_del_msg(message.chat.id, msg.message_id, time_del)

#Повышение репутации
@dp.message_handler(lambda message: message.text.lower() in good)
async def add_reputation(message: types.Message):
    if message.chat.type == 'private':
        return
    
    if message.chat.id not in legal_chats:
        await botik_leave_chat(message)
        return
    
    if message.reply_to_message and message.from_user.id != message.reply_to_message.from_user.id:
        goodu = message.reply_to_message.from_user
        gooder = message.from_user
        
        if check_user(gooder.id):
            gooderr = [0, 0, 0, 0, 0, 0, 0]
        else:
            gooderr = get_user(gooder.id)
        
        if check_user(goodu.id) == False:
            goodur = get_user(goodu.id)
        else:
            return
        

        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
        
        warnerer = get_warner(message.chat.id, message.reply_to_message.from_user.id)
        if warnerer == None:
            warnerer = [message.chat.id, message.reply_to_message.from_user.id, 0, 0, 0]
        if warnerer[4] != 0:
            return

        global reps_user_id
        if reps_user_id == gooder.id:
            return
        else:
            reps_user_id = gooder.id
        
        if goodu.id == botik_id:
            hide = choice(hide_ver)
            if hide == 0:
                await message.answer(f"Чудесно, но я ведь просто Кузя 🙃")
            await add_reputation_f(message, gooderr, goodur)
            return
        
        if goodu.id in no_rp_list:
            await add_reputation_f(message, gooderr, goodur)
            return
        
        goodex = 0
        try:
            if message.reply_to_message.text != None:
                for word in good:
                    if word in message.reply_to_message.text.lower():
                        goodex = 1
                        break
        
       
        finally:
            if goodex == 1:
                return
            
            similar_r = 0
            if message.reply_to_message.text != None:
                if utils.full_process(message.reply_to_message.text.lower()):
                    simi_r = process.extractOne(message.reply_to_message.text.lower(), good)
                    similar_r = simi_r[1]
                else:
                    similar_r = 0
            
            if similar_r > 90:
                return
                
            
            adminse = await message.chat.get_administrators()
            admino = 0
            for admin in adminse:
                if admin.user.id == gooder.id:
                    admino = 1
                    continue
            try:
                if admino == 0:
                    if abs(gooderr[5]) <= abs(goodur[5]):
                        result = randint(0,10)
                        if result >= rep_separat_g:  
                            
                            if gooderr[5] >= -10:
                                add_rep(goodu.id)
                            else:
                                take_rep(goodu.id)
                            
                            hide = choice(hide_ver)
                            if hide == 0:
                                await message.answer(f"✅ Повышение засчитано (<a href='tg://user?id={goodu.id}'>+1</a>)")

                            return
                        return
                    else:
                        result = randint(0,10)
                        if result >= rep_converg_g:    
                            
                            if gooderr[5] >= -10:
                                add_rep(goodu.id)
                            else:
                                take_rep(goodu.id)
                            
                            hide = choice(hide_ver)
                            if hide == 0:
                                await message.answer(f"✅ Повышение засчитано (<a href='tg://user?id={goodu.id}'>+1</a>)")
                            return
                        return
                if admino == 1:
                    add_rep(goodu.id)
                    await message.answer(f"✅ Повышение засчитано (<a href='tg://user?id={goodu.id}'>+1</a>)")
                    return
            except:
                return
            return


#Понижение репутации
@dp.message_handler(lambda message: message.text.lower() in bad)
async def take_reputation(message: types.Message):
    if message.chat.type == 'private':
        return
    
    if message.chat.id not in legal_chats:
        await botik_leave_chat(message)
        return
    
    if message.reply_to_message and message.from_user.id != message.reply_to_message.from_user.id:
        badu = message.reply_to_message.from_user
        bader = message.from_user
        
        if check_user(bader.id):
            baderr = [0, 0, 0, 0, 0, 0, 0]
        else:
            baderr = get_user(bader.id)
        
        if check_user(badu.id) == False:
            badur = get_user(badu.id)
        else:
            return
        
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
        
        warnerer = get_warner(message.chat.id, message.reply_to_message.from_user.id)
        if warnerer == None:
            warnerer = [message.chat.id, message.reply_to_message.from_user.id, 0, 0, 0]
        if warnerer[4] != 0:
            return
        
        global reps_user_id
        if reps_user_id == bader.id:
            return
        else:
            reps_user_id = bader.id
        
        if badu.id == botik_id:
            hide = choice(hide_ver)
            if hide == 0:
                await message.answer(f"Печально, но я ведь просто Кузя 🙃")
            await take_reputation_f(message, baderr, badur)
            return
        
        if badu.id in no_rp_list:
            await take_reputation_f(message, baderr, badur)
            return
        
        
        badex = 0
        try:
            if message.reply_to_message.text != None:
                for word in bad:
                    if word in message.reply_to_message.text.lower():
                        badex = 1
                        break
            
        finally:
            if badex == 1:
                return
            
            similar_r = 0
            if message.reply_to_message.text != None:
                if utils.full_process(message.reply_to_message.text.lower()):
                    simi_r = process.extractOne(message.reply_to_message.text.lower(), bad)
                    similar_r = simi_r[1]
                else:
                    similar_r = 0
            
            if similar_r > 90:
                return
            
            adminse = await message.chat.get_administrators()
            admino = 0
            for admin in adminse:
                if admin.user.id == bader.id:
                    admino = 1
                    continue
            try:
                if admino == 0:
                    if abs(baderr[5]) >= abs(badur[5]):
                        result = randint(0,10)
                        if result >= rep_separat_b:
                            
                            if baderr[5] >= -10:
                                take_rep(badu.id)
                            else:
                                add_rep(badu.id)
                            
                            hide = choice(hide_ver)
                            if hide == 0:
                                await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
                            return
                        return
                    else:
                        result = randint(0,10)
                        if result >= rep_converg_b:
                            
                            if baderr[5] >= -10:
                                take_rep(badu.id)
                            else:
                                add_rep(badu.id)
                            
                            hide = choice(hide_ver)
                            if hide == 0:
                                await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
                            return
                        return
                if admino == 1:
                    take_rep(badu.id)
                    await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={badu.id}'>-1</a>)")
                    return
            except:
                return


async def string_rep(rep, gender):
    if rep < 0:
        if rep <= -1000:
            return "ㅤ✳︎ㅤ"
        
        if rep <= -750 and rep > -1000:
            return "Король Адской Долины"
        
        if rep <= -500 and rep > -750:
            return "Великий Древний"
        
        if rep <= -250 and rep > -500:
            return "Архидьявол"
        
        if rep <= -100 and rep > -250:
            return f"{str(gender).replace('1', 'Люцифер').replace('2', 'Лилит').replace('0', 'Дьябло').replace('3', 'Дьябло').replace('4', 'Дьябло')}"
        
        if rep <= -50 and rep > -100:
            return "Само Зло"
        
        if rep <= -25 and rep > -50:
            return "Ужасная"
        
        if rep <= -10 and rep > -25:
            return "Зловещая"
        
        if rep < 0 and rep > -10: 
            return "Плохая"
    
    if rep == 0:
        return "Никакая"
    
    if rep > 0:
        if rep > 0 and rep < 10:
            return "Хорошая"
        
        if rep >= 10 and rep < 25:
            return "Приличная"
        
        if rep >= 25 and rep < 50:
            return "Надёжная"
        
        if rep >= 50 and rep < 100:
            return "Благословенная"
        
        if rep >= 100 and rep < 250:
            return f"{str(gender).replace('1', 'Бог').replace('2', 'Богиня').replace('0', 'Божество').replace('3', 'Божество').replace('4', 'Божество')}"
            
        if rep >= 250 and rep < 500:
            return "Демиург"
        
        if rep >= 500 and rep < 750:
            return "Архангел"
        
        if rep >= 750 and rep < 1000:
            return "Божественный"
        
        if rep >= 1000 and rep < 1500:
            return "Абсолютный"
        
        if rep >= 1500:
            return "ㅤ✳︎ㅤ"

            
async def add_reputation_f(message: types.Message, gooderr, goodur):
    if gooderr[5] < -10:
        good = bad2
    else:
        good = good2
    
    if len(gooderr) >= 9:
        if gooderr[9] == 3 or goodur[9] == 3:
            return
    
    if goodur[9] == 3:
        return
    
    elif len(gooderr) >= 9:
        if gooderr[9] == 3:
            return
    
    if message.reply_to_message.text:
        if message.reply_to_message.text.lower() in good:
            return

    if utils.full_process(message.text.lower()) == False:
        return

    similar_r = 0
    if message.reply_to_message.text != None:
        if utils.full_process(message.reply_to_message.text.lower()):
            simi_r = process.extractOne(message.reply_to_message.text.lower(), good)
            similar_r = simi_r[1]
        else:
            similar_r = 0
    
    if similar_r > 90:
        return
    
    similar = 0
    
    if message.text.lower() in good:
        similar = 100
        print(f"Гуд. {similar}: Сообщение: →{message.text.lower()}←")
        logging.info(f'Гуд. {similar}: Сообщение: [{message.text.lower()}]')
    
    wrods = None
    if similar != 100:
        text_l = message.text.lower().replace("!", "").replace("?", "").replace(".", "").replace("+", "").replace("-", "").replace(")", "").replace("(", "").replace("…", "").replace(",", "").replace(":", "").replace('"', '').replace("«", "").replace("»", "").replace("[", "").replace("]", "")
        
        for word in text_l.split():
            if word == "нет" or word == "не":
                return
        
        if fuzz.WRatio("да", message.text.lower()) > 90:
            return
        
        if "+++++" in message.text.lower():
            similar = fuzz.partial_ratio(message.text.lower(), "+++++++++++++++++++++++++++++++++++++")
            print(f"Гуд. {similar}: Сообщение: →{message.text.lower()}← слово: →+++++←")
            logging.info(f'Гуд. {similar}: Сообщение: [{message.text.lower()}] слово: [+++++]')
        
        else:
            for word in good:
                if f"не{word[0]}{word[1]}" in text_l:
                    continue
                
                if len(word) > 1:
                    if len(text_l) < (len(word) / 2) + 1:
                        continue
                
                if len(text_l) > (len(word) * 3):
                    continue
                
                similar = fuzz.WRatio(word, text_l)
    
            
                if similar >= 90:
                    print(f"Гуд. {similar}: Сообщение: →{message.text.lower()}← слово: →{word}←")
                    logging.info(f'Гуд. {similar}: Сообщение: [{message.text.lower()}] слово: [{word}]')
                    wrods = word
                    break

    if similar >= 90:

        if wrods == 'хорош' or wrods == 'харош':
            for word in message.text.lower().split():
                if word == wrods:
                    continue
                elif fuzz.WRatio(f"{wrods}о", word) > similar:
                    print("Отклонено")
                    logging.info("Отклонено")
                    return

        global reps_user_id
        if reps_user_id == gooderr[0]:
            return
        else:
            reps_user_id = gooderr[0]
        
        if message.chat.id not in legal_chats:
            await botik_leave_chat(message)
            return
        
        try:
            if abs(gooderr[5]) <= abs(goodur[5]):
                result = randint(0,10) - (100 - similar)/10
                if result >= rep_separat_g:  
                    add_rep(goodur[0])
                    return True
                else:
                    return False
                
            else:
                result = randint(0,10) - (100 - similar)/10
                if result >= rep_converg_g:    
                    add_rep(goodur[0])
                    return True
                else:
                    return False
        except:
            return False
                
                
async def take_reputation_f(message: types.Message, baderr, badur):
    
    if baderr[5] < -10:
        bad = good2
    else:
        bad = bad2
    
    if badur[9] == 3:
        return
    
    elif len(baderr) >= 9:
        if baderr[9] == 3:
            return
    
    if message.reply_to_message.text:
        if message.reply_to_message.text.lower() in bad:
            return
    
    similar_r = 0
    
    if message.reply_to_message.text != None:
        if utils.full_process(message.reply_to_message.text.lower()):
            simi_r = process.extractOne(message.reply_to_message.text.lower(), bad)
            similar_r = simi_r[1]
        else:
            similar_r = 0
    
    if similar_r > 90:
        return
    
    similar = 0
    
    if message.text.lower() in bad:
        similar = 100
        print(f"Бэд. {similar}: Сообщение: →{message.text.lower()}←")
        logging.info(f'Бэд. {similar}: Сообщение: [{message.text.lower()}]')
    
    
    if similar != 100:
        text_l = message.text.lower().replace("!", "").replace("?", "").replace(".", "").replace("+", "").replace("-", "").replace(")", "").replace("(", "").replace("…", "").replace(",", "").replace(":", "").replace('"', '').replace("«", "").replace("»", "").replace("[", "").replace("]", "")
        
        for word in text_l.split():
            if word == "нет" or word == "не":
                return
        
        if fuzz.WRatio("да", message.text.lower()) > 90:
            return
    
        if "-----" in message.text.lower():
            similar = fuzz.partial_ratio(message.text.lower(), "--------------------------------------")
            print(f"Бэд. {similar}: Сообщение: →{message.text.lower()}← слово: →-----←")
            logging.info(f'Бэд. {similar}: Сообщение: [{message.text.lower()}] слово: [-----]')
        
        else:
            for word in bad:
                if f"не{word[0]}{word[1]}" in text_l:
                    continue
                
                if len(word) > 1:
                    if len(text_l) < (len(word) / 2) + 1:
                        continue
                if len(text_l) > (len(word) * 3):
                    continue
                
                similar = fuzz.WRatio(word, text_l)
                
                if similar < 90:
                    similar = fuzz.token_set_ratio(word, text_l)
                
                if similar >= 90:
                    print(f"Бэд. {similar}: Сообщение: →{message.text.lower()}← слово: →{word}←")
                    logging.info(f'Бэд. {similar}: Сообщение: [{message.text.lower()}] слово: [{word}]')
                    break


    
    if similar >= 90:
        
        global reps_user_id
        if reps_user_id == baderr[0]:
            return
        else:
            reps_user_id = baderr[0]
        
        if message.chat.id not in legal_chats:
            await botik_leave_chat(message)
            return
        
        try:
            if abs(baderr[5]) >= abs(badur[5]):
                result = randint(0,10) - (100 - similar)/10
                if result >= rep_separat_b:
                    take_rep(badur[0])
                    return True
                else:
                    return False
                
            else:
                result = randint(0,10) - (100 - similar)/10
                if result >= rep_converg_b:
                    take_rep(badur[0])
                    return True
                else:
                    return False
        except:
            return False
            
            
                
