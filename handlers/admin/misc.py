from loader import dp, bot
from aiogram import types
from utils.db.db_utils_users import *
from utils.db.db_utils_сhats import *
from utils.db.relations.db_utils_moniker import *
from settings import *
from ..lib.other import message_user_get
import html

@dp.message_handler(commands=["правила", "rules"], commands_prefix="+", is_chat_admin=True)
async def rules_handler(message: types.Message):
    users = message.from_user
    create_user(users.id, users.username, users.first_name)
    rules = message.text.replace("+правила ", "").replace("+Правила ", "").replace("+rules ", "").replace("+Rules ", "")
    rules = rules.replace("+правила", "").replace("+Правила", "").replace("+rules", "").replace("+Rules", "")

    if "://" in rules or rules == "":
        chat = message.chat.id
        set_rules(chat, rules)
        await message.reply("<b>✅ Правила успешно изменёны!</b>")
        return
    else:
        await message.reply("<b>❌ Правила должны быть ссылкой!</b>")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



#Установить шанс антимата
@dp.message_handler(commands=["шансмат"], commands_prefix="/!.", is_chat_admin=True)
async def vermat_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)

    vermat = message.text.replace("!шансмат ", "").replace("/шансмат ", "").replace(".шансмат ", "").replace("!Шансмат ", "").replace("/Шансмат ", "").replace(".Шансмат ", "")
    raises = ["!шансмат", "/шансмат", ".шансмат", "!Шансмат", "/Шансмат", ".Шансмат", ""]
    if vermat in raises:
        await message.reply("<b>❌ Укажите значение!</b>")
        return
    if int(vermat) > 100:
        await message.reply("<b>❌ Укажите верное значение!</b>\n От нуля до ста.")
        return
    if int(vermat) < 0:
        await message.reply("<b>❌ Укажите верное значение!</b>\n От нуля до ста.")
        return
    else:
        chats = message.chat.id
        set_vermat(chats, vermat)
        await message.reply("<b> ✅ Шанс антимата успешно изменён!</b>")


#Установить мут антимата
@dp.message_handler(commands=["мутмат"], commands_prefix="/!.", is_chat_admin=True)
async def secmat_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)

    secmat = message.text.replace("!мутмат ", "").replace("/мутмат ", "").replace(".мутмат ", "").replace("!Мутмат ", "").replace("/Мутмат ", "").replace(".Мутмат ", "")
    raises = ["!мутмат", "/мутмат", ".мутмат", "!Мутмат", "/Мутмат", ".Мутмат", ""]
    if secmat in raises:
        await message.reply("<b>❌ Укажите значение в секундах!</b>")
        return
    if int(secmat) < 0:
        await message.reply("<b>❌ Укажите верное значение!</b>\nОт нуля секунд до бесконечности.")
        return
    else:
        chats = message.chat.id
        set_secmat(chats, secmat)
        await message.reply("<b> ✅ Мут антимата успешно изменён!</b>")


#Установить репутацию от антимата
@dp.message_handler(commands=["репмат"], commands_prefix="/!.", is_chat_admin=True)
async def secmat_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    repmat = message.text.replace("!репмат ", "").replace("/репмат ", "").replace(".репмат ", "").replace("!Репмат ", "").replace("/Репмат ", "").replace(".Репмат ", "")
    raises = ["!репмат", "/репмат", ".репмат", "!Репмат", "/Репмат", ".Репмат", ""]
    if repmat in raises:
        await message.reply("<b>❌ Укажите значение, 0(выкл) или 1(вкл)!</b>")
        return
    if int(repmat) != 0 and int(repmat) != 1:
        await message.reply("<b>❌ Укажите верное значение!</b>\n0 - выключить, и 1 - включить!")
        return
    else:
        chats = message.chat.id
        set_matrep(chats, repmat)
        await message.reply("<b> ✅ Падение репутации от антимата успешно изменено!</b>")


#Установить выключатель развлекух
@dp.message_handler(commands=["игры"], commands_prefix="/!.")
async def secmat_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    chats = message.chat.id
    chat = get_chat(chats)
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            chat = get_chat(chats)
            
    funny_func = message.text.replace("!игры ", "").replace("/игры ", "").replace(".игры ", "").replace("!Игры ", "").replace("/Игры ", "").replace(".Игры ", "")
    raises = [".Игры", "/Игры", "!Игры", ".игры", "/игры", "!игры", ""]
    if funny_func in raises:
        await message.reply(f"🎰 Текущий статус приколов - [{str(chat[4]).replace('1', 'Включено').replace('0', 'Выключено')}].\
        \n Админы могут ввести <code>!игры 1</code> чтобы включить, или <code>!игры 0</code> чтобы выключить игры с Кузей.")
        return
    else:
        us = message.from_user
        adminse = await message.chat.get_administrators()
        admino = 0
        for admin in adminse:
            if admin.user.id == us.id or us.id == 1087968824:
                admino = 1
                continue
        if admino == 0:
            return
        else:
            try:
                chats = message.chat.id
                set_funny_func(chats, int(funny_func))
                if int(funny_func) == 0:
                    await message.reply("<b> ❌ Развлечения успешно выключены!</b>")
                    return
                if int(funny_func) == 1:
                    await message.reply("<b> ✅ Развлечения успешно включены!</b>")
                    return

                else:
                    await message.reply("<b> ❌ Что-то пошло не так!\nУстановите верное значение! \n<code>!игры 0</code>  — выкл. игры <code>!игры 1</code> — вкл. игры.</b>")
                    return
            except:
                await message.reply("<b> ❌ Что-то серьёзно пошло не так!</b>")
                return


#Установить ЩИТ!!!!!

@dp.message_handler(commands=["щит"], commands_prefix="/!.")
async def secmat_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    chats = message.chat.id
    chat = get_chat(chats)
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            chat = get_chat(chats)
            
    stat0 = "Щит выключен!"
    stat1 = "Включена антиреклама!"
    stat2 = "Включены антиреклама и антибот!"
    
    us = message.from_user
    
    adminse = await message.chat.get_administrators()
    admino = 0
    
    for admin in adminse:
        if admin.user.id == us.id or us.id == 1087968824:
            admino = 1
            continue
    
    if admino == 0:
        await message.reply(f'🛡 Текущий статус щита - [{str(chat[13]).replace("0", stat0).replace("1", stat1).replace("2", stat2)}]')
    
    if admino == 1:
        if chat[13] == 0:
            set_shield(message.chat.id, 1)
        if chat[13] == 1:
            set_shield(message.chat.id, 2)
        if chat[13] == 2:
            set_shield(message.chat.id, 0)
        
        chat = get_chat(chats)
        await message.reply(f'🛡 Статус щита изменён на: [{str(chat[13]).replace("0", stat0).replace("1", stat1).replace("2", stat2)}]')

#Установить первое приветствие
@dp.message_handler(commands=["setwelcome1"], commands_prefix="!/.", is_chat_admin=True)
async def welcome1_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    welcome1 = message.text.replace("!setwelcome1 ", "").replace("/setwelcome1 ", "").replace(".setwelcome1 ", "").replace("!Setwelcome1 ", "").replace("/Setwelcome1 ", "").replace(".Setwelcome1 ", "").replace("!setwelcome1", "").replace("/setwelcome1", "").replace(".setwelcome1", "").replace("!Setwelcome1", "").replace("/Setwelcome1", "").replace(".Setwelcome1", "").replace("_", " ")
    if len(welcome1) > 150:
        await message.reply("<b>❌ Приветствие(1) не может содержать больше 150 символов!</b>")
        return
    elif "https://" in welcome1:
        await message.reply("<b>❌ Приветствие(1) не может содержать ссылок!</b>")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return
    else:
        chats = message.chat.id
        set_welcome1(chats, welcome1)
        await message.reply("<b>✅ Приветствие(1) успешно изменено!</b>")
        return


#Установить второе приветствие
@dp.message_handler(commands=["setwelcome2"], commands_prefix="!/.", is_chat_admin=True)
async def welcome2_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    welcome2 = message.text.replace("!setwelcome2 ", "").replace("/setwelcome2 ", "").replace(".setwelcome2 ", "").replace("!Setwelcome2 ", "").replace("/Setwelcome2 ", "").replace(".Setwelcome2 ", "").replace("!setwelcome2", "").replace("/setwelcome2", "").replace(".setwelcome2", "").replace("!Setwelcome2", "").replace("/Setwelcome2", "").replace(".Setwelcome2", "").replace("_", " ")
    if len(welcome2) > 150:
        await message.reply("<b>❌ Приветствие(2) не может содержать больше 150 символов!</b>")
        return
    elif "https://" in welcome2:
        await message.reply("<b>❌ Приветствие(2) не может содержать ссылок!</b>")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return
    else:
        chats = message.chat.id
        set_welcome2(chats, welcome2)
        await message.reply("<b>✅ Приветствие(2) успешно изменено!</b>")
        return


#Установить спам-лимит на фото
@dp.message_handler(commands=["фотолимит"], commands_prefix="/!.", is_chat_admin=True)
async def photo_limit_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    photo_limit = message.text.replace("!фотолимит ", "").replace("/фотолимит ", "").replace(".фотолимит ", "").replace("!Фотолимит ", "").replace("/Фотолимит ", "").replace(".Фотолимит ", "")
    raises = ["!фотолимит", "/фотолимит", ".фотолимит", "!Фотолимит", "/Фотолимит", ".Фотолимит", ""]
    if photo_limit in raises:
        await message.reply("<b>❌ Укажите значение!</b>")
        return
    if int(photo_limit) < 0:
        await message.reply("<b>❌ Укажите верное значение!</b>\n От нуля до бесконечности.")
        return
    else:
        chats = message.chat.id
        set_photo_limit(chats, photo_limit)
        await message.reply(f"<b> ✅ Фото-антиспам успешно установлен на {photo_limit}!</b>")


#Установить спам-лимит на видео
@dp.message_handler(commands=["видеолимит"], commands_prefix="/!.", is_chat_admin=True)
async def video_limitt_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    video_limit = message.text.replace("!видеолимит ", "").replace("/видеолимит ", "").replace(".видеолимит ", "").replace("!Видеолимит ", "").replace("/Видеолимит ", "").replace(".Видеолимит ", "")
    raises = ["!видеолимит", "/видеолимит", ".видеолимит", "!Видеолимит", "/Видеолимит", ".Видеолимит", ""]
    if video_limit in raises:
        await message.reply("<b>❌ Укажите значение!</b>")
        return
    if int(video_limit) < 0:
        await message.reply("<b>❌ Укажите верное значение!</b>\n От нуля до бесконечности.")
        return
    else:
        chats = message.chat.id
        set_video_limit(chats, video_limit)
        await message.reply(f"<b> ✅ Видео-антиспам успешно установлен на {video_limit}!</b>")


#Установить спам-лимит на стикеры
@dp.message_handler(commands=["стиклимит"], commands_prefix="/!.", is_chat_admin=True)
async def sticker_limit_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    sticker_limit = message.text.replace("!стиклимит ", "").replace("/стиклимит ", "").replace(".стиклимит ", "").replace("!Стиклимит ", "").replace("/Стиклимит ", "").replace(".Стиклимит ", "")
    raises = ["!стиклимит", "/стиклимит", ".стиклимит", "!Стиклимит", "/Стиклимит", ".Стиклимит", ""]
    if sticker_limit in raises:
        await message.reply("<b>❌ Укажите значение!</b>")
        return
    if int(sticker_limit) < 0:
        await message.reply("<b>❌ Укажите верное значение!</b>\n От нуля до бесконечности.")
        return
    else:
        chats = message.chat.id
        set_sticker_limit(chats, sticker_limit)
        await message.reply(f"<b> ✅ Стик-антиспам успешно установлен на {sticker_limit}!</b>")


#Установить спам-лимит на гифки
@dp.message_handler(commands=["гифлимит"], commands_prefix="/!.", is_chat_admin=True)
async def anmiation_limit_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    anmiation_limit = message.text.replace("!гифлимит ", "").replace("/гифлимит ", "").replace(".гифлимит ", "").replace("!Гифлимит ", "").replace("/Гифлимит ", "").replace(".Гифлимит ", "")
    raises = ["!гифлимит", "/гифлимит", ".гифлимит", "!Гифлимит", "/Гифлимит", ".Гифлимит", ""]
    if anmiation_limit in raises:
        await message.reply("<b>❌ Укажите значение!</b>")
        return
    if int(anmiation_limit) < 0:
        await message.reply("<b>❌ Укажите верное значение!</b>\n От нуля до бесконечности.")
        return
    else:
        chats = message.chat.id
        set_anmiation_limit(chats, anmiation_limit)
        await message.reply(f"<b> ✅ GIF-антиспам успешно установлен на {anmiation_limit}!</b>")


#Установить спам-лимит на гифки
@dp.message_handler(commands=["текстлимит"], commands_prefix="/!.", is_chat_admin=True)
async def text_limit_handler(message: types.Message):
    if message.chat.type == 'private':
        return
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            
    text_limit = message.text.replace("!текстлимит ", "").replace("/текстлимит ", "").replace(".текстлимит ", "").replace("!Текстлимит ", "").replace("/Текстлимит ", "").replace(".Текстлимит ", "")
    raises = ["!текстлимит", "/текстлимит", ".текстлимит", "!Текстлимит", "/Текстлимит", ".Текстлимит", ""]
    if text_limit in raises:
        await message.reply("<b>❌ Укажите значение!</b>")
        return
    if int(text_limit) < 0:
        await message.reply("<b>❌ Укажите верное значение!</b>\n От нуля до бесконечности.")
        return
    else:
        chats = message.chat.id
        set_text_limit(chats, text_limit)
        await message.reply(f"<b> ✅ Текст-антиспам успешно установлен на {text_limit}!</b>")

