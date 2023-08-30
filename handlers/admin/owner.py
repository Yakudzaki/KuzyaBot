from aiogram import types
import logging
import globales
from loader import bot
from settings import *
from utils.db import *
from .owner_menu import dev_handler


async def owner_func(message: types.Message, mctp, mrm, chat):
    if mctp == True:
        stop = await dev_handler(message)
        if stop == True:
            return
    
    if message.from_user.id not in botovod_id:
        return
    
    if message.text.lower() == "челинфо" and mctp == False and mrm == True:
        ment = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id,)
        await message.answer(f"{ment}")

#мессаджинфо
    if message.text.lower() == "мессинфо" and mrm == True:
        from html import escape
        await message.answer(f"{escape(str(message.reply_to_message))}")
        # await message.answer(f"len(message.text)={len(message.reply_to_message.text)}")
        # await message.answer(f"len(html.escape(message.text))={len(html.escape(message.reply_to_message.text))}")

#ЧАТИНФО
    if message.text.lower() == "чатинфо" and mctp == False:

        await message.answer(f"Айди вашего чата: [{str(chat_id)}].\
        \nШанс антимата - {str(chat[1])} процентов.\
        \nМут антимата - {str(chat[2])} секунд.\
        \nРепутация антимата - [{str(chat[7]).replace('1', 'Включено').replace('0', 'Выключено')}].\
        \nТекущий статус приколов - [{str(chat[4]).replace('1', 'Включено').replace('0', 'Выключено')}].\
        \nТекущий статус щита - [{str(chat[13]).replace('1', 'Включено').replace('0', 'Выключено').replace('0', 'Антибот')}].\
        \n\nТекущее приветствие: \n{chat[5]}[никнейм]{chat[6]}")
#БлокСтик
    if message.text.lower() == "блокстик" and mctp == False:
        from ..f_lib.other import restrict_chat
        await restrict_chat(message)

#ПОЗВАТЬ ВСЕХ
    
    if mctp == False and message.text.lower().startswith("великий созыв"):
        from ..f_lib.other import call_everybody

        await call_everybody(message)

#ЛИЧКА С КУЗЕЙ
    #ПРОВЕРИТЬ ЮЗЕРОВ НА ПРИНАДЛЕЖНОСТЬ ЧАТАМ
    
    if mctp == True and message.text.lower() == 'чекнуть мемберов':
        from ..f_lib.other import check_all_members
        await check_all_members(message)

    #ПОСЫЛАТЬ СООБЩЕНИЯ
    
    if mctp == True:
        global reply_transfer
        i = 0
        if reply_transfer == 0 and message.text.lower().startswith('https://t.me'):
            import re
            
            global message_transfer_id
            global text_name
            global text_id
            
            match = re.search(r'(?s:.*)/(\w+)', message.text)
            if match:
                message_transfer_id = match.group(1)
                reply_transfer = 1
                
                await message.reply(f"Получено ID сообщения - [{message_transfer_id}]")
                text = message.text.replace(f"/{message_transfer_id}", "")
                if "https://t.me/c/" in text:
                    try:
                        text_id = int(text.replace("https://t.me/c/", "-100"))
                        await message.reply(f"Получено ID чата - [{text_id}]")
                        reply_transfer = 1
                        return
                    except:
                        await message.reply(f"Случилась хрень.")
                else:
                    if "https://t.me/" in text: 
                        text_name = text.replace("https://t.me/", "@")
                        await message.reply(f"Получено Username чата - [{text_name}]")
                        reply_transfer = 1
                        return
            return

        

        if reply_transfer == 1 and message.text.lower().startswith(".сенд "):
            if text_name != "":
                await bot.send_chat_action(text_name, types.ChatActions.TYPING)
                await bot.send_message(text_name, message.text.replace(".сенд ", ""))
                await message.reply(f"ОТПРАВЛЕНО В {text_name}")
                reply_transfer = 0
                text_name = ""
                return
            if text_id != 0:
                await bot.send_chat_action(text_id, types.ChatActions.TYPING)
                await bot.send_message(text_id, message.text.replace(".сенд ", ""))
                await message.reply(f'ОТПРАВЛЕНО В https://t.me/c/{str(text_id).replace("-100", "")}')
                reply_transfer = 0
                text_id = 0
                return
        
        if reply_transfer == 1 and message.text.lower() == "стоп":
            reply_transfer = 0 
            message_transfer_id = 0
            text_name = ""
            text_id = 0
            await message.reply(f"Сброшено айди сообщения и чата.")
            return
        
        if reply_transfer == 1:
            try:
                if text_name != "":
                    await bot.send_chat_action(text_name, types.ChatActions.TYPING)
                    await bot.send_message(text_name, message.text, reply_to_message_id=message_transfer_id)
                    await message.reply(f"ОТПРАВЛЕНО В {text_name} в ответ на сообщение {message_transfer_id}")
                    reply_transfer = 0
                    text_name = ""
                    return
                if text_id != 0:
                    await bot.send_chat_action(text_id, types.ChatActions.TYPING)
                    await bot.send_message(text_id, message.text, reply_to_message_id=message_transfer_id)
                    await message.reply(f'ОТПРАВЛЕНО В https://t.me/c/{str(text_id).replace("-100", "")} в ответ на сообщение {message_transfer_id}')
                    reply_transfer = 0
                    text_id = 0
                    return
            except:
                reply_transfer = 0 
                message_transfer_id = 0
                text_name = ""
                text_id = 0
                await message.reply(f"Сброшено айди сообщения и чата. Ибо сообщение не найдено в чате.")


    #ЧИСТКА БАЗЫ
        
        if message.text.lower() == 'чистка базы':
            from ..f_lib.other import clean_db_users
            await clean_db_users(message)

    if message.text.lower() == "!terminate" and message.from_user.id == yakudza_id:
        await message.reply("⌨️ Системная команда -f to force kill\nКод выхода  0\n📼 Вывод: process is killed ")