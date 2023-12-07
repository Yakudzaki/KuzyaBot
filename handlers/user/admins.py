import html

from loader import dp, bot
from aiogram import types
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from settings import topa_username, whitelist, botik_id, botovod_id
from ..f_lib.shield import anti_advert_t, anti_advert
from ..f_lib.other import as_del_msg


@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['админс', "админы"], commands_prefix='!/.')
async def get_admin_list(message: types.Message):
    

    
    if message.reply_to_message:
        if message.reply_to_message.from_user.id in whitelist:
            id = message.reply_to_message.message_id
            users = message.from_user
            msg = await message.reply(f"<b>❌ Админы не будут вызваны!</b>\
            \n * * * \n<b>Эта команда отправляется в ответ на сообщение.</b>\n * * * \nИ сообщение, в ответ на которое <a href='tg://user?id={users.id}'>вы</a> пытались вызвать админов, отправлено неприкосновенным лицом. Либо вы ошиблись целью.")
            await as_del_msg(message.chat.id, msg.message_id, 10)
            await as_del_msg(message.chat.id, message.message_id, 10)
            return
    else:
        msg = await message.reply("Эту команду следует отправлять в ответ на сообщение.")
        await as_del_msg(message.chat.id, msg.message_id, 10)
        await as_del_msg(message.chat.id, message.message_id, 10)
        return
    
    admins = await message.chat.get_administrators()
    for admin in admins:
        if admin.user.id == message.reply_to_message.from_user.id:
            msg_to = await message.reply(f"<b>❌ Админы не будут вызваны!</b>\
            \n * * * \n<b>Эта команда отправляется в ответ на сообщение.</b>\n * * * \nИ сообщение, в ответ на которое <a href='tg://user?id={users.id}'>вы</a> пытались вызвать админов, отправлено неприкосновенным лицом. Либо вы ошиблись целью.")
            await as_del_msg(message.chat.id, msg.message_id, 10)
            await as_del_msg(message.chat.id, message.message_id, 10)
            return
    
    users = message.from_user
    
    
    if check_user(users.id) == False and message.reply_to_message.from_user.id != botik_id:
        etype = ["url", "text_link", "mention", "text_mention"]
        if check_user(message.reply_to_message.from_user.id):
            bad_user_in_base = False
        else:
            bad_user_in_base = True
        

        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        
        try:
            stop = await anti_advert_t(message.reply_to_message, etype, bad_user_in_base, warner)  
            if stop != None:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                return
            else:
                stop = await anti_advert(message.reply_to_message, etype, bad_user_in_base, warner)  
                if stop != None:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    return
        except:
            pass

    user = create_user(users.id, users.username, users.first_name)
    
    msg = str(f"🚨 Админы вызваны товарищем <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a>!\n\n")
    i = 1
    
    for admin in admins:
        if admin.user.is_bot:
            continue
        
        if admin.user.username == topa_username:   #исключение из команды вызова самого Топы (Кто еще будет?)
            continue

        
        i = i + 1
        msg += f"@{admin.user.username}\n"
        
        if i == 5:
            
            if message.reply_to_message:
                id = message.reply_to_message.message_id
                await bot.send_message(message.chat.id, msg, reply_to_message_id=id)
                i = 0
                msg = ""
    

    id = message.reply_to_message.message_id
    await bot.send_message(message.chat.id, msg, reply_to_message_id=id)
        
        
async def call_all(message: types.Message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id in whitelist:
            id = message.reply_to_message.message_id
            users = message.from_user
            msg = await message.reply(f"<b>❌ Админы не будут вызваны!</b>\
            \n * * * \n<b>Эта команда отправляется в ответ на сообщение.</b>\n * * * \nИ сообщение, в ответ на которое <a href='tg://user?id={users.id}'>вы</a> пытались вызвать админов, отправлено неприкосновенным лицом. Либо вы ошиблись целью.")
            await as_del_msg(message.chat.id, msg.message_id, 10)
            await as_del_msg(message.chat.id, message.message_id, 10)
            return
    else:
        msg = await message.reply("Эту команду следует отправлять в ответ на сообщение.")
        await as_del_msg(message.chat.id, msg.message_id, 10)
        await as_del_msg(message.chat.id, message.message_id, 10)
        return
       
    admins = await message.chat.get_administrators()
    for admin in admins:
        if admin.user.id == message.reply_to_message.from_user.id:
            msg_to = await message.reply(f"<b>❌ Админы не будут вызваны!</b>\
            \n * * * \n<b>Эта команда отправляется в ответ на сообщение.</b>\n * * * \nИ сообщение, в ответ на которое <a href='tg://user?id={users.id}'>вы</a> пытались вызвать админов, отправлено неприкосновенным лицом. Либо вы ошиблись целью.")
            await as_del_msg(message.chat.id, msg.message_id, 10)
            await as_del_msg(message.chat.id, message.message_id, 10)
            return
    
    users = message.from_user
    user = create_user(users.id, users.username, users.first_name)

    msg = str(f"🚨 Админы вызваны товарищем <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a>!\n\n")
    i = 1
    
    for admin in admins:
        if admin.user.is_bot:
            continue
        if admin.user.username == topa_username:   #исключение из команды вызова самого Топы (Кто еще будет?)
            continue

        i = i + 1
        msg += f"@{admin.user.username}\n"
        
        if i == 5: 
            if message.reply_to_message:
                id = message.reply_to_message.message_id
                await bot.send_message(message.chat.id, msg, reply_to_message_id=id)
                i = 0
                msg = ""
    

    id = message.reply_to_message.message_id
    await bot.send_message(message.chat.id, msg, reply_to_message_id=id)