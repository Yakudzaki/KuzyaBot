from loader import dp, bot
from aiogram import types
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
import datetime
import html


@dp.message_handler(commands=["warn", "варн"], commands_prefix="/!.", is_chat_admin=True)
async def warn_handler(message: types.Message):

    if not message.reply_to_message:
        return
    
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
    
    user = message.from_user
    reply = message.reply_to_message.from_user
    chat = message.chat

        
    res = create_user(reply.id, reply.username, reply.first_name)
    create_warner(chat.id, reply.id)
    res_w = get_warner(chat.id, reply.id)
    
    if int(res_w[2]) >= int(3):
        try:
            await bot.kick_chat_member(message.chat.id, reply.id, types.ChatPermissions(False))
            await message.answer(f"⚠️ | Пользователь <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> набрал больше, чем максимальное количество предупреждений, в результате чего должен быть заблокирован!")
        except:
            await message.answer(f"⚠️ | Админ <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> получил слишком много предупреждений!")
            return
        return
    
    if int(res_w[2]) == int(2):
        add_warning(chat.id, reply.id)
        try:
            await bot.kick_chat_member(message.chat.id, reply.id, types.ChatPermissions(False))
            await message.answer(f"⚠️ | Пользователь <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> получил третье предупреждение, в результате чего был заблокирован!")
        except:
            await message.answer(f"⚠️ | Админ <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> получил третье предупреждение!")
            return
        return
    
    if int(res_w[2]) == int(1):
        add_warning(chat.id, reply.id)
        try:
            await bot.restrict_chat_member(message.chat.id, reply.id, types.ChatPermissions(False), until_date=datetime.timedelta(hours=24))
            await message.answer(f"⚠️ | Пользователь <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> получил второе предупреждение, в результате чего был замучен на 2 часа!")
        except:
            await message.answer(f"⚠️ | Админ <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> получил второе предупреждение!")
        return
        
    adminse = await message.chat.get_administrators()
    admino = 0
    for admin in adminse:
        if admin.user.id == reply.id:
            admino = 1
            continue

    if admino == 0:
        add_warning(chat.id, reply.id)
        res_w = get_warner(chat.id, reply.id)
        await message.answer(f"⚠️ | <a href='tg://user?id={user.id}'>Администратор</a> выдал варн пользователю <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a>\nВсего предупреждений ({res_w[2]}/3)")
        return
    else:
        add_warning(chat.id, reply.id)
        res_w = get_warner(chat.id, reply.id)
        await message.answer(f"⚠️ | Админ <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> получил предупреждение!")
        return

    return




@dp.message_handler(commands=["unwarn", "анварн"], commands_prefix="/!.", is_chat_admin=True)
async def unwarn_handler(message: types.Message):
    
    if not message.reply_to_message:
        return

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

    user = message.from_user
    reply = message.reply_to_message.from_user
    chat = message.chat
    

    res = create_user(reply.id, reply.first_name, reply.username)
    
    create_warner(chat.id, reply.id)
    
    res_w = get_warner(chat.id, reply.id)

    
    if int(res_w[2]) == int(0):
        await message.answer(f"❌ У Пользователя <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> нет предупреждений!")
        return
    if int(res_w[2]) < int(0):
        await message.answer(f"❌ У Пользователя <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a> отрицательные предупреждения!")
        add_warning(chat.id, reply.id)
        return
    
    take_warning(chat.id, reply.id)
    res_w = get_warner(chat.id, reply.id)
    await message.answer(f"⚠️ | <a href='tg://user?id={user.id}'>Администратор</a> забрал варн у пользователя <a href='tg://user?id={res[0]}'>{html.escape(res[2])}</a>\nВсего предупреждений ({res_w[2]}/3)")
    return
