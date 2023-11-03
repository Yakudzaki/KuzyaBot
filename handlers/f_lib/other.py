from loader import dp, bot
from keyboards.inline.channel_kb import channel_btn
from aiogram import types
import asyncio
import logging
from random import randint, choice

from utils.db import *

import time
import re
import html
import pymorphy3
#pip install pymorphy3   (И проверить, что словари (dict) - установились тоже)

from settings import *

from .mats import *

from .pyrogram_f import pyro_get_chat_member, get_chat_members, get_delete_members

from aiogram.utils import executor
from fuzzywuzzy import fuzz
wait = 0

async def rp_check(message: types.Message):
    
    user = create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    user2 = None
    
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.reply_to_message:

        user2 = create_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name)
        
        if user2[1] != message.reply_to_message.from_user.username:
            if message.reply_to_message.from_user.username != None:
                set_username(user2[0], message.reply_to_message.from_user.username)
                user2 = get_user(message.reply_to_message.from_user.id)
            else:
                set_username(user2[0], user2[0])
                user2 = get_user(message.reply_to_message.from_user.id)
        
        if user2[0] in no_rp_list:
            return
        
        if check_monik(user2[0], user2[8]) == True:
            rep_monic = get_monik(user2[0], user2[8])[2]
            if user2[5] < rep_monic:
                if user2[8] != "":
                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
            elif user[5] > user2[5]:
                if user2[8] != "":
                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        
        return user2
    
    else:
        match = re.search(r'@(\w+)', message.text)
        if match:
            name = match.group(1)
            if check_username(name):
                
                if message.chat.type == 'private':
                    msg = await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return

                try:
                    member = await pyro_get_chat_member(message.chat.id, name)
                    
                    if check_user(member.user.id):
                        create_user_main(member.user.id, name, member.user.first_name)
                    else:
                        set_username(member.user.id, name)
                    
                    user2 = get_user(member.user.id)
                
                except:
                    msg = await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return
            else:
                user2 = get_username(name)
            
            if user2[0] in no_rp_list:
                return
            
            if check_monik(user2[0], user2[8]) == True:
                rep_monic = get_monik(user2[0], user2[8])[2]
                if user2[5] < rep_monic:
                    if user2[8] != "":
                        user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                elif user[5] > user2[5]:
                    if user2[8] != "":
                        user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except:
                pass
            

            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            return user2
        
        else:
            
            for entity in message.entities:
                
                if entity.type == "text_mention":
                    user2_id = entity.user.id

                    user2 = create_user(user2_id, str(user2_id), entity.user.first_name)
                    
                    if user2[0] in no_rp_list:
                        continue
                    
                    if check_monik(user2[0], user2[8]) == True:
                        rep_monic = get_monik(user2[0], user2[8])[2]
                        if user2[5] < rep_monic:
                            if user2[8] != "":
                                user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                        elif user[5] > user2[5]:
                            if user2[8] != "":
                                user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                    try:
                        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    except:
                        pass
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    return user2

                else:
                    continue
            
            if message.chat.type != 'private' and "рандом" in message.text.lower():
                members = get_members(message.chat.id)
                for element in members:
                    member = choice(members)
                    user2 = get_user(member[1])
                    if user2[0] in no_rp_list:
                        continue
                    else:
                        if check_monik(user2[0], user2[8]) == True:
                            rep_monic = get_monik(user2[0], user2[8])[2]
                            if user2[5] < rep_monic:
                                if user2[8] != "":
                                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                            elif user[5] > user2[5]:
                                if user2[8] != "":
                                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                        try:
                            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                        except:
                            pass
                        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                        return user2

            return

async def message_user_get(message: types.Message):
    create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    user2 = None
    
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.reply_to_message:

        user2 = create_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name)
        
        if user2[1] != message.reply_to_message.from_user.username:
            if message.reply_to_message.from_user.username != None:
                set_username(user2[0], message.reply_to_message.from_user.username)
                user2 = get_user(message.reply_to_message.from_user.id)
            else:
                set_username(user2[0], user2[0])
                user2 = get_user(message.reply_to_message.from_user.id)
        
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        return user2
    
    else:
        match = re.search(r'@(\w+)', message.text)
        if match:
            name = match.group(1)
            if check_username(name):
                
                if message.chat.type == 'private':
                    msg = await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return

                try:
                    member = await pyro_get_chat_member(message.chat.id, name)
                    
                    if check_user(member.user.id):
                        create_user_main(member.user.id, name, member.user.first_name)
                    else:
                        set_username(member.user.id, name)
                    
                    user2 = get_user(member.user.id)
                
                except:
                    msg = await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return
            else:
                user2 = get_username(name)
            
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            return user2
        
        else:
            for entity in message.entities:
                if entity.type == "text_mention":
                    user2_id = entity.user.id
                    user2 = create_user(user2_id, str(user2_id), entity.user.first_name)
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    return user2
                else:
                    continue
            return

async def message_user_get_ban(message: types.Message):
    create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    user2 = None
    
    if message.reply_to_message:
        if check_user(message.reply_to_message.from_user.id):
            user2 = [message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name]
        else:
            user2 = get_user(message.reply_to_message.from_user.id)
        
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        return user2
    
    else:
        match = re.search(r'@(\w+)', message.text)
        if match:
            name = match.group(1)
            if check_username(name):
                
                if message.chat.type == 'private':
                    msg = await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return

                try:
                    member = await pyro_get_chat_member(message.chat.id, name)
                    
                    if check_user(member.user.id):
                        user2 = [member.user.id, name, member.user.first_name]
                    else:
                        set_username(member.user.id, name)
                    
                        user2 = get_user(member.user.id)
                
                except:
                    msg = await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return
            else:
                user2 = get_username(name)
            
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            return user2
        
        else:
            for entity in message.entities:
                if entity.type == "text_mention":
                    user2_id = entity.user.id
                    
                    if check_user(user2_id):
                        user2 = [user2_id, str(user2_id), entity.user.first_name]
                    else:
                        user2 = get_user(user2_id)
                    
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    return user2
                else:
                    continue
            return


async def check_all_members(message: types.Message):
    
    users = get_all_users()
    for chato in legal_chats:
        
        try:
            chat_memberses = await get_chat_members(chato)
        except:
            continue
        
        chat_members = chat_memberses[0]
        for user in users:
            print(f'{chato}→{user}')
            if user[0] not in chat_members:
                print(f'Пирограм сказал что чела в чате нет.')
                if check_member(chato, user[0]):
                    delete_member(chato, user[0])
            
            else:
                print(f'Пирограм сказал что чел в чате есть.')
                await asyncio.sleep(1)
                try:
                    ment = await bot.get_chat_member(chato, user[0])
                except:
                    ment = None
                    print(f'Нетуть данных.')
                    if check_member(chato, user[0]):
                        delete_member(chato, user[0])
                        print(f'Удален из мемберов.')
    
                if ment != None:
                    if ment.status == "kicked" or ment.status == "left":
                        if check_member(chato, user[0]):
                            delete_member(chato, user[0])
                            print('Был в чате, теперь нету')
                            continue

                    elif check_member(chato, user[0]) == False:
                        create_member(chato, user[0], ment.status)
                        print('Добавлен в мемберы')
                        continue
                else:
                    print(f'Нетуть данных.')
                    if check_member(chato, user[0]):
                        delete_member(chato, user[0])
                        print(f'Удален из мемберов.')

async def kuzya_wait(timese):

    await asyncio.sleep(timese)
   
async def clean_db_users(message: types.Message):
    users = get_all_users()
    deleters = await get_delete_members(legal_chats)
    print(f"deleters={deleters}")
    
    for user in users:
        print(f'{user}')
        try:
            chater = 0
            for chato in legal_chats:
                if check_member(chato, user[0]): 
                    chater = chater + 1
            
            if user[0] in deleters:
                chater = None
            
            if chater == 0:
                print(f"Нету в чатах: {user}")
                if user[3] == 'Нет' and user[4] == 0 and abs(user[5]) <= 2 and user[6] == 20 and user[7] == 'Человек' and user[8] == '':
                    print("Будет удалён. Ибо в базе на него нет ничего особого")
                    delete_user(user[0])
                else:
                    check = 0
                    for chato in legal_chats:
                        try:
                            await asyncio.sleep(2)
                            ment = await bot.get_chat_member(chato, user[0]) 
                            if ment != None:
                                check = check + 1
                                if ment.status != "left" and ment.status != "kicked":
                                    create_member(chato, user[0], ment.status)
                                    print(f"Стал {ment.status} в {chato}")
                        
                        except:     
                            continue
                    if check == 0:
                        print("Какая-то хрень. Чел особо секретный.")
                        delete_user(user[0])
                        print("Будет удалено из базы.")
                    else:

                        print(f"Останется.")
            
            elif chater == None:
                print('Удаленный Аккаунт')
                delete_user(user[0])
                print('Был в базе, теперь нету')
                continue
            
            else:
                print(f"Есть в чатах: {user}")
        except:
            continue
            
async def some_leave(chat_id):
    await asyncio.sleep(1)
    try:
        chat_members_all = await get_chat_members(chat_id)
        chat_members_in = chat_members_all[0]
        chat_members_del = chat_members_all[1]
    except:
        print('Отложено на 20 минут.')
        await asyncio.sleep(1250)
        try:
            chat_members_all = await get_chat_members(chat_id)
            chat_members_in = chat_members_all[0]
            chat_members_del = chat_members_all[1]
        except:
            return
    
    members = get_members(chat_id)
    for member in members:
        if member[1] in chat_members_in:
            continue
        elif member[1] in chat_members_del:
            set_status(chat_id, member[1], 'deleted')
            print(f'{chat_id} — {member[1]} → deleted')
            continue
        
        else:
            try:
                await asyncio.sleep(1)
                ment = await bot.get_chat_member(chat_id, member[1])
            except:
                ment = None
                set_status(chat_id, member[1], "left")

            if ment != None:
                if ment.status == "left" or ment.status == "kicked":
                    set_status(chat_id, member[1], ment.status)
                    print(f"{chat_id} — {ment.status} → {ment}")
                    logging.info(f'{chat_id} — {ment.status} — {ment}')

    
    
    lefters = get_from_status(chat_id, "left")
    for lefter in lefters:

        user = get_user(lefter[0])
        delete_member(chat_id, lefter[0])
        await bot.send_message(chat_id, f'Пока, <a href="tg://user?id={user[0]}">{html.escape(user[2])}</a>!😔', parse_mode='html')
        
    lefters = get_from_status(chat_id, "kicked")
    for lefter in lefters:

        user = get_user(lefter[0])
        delete_member(chat_id, lefter[0])
        await bot.send_message(chat_id, f'Прощай, <a href="tg://user?id={user[0]}">{html.escape(user[2])}</a>!😡', parse_mode='html')
        
    lefters = get_from_status(chat_id, "deleted")
    for lefter in lefters:

        user = get_user(lefter[0])
        delete_user(lefter[0])
        await bot.send_message(chat_id, f'<a href="tg://user?id={user[0]}">{html.escape(user[2])}</a> попадает в некролог!😭', parse_mode='html')
        try:
            await bot.kick_chat_member(chat_id, user[0])
        except:
            pass

async def restrict_chat(message: types.Message):
    global wait
    wait = wait + 1
    await asyncio.sleep(wait)

    if check_chat(message.chat.id):
        create_chat(message.chat.id)

    
    if check_chat_m(message.chat.id):
        create_chat_m(message.chat.id)
    
    set_time_up(message.chat.id, 30) #сколько минут выключены стики после поста с канала
    chatm = get_chat_m(message.chat.id)
    time_up = chatm[4]
    
    if chatm[3] == 0:

        set_chat_restricted(message.chat.id, 1)
        chate = get_chat(message.chat.id)
        chats = await bot.get_chat(message.chat.id)
        perm = chats.permissions
        
        await bot.set_chat_permissions(message.chat.id, types.chat_permissions.ChatPermissions(perm.can_send_messages, perm.can_send_media_messages, perm.can_send_audios, perm.can_send_documents, perm.can_send_photos, perm.can_send_videos, perm.can_send_video_notes, perm.can_send_voice_notes, perm.can_send_polls, False, perm.can_add_web_page_previews, perm.can_change_info, perm.can_invite_users, perm.can_pin_messages, perm.can_manage_topics), use_independent_chat_permissions=True)
        #Без названия - can_send_other_messages
        set_funny_func(message.chat.id, 0)

        while time_up > 0:
            await asyncio.sleep(60)
            chatm2 = get_chat_m(message.chat.id)
            time_up = chatm2[4] - 1
            set_time_up(message.chat.id, time_up)
            wait = 0

        
        await bot.set_chat_permissions(message.chat.id, permissions=perm, use_independent_chat_permissions=True)
        set_funny_func(message.chat.id, chate[4])
        
        set_chat_restricted(message.chat.id, 0)
        
    else:
        return
   

async def botik_leave_chat(message: types.Message):
    await message.answer(f"❌ Я создан исключительно для чата <a href='{topa_chat_invite}'>Опа Это Топа</a>!", parse_mode="html", disable_web_page_preview=True)
    
    await asyncio.sleep(2)
    
    await message.answer(f"Айди вашего чата: [{str(message.chat.id)}]\nДоговаривайтесь с <a href='{yakudza_url}'>создателем</a> бота.", parse_mode="html", disable_web_page_preview=True)
    
    await asyncio.sleep(2)
    
    if check_chat(message.chat.id):
        create_chat_with_info(message.chat.id, f"НЕЛЕГАЛ: {message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
    else:
        set_chat_info(message.chat.id, f"НЕЛЕГАЛ: {message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
    
    
    await asyncio.sleep(2)
    
    await bot.leave_chat(message.chat.id)
    return
    
    
def similaring(text, massive, num, lim):
    similar = 0
    
    text = text.replace("!", "").replace("?", "").replace(".", "").replace("+", "").replace("-", "").replace(")", "").replace("(", "").replace("…", "").replace(",", "").replace(":", "").replace('"', '').replace("«", "").replace("»", "").replace("[", "").replace("]", "").replace("—", "")
    
    for word in massive:
        
        if len(text) < (len(word) / 2) + 1:
            continue
        
        if len(text) > round(len(word) * lim):
            continue
        
        similar = fuzz.WRatio(word, text)
        if similar >= num:
            return True

    return False
    
    
def matex(text):
    if text == None:
        return False
    if text == "":
        return False
    try:
        for word in curse_words_w:
            if word in text:
                return True
    except:
        pass
    
    
    try:
        for word in text.split():
            
            for word2 in curse_words_s:
                if word.startswith(word2):
                    return True
            
            
            for word2 in curse_words_f:
                if word == word2:
                    return True
                elif fuzz.WRatio(word, word2) > 95:
                    return True
    
    except:
        pass
    
    return False
    
    


async def call_everybody(message: types.Message):
    logging.info(f'В чате {message.chat.id} созывают всех!')
    print(f'В чате {message.chat.id} созывают всех!')
    timese = 15
    replic_gone = False
    replic = ""
    try:
        if message.text.split()[2] != None:
            try:
                if int(message.text.split()[2]) < 5000 and int(message.text.split()[2]) >= 0:
                    timese = int(message.text.split()[2])
                else:
                    timese = 15
            except:
                try:
                    try:
                        replic = f"|"
                        for word in message.text.split()[2:]:
                            replic = replic + f" {word}"
                        replic_gone = True
                    except:
                        replic = ""
                except:
                    timese = 15
                    replic = ""
    except:
        timese = 15
    if replic_gone == False:
        try:
            if message.text.split()[2] != None:
                if message.text.split()[3] != None:
                    try:
                        replic = f"|"
                        for word in message.text.split()[3:]:
                            replic = replic + f" {word}"
                    except:
                        replic = ""
        except:
            replic = ""
    
    logging.info(f'Реплика - {replic}, время - {timese}!')
    
    members = get_members(message.chat.id)
    msg = '🔔'
    i = 0
    for member in members:
        if check_user(member[1]):
            delete_member(message.chat.id, member[1])
            continue
        if member[2] != "creator":
            user = get_user(member[1])
            i = i + 1
            msg += f'<a href="tg://user?id={member[1]}">‎</a>' # ‌ ‍   ​ ‏
            if i == 5:
                i = 0
                msg = msg + replic
                await asyncio.sleep(1)
                await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                msg_main = await bot.send_message(message.chat.id, msg, parse_mode='html')
                asyncio.create_task(del_msg(message.chat.id, msg_main.message_id, timese))
                msg = '🔔'
    
    if msg != '🔔':
        await asyncio.sleep(1)
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        msg = msg + replic
        msg_main = await bot.send_message(message.chat.id, msg, parse_mode='html')
        asyncio.create_task(del_msg(message.chat.id, msg_main.message_id, timese))

async def del_msg(chat_id, msg_id, timese):

    if timese > 0 and timese < 18000:
        await asyncio.sleep(timese)
        try:
            await bot.delete_message(chat_id, msg_id)
            return
        except:
            return
    else:
        return

async def as_del_msg(chat_id, msg_id, timese):
    if timese > 0 and timese < 18000:
        asyncio.create_task(del_msg(chat_id, msg_id, timese))
        return
    else:
        return
    
    
def update_morph(user_id):
    user = get_user(user_id)
    
    if user == None:
        return

    monikse = get_monik(user[0], user[8])
    if monikse != None:
        monic = morph_word_simple(user[8], user[4])
        set_monik_nomn(user[0], user[8], monic[0])
        set_monik_gent(user[0], user[8], monic[1])
        set_monik_datv(user[0], user[8], monic[2])
        set_monik_accs(user[0], user[8], monic[3])
        set_monik_ablt(user[0], user[8], monic[4])
        set_monik_loct(user[0], user[8], monic[5])


    morph = morph_word_simple(user[2], user[4])
    nick = create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])

def morph_word(user_id, name, gender):
    user = get_user(user_id)
    
    if user == None:
        nick = morph_word_simple(name, gender)
        return nick
    
    if name == user[8]:
        monikse = get_monik(user[0], name)
        
        if monikse == None:
            monik = morph_word_simple(name, gender)
            return monik
        
        else:
            if monikse[3] != '' and monikse[4] != '' and monikse[5] != '' and monikse[6] != '' and monikse[7] != '' and monikse[8] != '':
                monik = [monikse[3], monikse[4], monikse[5], monikse[6], monikse[7], monikse[8]]
                return monik
            else:
                monic = morph_word_simple(name, gender)
                set_monik_nomn(user[0], user[8], monic[0])
                set_monik_gent(user[0], user[8], monic[1])
                set_monik_datv(user[0], user[8], monic[2])
                set_monik_accs(user[0], user[8], monic[3])
                set_monik_ablt(user[0], user[8], monic[4])
                set_monik_loct(user[0], user[8], monic[5])
                return monic
    
    if name == user[2]:
        create = None
        nick = get_users_nick(user_id)
        
        if nick == None:
            create = True
        
        elif nick[1] == user[2]:
            return [nick[2], nick[3], nick[4], nick[5], nick[6], nick[7]]
        else:
            create = True
        
        if create:
            morph = morph_word_simple(user[2], user[4])
            nick = create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])
            return [nick[2], nick[3], nick[4], nick[5], nick[6], nick[7]]
    
        else:
            nick = morph_word_simple(name, gender)
            return nick
    else:
        nick = morph_word_simple(name, gender)
        return nick



def morph_word_simple(name, gender):
    nomn = ""
    gent = ""
    datv = ""
    accs = ""
    ablt = ""
    loct = ""

    nomning = 0
    
    i = 0
    for word in name.split():
        word = morph_word_main(word, gender)
        # print(f"{word}")
        if i == 0:
            nomn = nomn + word[0]
            gent = gent + word[1]
            datv = datv + word[2]
            accs = accs + word[3]
            ablt = ablt + word[4]
            loct = loct + word[5]
            if len(name.split()) > 3:
                if word[6] == "False":
                    nomning = nomning + 1
                elif word[1] == word[2] and word[2] == word[3] and word[3] == word[4] and word[4] == word[5]:
                    nomning = nomning + 1
            
            i = i + 1
        else:
            nomn = nomn + " " + word[0]
            gent = gent + " " + word[1]
            datv = datv + " " + word[2]
            accs = accs + " " + word[3]
            ablt = ablt + " " + word[4]
            loct = loct + " " + word[5]
            
            if len(name.split()) > 3:
                if word[6] == "False":
                    nomning = nomning + 1
                elif word[1] == word[2] and word[2] == word[3] and word[3] == word[4] and word[4] == word[5]:
                    nomning = nomning + 1
    
    
    if len(name.split()) > 1:
        
        if len(name.split()) > 3:
            if nomning*2 > len(name.split()):
                gent = nomn
                datv = nomn
                accs = nomn
                ablt = nomn
                loct = nomn

        elif accs.lower() != nomn.lower() or accs.lower() != gent.lower():
            a_nomnis = 0
            a_gentis = 0
            a_accsing = 0
            a_len = 0
            
            n_nomnis = 0
            n_gentis = 0
            n_accsing = 0
            n_len = 0
            
            i = 0
            while True:
                try:
                    word_a = accs.split()[i]
                    word_n = nomn.split()[i]
                    i = i + 1
    
                    word2 = morph_word_main(word_n, gender)
                    
                    if word2[6] == "ADJF":
                        a_len = a_len + len(word2[0])
                    
                    elif word2[6] == "True":
                        n_len = n_len + len(word2[0])
                        if word2[1] == word2[3]:
                            n_gentis = n_gentis + len(word2[0])
    
                        if word2[0] == word2[3]:
                            n_nomnis = n_nomnis + len(word2[0])
                        
                        if word2[0] != word2[3] and word2[1] != word2[3]:
                            n_accsing = n_accsing + len(word2[0])
                            continue 
                    
                    else:
                        continue

                except:
                    break
        
            n_distance = abs(n_gentis - n_nomnis)
            a_distance = abs(a_gentis - a_nomnis)
            
            if a_len > 1:
                if n_accsing < n_distance:
                    if n_nomnis >= n_gentis:
                        number = 0
                    else:
                        number = 1

                    i = 0
                    accs = ""
                    for word in name.split():
                        word = morph_word_main(word, gender)

                        if i == 0:
                            if word[6] == "ADJF":
                                accs = accs + word[number]
                            else:
                                accs = accs + word[3]
                            i = i + 1
                        else:
                            if word[6] == "ADJF":
                                accs = accs + " " + word[number]
                            else:
                                accs = accs + " " + word[3]
    
    
    names = [nomn, gent, datv, accs, ablt, loct]
    return names

def morph_word_main(name, gender):
    doing = 0
    
    infos = "False"
    
    if name == "" or name == None or name == " ":
        user_names = [name, name, name, name, name, name, infos]
        return user_names
    
    if name.lower() == name:
        doing = 0
    elif name.capitalize() == name:
        doing = 1
    elif name.upper() == name:
        doing = 2
    
    elif name[0] == name.capitalize()[0]:
        doing = 1
    else:
        doing = 0

    try:
        word = name.strip()
        morph = pymorphy3.MorphAnalyzer()
        
        word_all = morph.parse(word)
        word = None
    except:
        user_names = [name, name, name, name, name, name, infos]
        return user_names
    
    for nick in word_all:
        # print(f"{nick}")
        if 'nomn' in nick.tag: 
            word = nick
            break
        else:
            continue
    
    if word == None:
        user_names = [name, name, name, name, name, name, infos]
        return user_names
    
    infos = "True"
    
    
    
    for nick in word_all:
        
        if 'nomn' not in nick.tag:
            continue
        
        elif nick.normal_form == nick.word:
            word = nick
            # print(f"2")
            break
        
        elif "neut" in nick.tag:
            word = nick
            # print(f"4")
            break
        
        else:
            continue
    
    for nick in word_all:
        if 'nomn' not in nick.tag:
            continue
       
        elif gender == 1:
            if "femn" in nick.tag:
                continue
            if nick.normal_form == nick.word and "masc" in nick.tag:
                word = nick
                # print(f"8")
                break
        elif gender == 2:
            if "masc" in nick.tag:
                continue
            if nick.normal_form == nick.word and "femn" in nick.tag:
                word = nick
                # print(f"9")
                break
        elif gender == 3:
            if nick.normal_form == nick.word and "neut" in nick.tag:
                word = nick
                # print(f"10")
                break

    
    # print(f"{word}")

    if 'nomn' not in word.tag:
        user_names = [name, name, name, name, name, name, "False"]
        return user_names

    cases = (('nomn', 'именительный'),
            ('gent', 'родительный'),
            ('datv', 'дательный'),
            ('accs', 'винительный'),
            ('ablt', 'творительный'),
            ('loct', 'предложный'))
    
    user_names = []

    # print(f"фин")
    try:
        if gender == 2:
            if "masc" in word.tag and "plur" not in nick.tag:
                user_names = [name, name, name, name, name, name, infos]
                # print(f"сброс жен")
                return user_names
        if gender == 1:
            if "femn" in word.tag and "plur" not in nick.tag:
                user_names = [name, name, name, name, name, name, infos]
                # print(f"сброс муж")
                return user_names
        

        
        if 'sing' in word.tag:
            for j in cases:
                info = word.inflect({'sing', j[0]})
                if info != None:
                    names_lower = info.word
                    
                    if doing == 1:
                        names = names_lower.capitalize()
                        # print(f"names={names}")
                    elif doing == 2:
                        names = names_lower.upper()
                    else:
                        names = names_lower
                    
                    user_names = user_names + [names]
                else:
                    names = name
                    # print(f"сброс един падеж {j}")
                    user_names = user_names + [names]
        
        if 'plur' in word.tag:
            if 'Name' in word.tag or 'Surn' in word.tag or 'Patr' in word.tag or 'Orgn' in word.tag or 'Abbr' in word.tag:
                user_names = [name, name, name, name, name, name, "False"]
                return user_names
            
            for j in cases:
                info = word.inflect({'plur', j[0]})
                
                if info != None:
                    names_lower = info.word
                    
                    if doing == 1:
                        names = names_lower.capitalize()
                        # print(f"names={names}")
                    elif doing == 2:
                        names = names_lower.upper()
                    else:
                        names = names_lower.lower()
                    
                    user_names = user_names + [names]
                
                else:
                    names = name
                    # print(f"сброс множ падеж {j}")
                    user_names = user_names + [names]
        
        
        if 'ADJF' in word.tag:
            infos = 'ADJF'
        users_names = [user_names[0], user_names[1], user_names[2], user_names[3], user_names[4], user_names[5], infos]
        return users_names
    
    except:
        # print(f"ошибка")
        user_names = [name, name, name, name, name, name, infos]
        return user_names



def eight_years(chat_id, user1, user2, message, agree): #user1 - кто, user2 - кого. if agree == True, то посадить могут любого из юзеров, если False - то только user1 - рискует.
    
    if user1[0] == user2[0]:
        return
    
    if agree == False:
        if user1[6] <= user2[6]:
            return
        else:
            eight_years_main(chat_id, user1, user2, message)
    
    else:
        if user1[6] <= user2[6]:
            eight_years_main(chat_id, user2, user1, message)
        else:
            eight_years_main(chat_id, user1, user2, message)

    return

def eight_years_main(chat_id, user1, user2, message): #user1 - кто возможно виноват, user2 - кого.
    
    polic = False

    if user1[6] >= 18 and user2[6] < 16:
        polic = True
    
    elif user1[6] >= 14 and user2[6] < 12:
        polic = True

    if polic == False:
        return
    
    
    result = randint(0, 100)
    
    if result >= 50:
        
        if check_marry(user1[0], user2[0]) == True and user2[6] >= 12:
            return
        
        asyncio.create_task(eight_years_sending(chat_id, user1, message))
    else:
        return


async def eight_years_sending(chat_id, user, message): #сообщение — то которое кузя послал. (ну или любое иное. если кто внесет...)
    if user[6] >= 18:
        rpword = "посадили на восемь лет строгача!"
        rpemodz = ["👤→⛓", "👨‍🦰→⛓", "👩→⛓", "👾→⛓", "🐱→⛓"]
    else:
        rpword = "отправили на четыре года в колонию!"
        rpemodz = ["👤→⛓", "👨‍🦰→⛓", "👩→⛓", "👾→⛓", "🐱→⛓"]
    
    user = get_user(user[0])
    
    nick2 = morph_word(user[0], user[2], user[4])[3]    
    
    action = rpword
    rpemodz = rpemodz[user[4]]
    
    text = f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(nick2)}</a> {html.escape(action)}"
    
    await asyncio.sleep(30)
    await bot.send_chat_action(chat_id, types.ChatActions.TYPING)
    await bot.send_message(chat_id, text, reply_to_message_id=message.message_id, parse_mode="html")
    
    
def years_letter(num):
    num = str(num)
    if num.endswith("0"):
        if num == "0":
            return "зим"
        else:
            return "лет"
        
    elif num.endswith("1"):
        if num.endswith("11"):
            return "лет"
        elif num == "1":
            return "годик"
        else:
            return "год"
    
    elif num.endswith("2"):
        if num.endswith("12"):
            return "лет"
        else:
            return "года"
    
    elif num.endswith("3"):
        if num.endswith("13"):
            return "лет"
        else:
            return "года"
    
    elif num.endswith("4"):
        if num.endswith("14"):
            return "лет"
        else:
            return "года"

    elif num.endswith("5"):
        return "лет"
    elif num.endswith("6"):
        return "лет"
    elif num.endswith("7"):
        return "лет"
    elif num.endswith("8"):
        return "лет"
    elif num.endswith("9"):
        return "лет"
    elif num == "Неизмеримо":
        return ""
    else:
        return "годов"


async def is_sub(message): 
    temp = await bot.get_chat_member(kuzya_news_name, message.from_user.id) 
    if temp.status == 'left': 
        await message.reply('<b>Чтобы воспользоваться этой функцией вы должны быть подписаны на канал ниже!</b>', 
                               reply_markup = channel_btn) 
        return False
    else:
        return True