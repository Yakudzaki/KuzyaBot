from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, Text
from loguru import logger
from keyboards.inline.help_kb import buttons
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from settings import legal_chats, topa_chat_invite, yakudza_url
from app import server_dir

    
@dp.message_handler(commands=['хелп', 'команды', 'помощь', 'help'], commands_prefix='!?./')
async def help_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.chat.id not in legal_chats and message.chat.type != 'private':
        await message.answer(f"❌ Я создан исключительно для чата <a href='{topa_chat_invite}'>Опа Это Топа</a>!", parse_mode="html", disable_web_page_preview=True)
        await message.answer(f"Айди вашего чата: [{str(message.chat.id)}]\nДоговаривайтесь с <a href='{yakudza_url}'>создателем</a> бота.", parse_mode="html", disable_web_page_preview=True)

        if check_chat(message.chat.id):
            create_chat_with_info(message.chat.id, f"НЕЛЕГАЛ: {message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")
            chat = get_chat(chats)
        await bot.leave_chat(message.chat.id)
        return
        
    
    user = message.from_user
    create_user(user.id, user.username, user.first_name)
    await message.answer("<b>📚 Выберите раздел:</b>", reply_markup=buttons)
    
@dp.message_handler(lambda message: message.text.lower() == "антимат")
async def rp_spis(message: types.Message):
    nick = html.escape(message.from_user.first_name)
    await message.reply(f"<a href='tg://user?id={message.from_user.id}'>{nick}</a>, вот список команд системы антимата:\n\
                           \n🔒 <code>+Антимат</code> (0-100) — Установить шанс антимата пресонально для участника чата. Мут и прочее будут, как в настройках чата\
                           \n🔒 <code>!Мутмат (секунды)</code> — Установить мут антимата. (Если меньше 60, то мут отключается)\
                           \n🔒 <code>!Шансмат (проценты)</code> — Установить шанс антимата. (от 0 до 100)\
                           \n🔒 <code>!Репмат</code> (0,1) — Включить или выключить падение репутации от мата. (0 - выкл. 1 - вкл.)\
                           \n\n👌 <code>!Антимат</code> — Узнать текущие шанс и мут антимата.", parse_mode="html")
                           
@dp.message_handler(lambda message: message.text.lower() == "спамлим")
async def rp_spis(message: types.Message):
    nick = html.escape(message.from_user.first_name)
    await message.reply(f"<a href='tg://user?id={message.from_user.id}'>{nick}</a>, вот список команд системы антиспама:\n\
                           \nУстановить ограничения в чате на количество сообщений подряд, за короткое время, от одного человека:\
                           \n🔒 <code>!фотолимит</code> (число) — для изображений.\
                           \n🔒 <code>!видеолимит</code> (число) — для видео.\
                           \n🔒 <code>!стиклимит</code> (число) — для стикеров.\
                           \n🔒 <code>!гифлимит</code> (число) — для GIF.\
                           \n🔒 <code>!текстлимит</code> (число) — для текстовых сообщений.\
                           \n\n👌 <code>!спамлимиты</code> — Узнать текущие настройки антиспама", parse_mode="html")
                           
@dp.message_handler(lambda message: message.text.lower() == "падежи")
async def padeghes(message: types.Message):
    await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_PHOTO)
    
    await bot.send_photo(message.chat.id, open(server_dir + f"/data/padegh.jpg", "rb"), reply_to_message_id=message.message_id)
    
@dp.message_handler(lambda message: message.text.lower() == "заповеди админа")
async def padeghes(message: types.Message):
    await bot.send_chat_action(message.chat.id, types.ChatActions.UPLOAD_PHOTO)
    
    await bot.send_photo(message.chat.id, open(server_dir + f"/data/odmen.jpg", "rb"), reply_to_message_id=message.message_id)