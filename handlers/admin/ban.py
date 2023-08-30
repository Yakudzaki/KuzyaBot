from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter
import datetime
import time
import html
import asyncio

from utils.db.db_utils_members import *
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from ..f_lib.other import message_user_get_ban
from ..f_lib.pyrogram_f import get_delete_members
from settings import *

@dp.message_handler(commands=['dban', 'дбан', 'дкик', 'dkick'], commands_prefix='!?./', is_chat_admin=True)
async def dban(message: types.Message):
    await ban(message)
    await message_del_main(message, False)


@dp.message_handler(commands=['ban', 'бан', 'кик', 'kick'], commands_prefix='!?./', is_chat_admin=True)
async def ban(message: types.Message):

   
    admins = await message.chat.get_administrators()
    
    restr = False
    for admin in admins:
        if admin.user.id == message.from_user.id:
            if admin.can_restrict_members == True:
                restr = True
                break
            else:
                break
        else:
            continue
    if restr == False:
        await message.reply("У вас недостаточно прав!")
        return
   
    baned = await message_user_get_ban(message)
    
    if baned == None:
        await message.reply("Цель забанивания не определена!")
        return
    
    text_l = message.text
    for entity in message.entities:
        text_l = text_l[:entity.offset] + text_l[entity.offset + entity.length:]
        break
    
    comment = " ".join(text_l.split()[1:])
    
    try:
        await bot.kick_chat_member(message.chat.id, baned[0], types.ChatPermissions(False))
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(baned[2])
        if comment == " ":
            await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🛑| Забанил: <a href="tg://user?id={baned[0]}">{nick2}</a>\n⏰| Срок: навсегда')
        else:
            await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🛑| Забанил: <a href="tg://user?id={baned[0]}">{nick2}</a>\n⏰| Срок: навсегда\n📃| Причина: {comment}')
    
    except:
        await message.reply("Не лучшая идея...")

@dp.message_handler(commands=['разбан', 'unban'], commands_prefix='!?./', is_chat_admin=True)
async def unban(message: types.Message):
   
    admins = await message.chat.get_administrators()
    
    restr = False
    for admin in admins:
        if admin.user.id == message.from_user.id:
            if admin.can_restrict_members == True:
                restr = True
                break
            else:
                break
        else:
            continue
    if restr == False:
        await message.reply("У вас недостаточно прав!")
        return
   
    baned = await message_user_get_ban(message)
    
    if baned == None:
        await message.reply("Цель забанивания не определена!")
        return
    
    await bot.restrict_chat_member(message.chat.id, baned[0], permissions=types.ChatPermissions(True, True, True, True, True, True, True, True, True, True, True, True, True, True, True))
    nick = html.escape(message.from_user.first_name)
    nick2 = html.escape(baned[2])
    
    await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n📲| Разбанил: <a href="tg://user?id={baned[0]}">{nick2}</a>')

@dp.message_handler(commands=['del', 'дел'],commands_prefix="!?./", is_chat_admin=True)
async def message_del(message: types.Message):
    await message_del_main(message, True)



async def message_del_main(message: types.Message, send):
    if not message.reply_to_message:
        if send:
            await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    try:
        if message.content_type!=['text', 'photo', 'document', 'audio', 'video']:
            text = message.text
            if isinstance(message.caption, str):
                caption = message.caption
            else:
                caption = ''
    
            if hasattr(message, 'text') and isinstance(text, str):
                if send:
                    await message.answer(f"\n🗑️| Публикация удалена.", parse_mode="HTML")
                await message.bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
            elif hasattr(message, 'caption') and message.media_group_id not in check_mess:
                check_mess.append(message.media_group_id)
                if send:
                    await message.answer(f"\n🗑️| Публикация удалена.", parse_mode="HTML")
                await message.bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
                check_mess.clear()
                return
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except:
                pass
    except:
        pass

@dp.message_handler(commands=['чист'], commands_prefix='!?./')
async def delall(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return
    
    comment = " ".join(message.text.split()[1:])
    
    allow = 0
    for cleaner in botovod_id:
        if message.from_user.id == cleaner:
            allow = 1
            continue
    
    if allow == 0:  #Айди ботовода
        await message.reply("Вы не властны надо мной!")
        return
    
    del_user_id = message.reply_to_message.from_user.id
    
    if del_user_id != botik_id:
        await message.reply("Эта команда применима только к сообщениям Кузи!")
        return
    
    try:

        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    except:
       await message.reply('Не лучшая идея...')


@dp.message_handler(commands=['созвать', 'озвать', 'где', 'де'],commands_prefix="!./сСГг", is_chat_admin=True)
async def delall(message: types.Message):
    if 'всех' in message.text.lower() or 'актив' in message.text.lower():
        
        from ..f_lib.other import call_everybody
        
        await call_everybody(message)
        
@dp.message_handler(commands=['чистка'],commands_prefix="!./", is_chat_admin=True)
async def delall(message: types.Message):

    mess = await message.reply('Начинаю чистку …')
    chat_id = message.chat.id
    deleted = await get_delete_members([chat_id])
    
    
    for user_id in deleted:
        await asyncio.sleep(1)
        try:
            await bot.kick_chat_member(chat_id, user_id)
        except:
            pass
        if check_user(user_id) == False:
            delete_user(user_id)
    
    for user_id in deleted:
        await asyncio.sleep(1)
        try:
            await bot.restrict_chat_member(chat_id, user_id, permissions=types.ChatPermissions(True, True, True, True, True, True, True, True, True, True, True, True, True, True, True))
        except:
            pass
    
    msg_text = '… заканчиваю чистку.'
    await bot.send_message(chat_id, msg_text, reply_to_message_id=mess.id)
    
    
@dp.message_handler(commands=['кузясброс'], commands_prefix='!?./')
async def kuzunban(message: types.Message):
    
    if message.from_user.id in botovod_id:

    
        baned = await message_user_get(message)
        
        if baned == None:
            await message.reply("Цель Кузясброса не определена!")
            return
        
        set_ban(baned[0], 0)
        
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(baned[2])
        
        await message.reply('Исполнено.')
    
    else:
        return

@dp.message_handler(commands=['кузяразбан'], commands_prefix='!?./')
async def kuzunban(message: types.Message):
    
    if message.from_user.id in botovod_id:

        baned = await message_user_get(message)
        
        if baned == None:
            await message.reply("Цель Кузяразбанивания не определена!")
            return
        
        set_ban(baned[0], 2)
        
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(baned[2])
        
        await message.reply(f'👤| Разраб: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n📲| Кузяразбанил: <a href="tg://user?id={baned[0]}">{nick2}</a>')

    elif message.chat.type != 'private':
    
        admins = await message.chat.get_administrators()
        restr = False
        for admin in admins:
            if admin.user.id == message.from_user.id:
                if admin.can_restrict_members == True:
                    restr = True
                    break
                else:
                    break
            else:
                continue
        if restr == False:
            await message.reply("У вас недостаточно прав!")
            return
        baned = await message_user_get(message)
        if baned == None:
            await message.reply("Цель Кузяразбанивания не определена!")
            return
        
        for admin in admins:
            if admin.user.id == baned[0]:
                await message.reply("Цель Кузяразбанивания не может быть админом чата!")
                return
            else:
                continue
        user = message.from_user
        chat = message.chat
        create_warner(chat.id, baned[0])
        set_kuzya_ban(chat.id, baned[0], 0)
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(baned[2])
        await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n📲| Кузяразбанил: <a href="tg://user?id={baned[0]}">{nick2}</a>')




@dp.message_handler(commands=['кузябан'], commands_prefix='!?./')
async def kuzban(message: types.Message):
    
    if message.from_user.id in botovod_id:
        
        baned = await message_user_get(message)
        
        if baned == None:
            await message.reply("Цель Кузябанивания не определена!")
            return
    
        set_ban(baned[0], 3)
        
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(baned[2])
        
        await message.reply(f'👤| Разраб: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🛑| Кузябанил: <a href="tg://user?id={baned[0]}">{nick2}</a>')
    
    elif message.chat.type != 'private':

        admins = await message.chat.get_administrators()
        restr = False
        for admin in admins:
            if admin.user.id == message.from_user.id:
                if admin.can_restrict_members == True:
                    restr = True
                    break
                else:
                    break
            else:
                continue
        if restr == False:
            await message.reply("У вас недостаточно прав!")
            return
        baned = await message_user_get(message)
        if baned == None:
            await message.reply("Цель Кузябанивания не определена!")
            return
        for admin in admins:
            if admin.user.id == baned[0]:
                await message.reply("Цель Кузябанивания не может быть админом чата!")
                return
            else:
                continue
        chat = message.chat
        create_warner(chat.id, baned[0])
        set_kuzya_ban(chat.id, baned[0], 1)
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(baned[2])
        await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🛑| Кузябанил: <a href="tg://user?id={baned[0]}">{nick2}</a>')