import requests
import base64
import html
import asyncio
import os
import logging
import aioschedule
import asyncio
import gtts
import secrets
import string

from loader import dp, bot
from aiogram import types
from app import server_dir
from handlers.f_lib.other import as_del_msg
from utils.db.db_utils_users import *
from utils.db.db_utils_сhats import *
from utils.db.db_utils_warning import *
from ..f_lib.other import is_sub
from settings import *
from data import config


TOKEN = config.TOKEN


@dp.message_handler(commands=["record", "рекорд"], commands_prefix="/!.")
async def handler_record(message: types.Message):
    
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
    
    allow = 0

    if message.from_user.id in botovod_id:
        allow = 1
    
    command = message.text.split()[0]
    args = message.text.replace(f"{command} ", "").replace(f"{command}", "")
    var = 0
    
    if args == "" or args == " " or args == None:
        if message.reply_to_message:
            if message.reply_to_message.text:
                args = message.reply_to_message.text
                var = 1
    
            if message.reply_to_message.caption:
                args = message.reply_to_message.caption
                var = 1
   
    
    if args == "" or args == " " or args == None:
        msg = await message.reply("<b>❌ Укажите текст или сделайте ответ на сообщение командой!</b>")
        await as_del_msg(message.chat.id, msg.message_id, 30)
        await as_del_msg(message.chat.id, message.message_id, 30)
        return
        

    
    if allow == 0 and args != None:
        if var == 0 and message.reply_to_message:
            if args.endswith("?"):
                if message.from_user.last_name != None:
                    args = f"{message.from_user.first_name} {message.from_user.last_name} спра́шивает: — " + args
                else:
                    args = f"{message.from_user.first_name} спра́шивает: — " + args
            else:
                if message.from_user.last_name != None:
                    args = f"{message.from_user.first_name} {message.from_user.last_name} отвеча́ет: — " + args
                else:
                    args = f"{message.from_user.first_name} отвеча́ет: — " + args
        
        
        else:
            if args.endswith("?"):
                if message.from_user.last_name != None:
                    args = f"{message.from_user.first_name} {message.from_user.last_name} спра́шивает: — " + args
                else:
                    args = f"{message.from_user.first_name} спра́шивает: — " + args
            else:
                if message.from_user.last_name != None:
                    args = f"{message.from_user.first_name} {message.from_user.last_name} глаго́лет: — " + args
                else:
                    args = f"{message.from_user.first_name} глаго́лет: — " + args
    
    
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_chat_action(message.chat.id, types.ChatActions.RECORD_VOICE)
    asyncio.create_task(saying(message, args, var))
    return


async def saying(message, args, var):
    try:
        text = gtts.gTTS(args, lang="ru")
        alphabet = string.ascii_letters + string.digits
        name = ''.join(secrets.choice(alphabet) for i in range(16))
        text.save(server_dir + f"/voice/{name}.mp3") 
    except:
        await message.answer("<b>❌ Что-то пошло не так!</b>")
        return
    await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_VOICE)
    
    if message.reply_to_message:
        if var == 0:
            id = message.reply_to_message.message_id
            await bot.send_voice(message.chat.id, open(server_dir + f"/voice/{name}.mp3", "rb"), reply_to_message_id=id)
        else:
            await bot.send_voice(message.chat.id, open(server_dir + f"/voice/{name}.mp3", "rb"))
    else:
        await bot.send_voice(message.chat.id, open(server_dir + f"/voice/{name}.mp3", "rb"))
    
    os.remove(server_dir + f"/voice/{name}.mp3")
    return
    
    
@dp.message_handler(commands=["say", "скажи"], commands_prefix="!/.")
async def say(message: types.Message):
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
    
    
    allow = 0
    if message.from_user.id in botovod_id:
        allow = 1
    user = create_user(users.id, users.username, users.first_name)
    try:
        if message.reply_to_message:
            sos = [""]
            command = message.text.split()[0]
            text = html.escape(message.text.replace(f"{command} ", "").replace(f"{command}", ""))
            if text in sos:
                if message.reply_to_message.text:
                    text2 = html.escape(message.reply_to_message.text)
                elif message.reply_to_message.caption:
                    text2 = html.escape(message.reply_to_message.caption)
                else:
                    msg = await message.reply("<b>❌ Укажите текст, либо сделайте ответ командой на то сообщение которое я должен сказать!</b>\nПример: !say привет; !скажи привет")
                    await as_del_msg(message.chat.id, msg.message_id, 30)
                    await as_del_msg(message.chat.id, message.message_id, 30)
                    
                    return
                if len(text2) > 500 and allow == 0:
                    await message.reply("<b>❌ Вы превысили ограничение на количество символов</b>!\n Максимальное количество символов - 500")
                    return
                if allow == 0:
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    await bot.delete_message(message.chat.id, message.message_id)
                    if text2.endswith("?"):
                        await bot.send_message(message.chat.id, f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> спрашивает: — «{text2}»", reply_to_message_id=id)
                        return
                    if text2.endswith("!"):
                        await bot.send_message(message.chat.id, f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> восклицает: — «{text2}»", reply_to_message_id=id)
                        return
                    if text2.endswith("."):
                        await bot.send_message(message.chat.id, f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> говорит: — «{text2}»", reply_to_message_id=id)
                        return
                    await message.answer(f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> говорит: — «{text2}».")
                    return
                if allow == 1:
                    await bot.delete_message(message.chat.id, message.message_id)
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    await message.answer(text2)
                    return
            else:
                if len(text) > 500 and allow == 0:
                    await message.reply("<b>❌ Вы превысили ограничение на количество символов</b>!\n Максимальное количество символов - 500")
                    return
                if allow == 0:
                    id = message.reply_to_message.message_id
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    await bot.delete_message(message.chat.id, message.message_id)
                    if text.endswith("?"):
                        await bot.send_message(message.chat.id, f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> спрашивает: — «{text}»", reply_to_message_id=id)
                        return
                    if text.endswith("!"):
                        await bot.send_message(message.chat.id, f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> восклицает: — «{text}»", reply_to_message_id=id)
                        return
                    if text.endswith("."):
                        await bot.send_message(message.chat.id, f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> отвечает: — «{text}»", reply_to_message_id=id)
                        return
                    await bot.send_message(message.chat.id, f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> отвечает: — «{text}».", reply_to_message_id=id)
                    return
                if allow == 1:
                    id = message.reply_to_message.message_id
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    await bot.delete_message(message.chat.id, message.message_id)
                    await bot.send_message(message.chat.id, message.text.replace(f"{command} ", "").replace(f"{command}", ""), reply_to_message_id=id)
                    return
        else:
            command = message.text.split()[0]
            text = html.escape(message.text.replace(f"{command} ", "").replace(f"{command}", ""))
            sos = [""]
            if text in sos:
                msg = await message.reply("<b>❌ Укажите текст, либо сделайте ответ командой на то сообщение которое я должен сказать!</b>\nПример: !say привет; !скажи привет")
                await as_del_msg(message.chat.id, msg.message_id, 30)
                await as_del_msg(message.chat.id, message.message_id, 30)
                
                return
            elif len(text) > 500 and allow == 0:
                await message.reply("<b>❌ Вы превысили ограничение на количество символов</b>!\n Максимальное количество символов - 500")
            if allow == 0:
                await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                await bot.delete_message(message.chat.id, message.message_id)
                await message.answer(f"<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> говорит: — «{text}».")
                return
            if allow == 1:
                await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                await bot.delete_message(message.chat.id, message.message_id)
                await message.answer(message.text.replace(f"{command} ", "").replace(f"{command}", ""))
                return
    except:
        msg = await message.answer("<b>❌ Укажите текст, либо сделайте ответ командой на то сообщение которое я должен сказать!</b>\nПример: !say привет; !скажи привет")
        await as_del_msg(message.chat.id, msg.message_id, 30)
        await as_del_msg(message.chat.id, message.message_id, 30)
        return

       
