from loader import dp, bot
import asyncio
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import *
from utils.db.db_utils_сhats import *
from utils.db.db_utils_users import *
from utils.db.db_utils_members import *
import html



@dp.message_handler(lambda message: True, content_types=['new_chat_members'])
async def new_chat_member(message: types.Message):
    if (message.chat.type == 'group' or message.chat.type == 'supergroup'):
        chat_id = message.chat.id
        user = message.new_chat_members[0]
    
    
        
        if user.id == botik_id and message.chat.id != topa_chat_id:
            await message.answer(f"❌ Я создан исключительно для чата <a href='{topa_chat_invite}'>Опа Это Топа</a>!", parse_mode="html", disable_web_page_preview=True)
            await asyncio.sleep(2)
            legal = 0
            chat_id = message.chat.id
            
            legal = 0
            if chat_id in legal_chats:
                legal = 1
            
            if legal == 0:
                await message.answer(f"Айди вашего чата: [{str(chat_id)}]\nДоговаривайтесь с <a href='{yakudza_url}'>создателем</a> бота.", parse_mode="html", disable_web_page_preview=True)

                if check_chat(message.chat.id):
                    create_chat_with_info(message.chat.id, f"НЕЛЕГАЛ: {message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
                await asyncio.sleep(2)
                await bot.leave_chat(message.chat.id)
                return
            if legal == 1:
                if check_chat(message.chat.id):
                    create_chat_with_info(message.chat.id, f"{message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
                return
            
                
        chats = message.chat.id #Отсюда и далее, до пустой строки - внесение чата в базу Кузи.
        chat = get_chat(chats)
        if check_chat(message.chat.id):
            create_chat_with_info(message.chat.id, f"{message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
            chat = get_chat(chats)
        
        if check_user(user.id):
            if user.last_name != None:
                name1 = html.escape(user.first_name)
                name2 = html.escape(user.last_name)
                html.escape(message.from_user.first_name)
                name = f"<a href='tg://user?id={user.id}'>{name1} {name2}</a>"
            else:
                name1 = html.escape(user.first_name)
                name = f"<a href='tg://user?id={user.id}'>{name1}</a>"
        else:
            if check_member(message.chat.id, message.from_user.id) == False:
                ment = await bot.get_chat_member(message.chat.id, message.from_user.id)
                if ment.status != "left" and ment.status != "kicked":
                    create_member(message.chat.id, message.from_user.id, ment.status)
            user_db = get_user(user.id)
            name = f"<a href='tg://user?id={user_db[0]}'>{html.escape(user_db[2])}</a>"
        

        
        m_count = await bot.get_chat_member_count(message.chat.id)
        if m_count != chat[15]:
            set_members_count(message.chat.id, m_count)

        if chat[5] == "" and chat[6] == "":
            return
        
        hello = InlineKeyboardMarkup(row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📝 Правила', url=f"{chat[16]}")
            ],
        ]
    )
        


        if check_chat_m(chat[0]):  #Запись чата в оперативку.
            create_chat_m(chat[0])
        
        chat_m = get_chat_m(chat[0])
        
        set_hello_count(chat_m[0], chat_m[1] + 1)
        names = chat_m[2]
        
        if chat_m[1] == 0:
            set_hello_string(chat_m[0], f'{name}')  
            set_msg_id(chat_m[0], message.message_id)
            await asyncio.sleep(20) #Время ожидания кода остальных новичков, после первого зашедшего.
        
        elif chat_m[1] < 4:
            set_hello_string(chat_m[0], f'{names}, {name}')
            return
        
        else:
            set_hello_string(chat_m[0], f'{names}, {name}')

        chat_m = get_chat_m(chat[0])
        if chat_m[1] == 0:
            return
        
        set_hello_count(chat_m[0], 0)
        
        names = chat_m[2]

        if chat[16] != "" and chat[16] != None:
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            await bot.send_message(message.chat.id, f"{chat[5]}{names}{chat[6]}", parse_mode='html', reply_markup=hello, reply_to_message_id=chat_m[5])
            # set_hello_string(chat_m[0], '')
            return
        
        else:
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            await bot.send_message(message.chat.id, f"{chat[5]}{names}{chat[6]}", parse_mode='html', reply_to_message_id=chat_m[5])
            # set_hello_string(chat_m[0], '')
            return


@dp.message_handler(content_types=['left_chat_member'])
async def left_member(message: types.Message):
    if (message.chat.type == 'group' or message.chat.type == 'supergroup'):
        user = message.left_chat_member
        if user.id != botik_id:
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            if check_member(message.chat.id, user.id):
                delete_member(message.chat.id, user.id)
            
            chat = get_chat(message.chat.id)
            
            m_count = await bot.get_chat_member_count(message.chat.id)
            if m_count != chat[15]:
                set_members_count(message.chat.id, m_count)
            
            nick = html.escape(user.first_name)
            
            if user.id == message.from_user.id:
                await message.answer(f'Пока, <a href="tg://user?id={user.id}">{nick}</a>!😔', parse_mode='html')
                return
            else:
                await message.answer(f'Прощай, <a href="tg://user?id={user.id}">{nick}</a>!😡', parse_mode='html')
                return
        else:
            return
