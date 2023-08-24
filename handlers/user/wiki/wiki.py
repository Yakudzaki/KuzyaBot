from loader import dp, bot
from aiogram import types
import html
from handlers.lib.other import as_del_msg
from settings import time_del
from utils.db.db_utils_warning import *

from .wikipedia_lxml_mod.wikipedia import (
    WikipediaPage,
    page,
    random,
    search,
    set_lang,
    suggest,
    summary,
)

set_lang("ru")



@dp.message_handler(commands=["wiki", "вики"], commands_prefix="/!.")
async def wiki_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    command = message.text.split()[0]
    request = message.text.replace(f"{command} ", "")
    if request == command:
        await message.reply("<b>❌ Укажите запрос!</b>")
        return
    try:
        result = summary(request)
        # result = BeautifulSoup(result, features="lxml").get_text()
    except:
        msg = await message.reply("☹️ По вашему запросу ничего не найдено!")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        await as_del_msg(message.chat.id, message.message_id, time_del)
        return
    
    try:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        msg = await message.reply(f"{html.escape(result)}\n\n🗞 <a href='https://t.me/KuzyaBotNews'>Канал с новостями</a>", disable_web_page_preview=True, parse_mode="html")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        await as_del_msg(message.chat.id, message.message_id, time_del)
    except:
        if len(result) >= 4000:
            i = 0
            while True:
                numb = i*4000
                numb2 = (i+1)*4000
                
                result1 = result[numb:numb2]
                i = i + 1
                
                if result1 != None and result1 != "":
                    if len(result1) >= 4000:
                        result1 = result1 + " …"
                    else:
                        result1 = "… " + result1

                    msg1 = await message.reply(f"{html.escape(result1)}\n\n🗞 <a href='https://t.me/KuzyaBotNews'>Канал с новостями</a>", disable_web_page_preview=True, parse_mode="html")
                    await as_del_msg(message.chat.id, msg1.message_id, time_del)
                    await as_del_msg(message.chat.id, message.message_id, time_del)
                else:
                    return

        else:
            msg2 = await message.reply("☹️ Ваш запрос превысил мои возможности!")
            await as_del_msg(message.chat.id, msg2.message_id, time_del)
            await as_del_msg(message.chat.id, message.message_id, time_del)

@dp.message_handler(commands=["random", "рандом"], commands_prefix="/!.")
async def randomize(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    try:
        try:
            random_title = page(random(pages=1)).url
            random_text = "🔎 Рандомная статья - <a href='" + random_title + "'>*тык*</a>"
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            await message.reply(random_text)
        except:
            try:
                random_title = page(random(pages=1)).url
                random_text = "🔎 Рандомная статья - <a href='" + random_title + "'>*тык*</a>"
                await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                await message.reply(random_text)
            except IndexError:
                await message.reply("😓 Что-то пошло не так, попробуйте ещё раз!")
    except:
        await message.reply("😓 Что-то пошло очень не так, попробуйте ещё раз!")