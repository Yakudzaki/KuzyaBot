from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter
from aiogram.types import ChatMemberAdministrator, ChatMemberOwner, ChatPermissions, Message
import datetime
import time
import html
from utils.db.db_utils_сhats import *
from utils.db.db_utils_warning import *
from utils.db.db_utils_users import *
from ..f_lib.other import message_user_get_ban
from settings import *


#Замутить юзера
@dp.message_handler(commands=['мут', 'mute'], commands_prefix='!?./', is_chat_admin=True)
async def mute(message: types.Message):

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
    
    muted = await message_user_get_ban(message)
    
    if muted ==  None:
        await message.reply("Цель замучивания не определена!")
        return
    
    text_l = message.text
    for entity in message.entities:
        text_l = text_l[:entity.offset] + text_l[entity.offset + entity.length:]
        break
    
    if len(text_l.split()) == 1:
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(muted[2])
        await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(False))
        await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🔇| Замутил: <a href="tg://user?id={muted[0]}">{nick2}</a>\n⏰| Срок: Навсегда')
        return
    
    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(text_l.split()[3:])
    except:
        try:
        
            mute = message.text.split()[1]
            
            muteint = mute.split("ч")[0]
            muteint = muteint.split("д")[0]
            muteint = muteint.split("м")[0]
            muteint = muteint.split("c")[0]
            
            muteint = muteint.split("h")[0]
            muteint = muteint.split("d")[0]
            muteint = muteint.split("m")[0]
            muteint = muteint.split("s")[0]
            
            mutetype = mute.replace(f"{muteint}", "")
            muteint = int(muteint)
            
            comment = " ".join(text_l.split()[2:])
    
        except:
            muteint = 0
            comment = " ".join(text_l.split()[1:])

    try:
        nick = html.escape(message.from_user.first_name)
        nick2 = html.escape(muted[2])
        comment = html.escape(comment)
        
        if muteint <= 0:
            await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(False))
            mut_type = 'Навсегда'
            
            if not mutetype.lower().startswith('ч') and not mutetype.lower().startswith('h') and not mutetype.lower().startswith('м') and not mutetype.lower().startswith('m') and not mutetype.lower().startswith('д') and not mutetype.lower().startswith('d'):
                    comment = " ".join(text_l.split()[1:])
                    comment = html.escape(comment)

        elif mutetype.lower().startswith('ч') or mutetype.lower().startswith('h'):
            await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(False), until_date=datetime.timedelta(hours=muteint))
            mut_type = f'{muteint} ч.'

        elif mutetype.lower().startswith('м') or mutetype.lower().startswith('m'):
            await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(False), until_date=datetime.timedelta(minutes=muteint))
            mut_type = f'{muteint} м.'

        elif mutetype.lower().startswith('д') or mutetype.lower().startswith('d'):
            await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(False), until_date=datetime.timedelta(days=muteint))
            mut_type = f'{muteint} д.'
       
        elif mutetype.lower().startswith('с') or mutetype.lower().startswith('s'):
            if muteint >= 60:
                await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(False), until_date=int(time.time() + muteint))
                mut_type = f'{muteint} cек.'
            else:
                await message.reply('Высокая вероятность вечного мута!')
                return
        else:
            await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(False))
            comment = " ".join(text_l.split()[1:])
            comment = html.escape(comment)
            mut_type = 'Навсегда'
            
        if comment != "":
            await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🔇| Замутил: <a href="tg://user?id={muted[0]}">{nick2}</a>\n⏰| Срок: {mut_type}\n📃| Причина: {comment}')
        else:
            await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🔇| Замутил: <a href="tg://user?id={muted[0]}">{nick2}</a>\n⏰| Срок: {mut_type}')
    except:
        await message.reply('Не лучшая идея...')

#Размутить юзера
@dp.message_handler(commands=['размут', 'unmute', 'анмут'], commands_prefix='!?./', is_chat_admin=True)
async def unmute(message: types.Message):
   
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
    
    muted = await message_user_get_ban(message)
    
    if muted == None:
        await message.reply("Цель размучивания не определена!")
        return
    
    await bot.restrict_chat_member(message.chat.id, muted[0], ChatPermissions(True, True, True, True, True, True, True, True, True, True, True, True, True, True, True))
    nick = html.escape(message.from_user.first_name)
    nick2 = html.escape(muted[2])
    await message.reply(f'👤| Администратор: <a href="tg://user?id={message.from_user.id}">{nick}</a>\n🔊| Размутил: <a href="tg://user?id={muted[0]}">{nick2}</a>')



#Антимат для юзера
@dp.message_handler(commands=['антимат'], commands_prefix='+')
async def mute(message: types.Message):
    
    if not message.reply_to_message:

        create_user(message.chat.id, message.from_user.username, message.from_user.first_name)
        create_warner(message.chat.id, message.reply_to_message.from_user.id)

        warner = get_warner(message.chat.id, message.from_user.id)
        await message.reply(f"Ваш персональный шанc антимата равен: [{warner[3]}]")
        return

                                   

    create_user(message.reply_to_message.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name)
    create_warner(message.chat.id, message.reply_to_message.from_user.id)

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
    
    command = message.text.lower().split()[0]
    matex_status = message.text.lower().replace(f'{command} ', "")
    if matex_status == command:
        await message.reply("Укажите значение шанса!")
        return
    try:
        if int(matex_status) >= 0:
            set_matex_status(message.chat.id, message.reply_to_message.from_user.id, int(matex_status))
            id = message.reply_to_message.message_id
            msg = f"Ваш шанс антимата установлен на {matex_status}!"
            await bot.send_message(message.chat.id, msg, reply_to_message_id=id)
        else:
            await message.reply("Шанс не может быть отрицательным!")
    except:
        matex_status = len(matex_status)
        set_matex_status(message.chat.id, message.reply_to_message.from_user.id, matex_status)
        id = message.reply_to_message.message_id
        msg = f"Ваш шанс антимата установлен на {matex_status}!"
        await bot.send_message(message.chat.id, msg, reply_to_message_id=id)