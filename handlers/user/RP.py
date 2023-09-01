import html
import re
from random import choice, randint

from aiogram import types

from loader import bot, dp
from settings import no_rp_list
from utils.db.db_utils_members import *
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from utils.db.db_utils_сhats import *
from utils.db.relations.db_utils_moniker import *

from ..f_lib.other import eight_years, morph_word, rp_check
from ..f_lib.pyrogram_f import pyro_get_chat_member


@dp.message_handler(commands=["мануал"], commands_prefix="/!.") #Cама РП команда
async def rp_manual(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    endrp = " рп"
    if endrp in message.text.lower():
        create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
        nick = html.escape(message.from_user.first_name)
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        await message.reply(f"<a href='tg://user?id={message.from_user.id}'>{nick}</a>, вот инструкция для РП команд:\n \
        \n\nФиксированные команды вводятся просто с [/!.] (или без префикса) в начале сообщения. Пример: [.обнять]\
        \nФиксированные команды (их можно узнать по команде <code>.список рп</code>) писать либо в ответ на сообщение, либо поставив @юзернейм после команды, строго в первой строке.\
        \nЕсли после фиксированной команды вы введете какой-либо текст во второй строке, то он окажется в сопроводительной реплике.\
        \nЕсли в фиксированной команде где-либо написать слово <code>рандом</code>, то в случае, если не указана цель, она будет выбрана случайным образом.\
        \n\nВ свободной РП, вы можете поставить знак % и после него ввести эмодзи для РП-команды. Вводить эмодзи нужно в первой строке.\
        \nНаписав фразу во второй строке в свободной форме РП, вы сделаете ее сопроводительной репликой, как и в фиксированных РП.\
        \nВ случае, если вы пишите свободное РП с указанием через @юзернейм, то юзернейм указывать нужно в первой строке, и вводить эмодзи - после него.\
        \n\nЕсли вам ответило, что «пользователь не найден в базе данных бота», то найдите любое сообщение этого пользователя и запросите у бота его профиль. Видимо, он либо новичок, либо успел сменить недавно свой @юзернейм.\
        \n\nПримеры для фиксированных команд:\
        \n— В ответ на сообщение:\
        \n<code>.обнять\
        \nХарош.</code>\
        \n\n—Не отвечая на сообщение, а просто отправить в чат:\
        \n<code>.пригласить на чай @юзернейм\
        \nОн вкусный!</code>\
        \n\nПримеры для сводной формы:\
        \n— В ответ на сообщение:\
        \n<code>.рп обнял %🤗\
        \nХарош.</code>\
        \n\n—Не отвечая на сообщение, а просто отправить в чат:\
        \n<code>.рп пригласил на чай @юзернейм %🤌🫖\
        \nОн вкусный!</code>\
        \n\n——\nНе рекомендуется делать эмодзи, реплику и действие одинаковыми, если используется свободная форма РП. Они все должны быть разными.\
        \nВ свободной форме РП можно устанавливать желаемый падеж у цели (если это возможно). Для этого нужно чтобы команда была с дополнительной буквой, первой из названия падежа.\
        \nПример: <code>.рпв убил</code> — установит винительный падеж. А <code>.рпд убил</code> — дательный. Если не указать цель, то цель будет выбрана случайно.")


@dp.message_handler(commands=["список"], commands_prefix="/!.") #Cама РП команда
async def rp_spis(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    endrp = " рп"
    if endrp in message.text.lower():
        nick = html.escape(message.from_user.first_name)
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        await message.reply(f"<a href='tg://user?id={message.from_user.id}'>{nick}</a>, вот список РП команд:\n \
        \n Вместо точек можно использовать и [/] и [!]\
        \n 1) .<code>Убить</code>\
        \n 2) .<code>Обнять</code>\
        \n 3) .<code>Укусить</code>\
        \n 4) .<code>Куснуть</code>\
        \n 5) .<code>Пнуть</code>\
        \n 6) .<code>Изнасиловать</code>\
        \n 7) .<code>Выебать</code>\
        \n 8) .<code>Трахнуть</code>\
        \n 9) .<code>Погладить</code>\
        \n10) <code>.Секс</code> или <code>делать секс</code> или <code>делать интим</code>\
        \n11) .<code>Потрогать</code>\
        \n12) .<code>Кусь</code>\
        \n13) .<code>Ударить</code>, и .<code>уебать</code>\
        \n14) .<code>Пожать руку</code>, и .<code>пожать шею</code>\
        \n15) .<code>Пригласить</code>, …<code>на чай</code>, …<code>на кофе</code>, …<code>на пиво</code>\
        \n16) .<code>Лизь</code>, и .<code>лизнуть</code>\
        \n17) .<code>Поцеловать</code>\
        \n18) .<code>Засосать</code>\
        \n19) .<code>Расстрелять</code>\
        \n20) .<code>Соболезновать</code> и <code>.собл</code> \
        \n21) .<code>Связать</code>\
        \n22) .<code>Отдаться</code>\
        \n23) .<code>Отсосать</code> или .<code>отлизать</code> или <code>делать орал</code>\
        \n24) .<code>Поприветствовать</code> или .<code>приветствовать</code> или <code>.привет</code>\
        \n25) .<code>Извиниться</code> или <code>.извини</code> или <code>.прости</code>\
        \n26) .<code>Покормить</code>\
        \n27) .<code>Попрощаться</code> или <code>.пока</code>\
        \n28) .<code>Дать пять</code>\
        \n29) .<code>Послать</code>, …<code>нахуй</code>, …<code>в пизду</code>\
        \n30) .<code>Отравить</code>\
        \n31) .<code>Похвалить</code>\
        \n32) .<code>Понюхать</code>\
        \n33) .<code>Сжечь</code>\
        \n34) .<code>Наградить</code>\
        \n35) .<code>Кастрировать</code> или .<code>стерилизовать</code>\
        \n36) .<code>Позвать</code>\
        \n37) .<code>Поздравить</code>\
        \n38) .<code>Наказать</code>\
        \n39) .<code>Облизать</code>\
        \n40) .<code>Унизить</code>\
        \n41) .<code>Вылечить</code>\
        \n42) .<code>Украсть</code>\
        \n\nГде префиксы стоят вне выделения, там можно без них (или с ними), где их нет, там только без них, а где они стоят внутри выделения, там работает только с ними.\
        \nПодробную инструкцию по использованию РП команд можно вызвать при помощи команды <code>.мануал рп</code>.")


#импортируется в games, откуда потом попадает в easters
async def rp_list(message: types.Message):
    
    if message.reply_to_message:
        first_string = message.text.split("\n")[0]
        if len(first_string.split()) > 3:
            return
        elif message.reply_to_message.from_user.id in no_rp_list:
            return
    elif 'рандом' in message.text.lower():
        first_string = message.text.split("\n")[0]
        if len(first_string.split()) > 4:
            return
    
    elif message.entities:
        ent = False
        text_l = message.text

        for entity in message.entities:
            if entity.type in ["text_mention", "mention"]:
                ent = True
                
                text_l = text_l[:entity.offset] + text_l[entity.offset + entity.length:]
                
                break
            
            else:
                continue
        
        if ent == False:
            return
        elif len(text_l.split()) > 3:
            return
    
    else:
        return
    
    wrp1 = "убить"
    wrp2 = "обнять"
    wrp3 = "укусить"
    wrp4 = "куснуть"
    wrp5 = "пнуть"
    wrp6 = "изнасиловать"
    wrp7 = "выебать"
    wrp8 = "трахнуть"
    wrp9 = "погладить"
    wrp10 = ["делать секс", "делать интим"]
    wrp11 = "потрогать"
    wrp12 = "кусь"
    wrp13 = ["ударить", "уебать"]
    wrp14 = "пожать" #пожать руку, и пожать шею"
    wrp15 = "пригласить" #, …на чай, …на кофе, …на пиво
    wrp16 = ["лизь", "лизнуть"]
    wrp17 = "поцеловать"
    wrp18 = "засосать"
    wrp19 = "расстрелять"
    wrp20 = "соболезновать"
    wrp21 = "связать"
    wrp22 = "отдаться"
    wrp23 = ["отсосать", "отлизать", "делать орал"]
    wrp24 = ["поприветствовать", "приветствовать"]
    wrp25 = "извиниться"
    wrp26 = "покормить"
    wrp27 = "попрощаться"
    wrp28 = "дать пять"
    wrp29 = "послать" #…нахуй, …в пизду
    wrp30 = "отравить"
    wrp31 = "похвалить"
    wrp32 = "понюхать"
    wrp33 = "сжечь"
    wrp34 = "наградить"
    wrp35 = ["кастрировать", "стерилизовать"]
    wrp36 = "позвать"
    wrp37 = "поздравить"
    wrp38 = "наказать"
    wrp39 = "облизать"
    wrp40 = "унизить"
    wrp41 = "вылечить"
    wrp42 = "украсть"
    
    done = 0
    if message.text.lower().startswith(wrp1):
        done = await rp1(message)
    if message.text.lower().startswith(wrp2):
        done = await rp2(message)
    if message.text.lower().startswith(wrp3):
        done = await rp3(message)
    if message.text.lower().startswith(wrp4):
        done = await rp4(message)
    if message.text.lower().startswith(wrp5):
        done = await rp5(message)
    if message.text.lower().startswith(wrp6):
        done = await rp6(message)
    if message.text.lower().startswith(wrp7):
        done = await rp7(message)
    if message.text.lower().startswith(wrp8):
        done = await rp8(message)
    if message.text.lower().startswith(wrp9):
        done = await rp9(message)
    for word in wrp10:
        if message.text.lower().startswith(word):
            done = await rp10(message)
            break
    if message.text.lower().startswith(wrp11):
        done = await rp11(message)
    if message.text.lower().startswith(wrp12):
        done = await rp12(message)
    for word in wrp13:
        if message.text.lower().startswith(word):
            done = await rp13(message)
            break
    if message.text.lower().startswith(wrp14):
        done = await rp14(message)
    if message.text.lower().startswith(wrp15):
        done = await rp15(message)
    for word in wrp16:
        if message.text.lower().startswith(word):
            done = await rp16(message)
            break
    if message.text.lower().startswith(wrp17):
        done = await rp17(message)
    if message.text.lower().startswith(wrp18):
        done = await rp18(message)
    if message.text.lower().startswith(wrp19):
        done = await rp19(message)
    if message.text.lower().startswith(wrp20):
        done = await rp20(message)
    if message.text.lower().startswith(wrp21):
        done = await rp21(message)
    if message.text.lower().startswith(wrp22):
        done = await rp22(message)
    for word in wrp23:
        if message.text.lower().startswith(word):
            done = await rp23(message)
            break
    for word in wrp24:
        if message.text.lower().startswith(word):
            done = await rp24(message)
            break
    if message.text.lower().startswith(wrp25):
        done = await rp25(message)
    if message.text.lower().startswith(wrp26):
        done = await rp26(message)
    if message.text.lower().startswith(wrp27):
        done = await rp27(message)
    if message.text.lower().startswith(wrp28):
        done = await rp28(message)
    if message.text.lower().startswith(wrp29):
        done = await rp29(message)
    if message.text.lower().startswith(wrp30):
        done = await rp30(message)
    if message.text.lower().startswith(wrp31):
        done = await rp31(message)
    if message.text.lower().startswith(wrp32):
        done = await rp32(message)
    if message.text.lower().startswith(wrp33):
        done = await rp33(message)
    if message.text.lower().startswith(wrp34):
        done = await rp34(message)
    for word in wrp35:
        if message.text.lower().startswith(word):
            done = await rp35(message)
            break
    if message.text.lower().startswith(wrp36):
        done = await rp36(message)
    if message.text.lower().startswith(wrp37):
        done = await rp37(message)
    if message.text.lower().startswith(wrp38):
        done = await rp38(message)
    if message.text.lower().startswith(wrp39):
        done = await rp39(message)
    if message.text.lower().startswith(wrp40):
        done = await rp40(message)
    if message.text.lower().startswith(wrp41):
        done = await rp41(message)
    if message.text.lower().startswith(wrp42):
        done = await rp42(message)
    
    if done == 0:
        return
    else:
        return 1


def get_replic(text):
    replic = ""
    match = re.search(r'\n(.+)\Z', text)
    if match:
        replic = f"\n💬 С репликой: «{match.group(1)}»"
    return replic


def get_funny(message: types.Message):
    if message.chat.type == 'private':
        return 1
    chats = message.chat.id
    chat = get_chat(chats)
    if check_chat(chats):
        create_chat(chats)
        chat = get_chat(chats)
    funny = chat[4]
    return funny


async def do_8_y(user, user2, text, msg):
    if len(text.split()) > 2:
        return
    text = text.lower()
    
    sex_word = ["выеб", "выёб", "выeб", "секс", "cекс", "сeкс", "секc", "ceкс", "ceкc", "cекc", "сeкc", "отсос", "oтсос", "отcос", "отсоc", "oтсоc", "отсoc", "отлиз", "oтлиз"]
    for word in sex_word:
        if word in text:
            eight_years(msg.chat.id, user, user2, msg, True)
            return
        else:
            continue

    sex_word_2 = ["изнасил", "изнaсил", "изнаcил", "изнacил"]
    for word in sex_word_2:
        if word in text:
            eight_years(msg.chat.id, user, user2, msg, False)
            return
        else:
            continue
    
    sex_word_3 = ["ебал", "eбал", "ебaл", "eбaл", "трах", "трaх", "траx", "трax", "oтьёба", "oтьeба", "oтъёба", "oтъeба", "oтьеба", "oтъеба", "oтьёбa", "oтьeбa", "oтъёбa", "oтъeбa", "oтьебa", "oтъебa", "отьёба", "отьeба", "отъёба", "отъeба", "отьеба", "отъеба", "отьёбa", "отьeбa", "отъёбa", "отъeбa", "отьебa", "отъебa"]
    for word in sex_word_2:
        for word2 in text.split():
            if word2.startswith(word):
                eight_years(msg.chat.id, user, user2, msg, True)
                return
    
    sex_word_4 = ["oтьёб", "oтьeб", "oтъёб", "oтъeб", "oтьеб", "oтъеб", "отьёб", "отьeб", "отъёб", "отъeб", "отьеб", "отъеб"]
    for word in sex_word_2:
        for word2 in text.split():
            if word2 == word:
                eight_years(msg.chat.id, user, user2, msg, True)
                return

@dp.message_handler(commands=["рп", "rp", "рпи", "rpи", "рпр", "rpр", "рпд", "rpд", "рпв", "rpв", "рпт", "rpт", "рпп", "rpп"], commands_prefix="/!.")
async def rp_command(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    funny = get_funny(message)
    
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    

    
    emodz = ""
    emodz1 = ""
    
    match = re.search(r'%(.+)\Z', message.text)
    if match:
        emodz1 = match.group(1)
        if emodz1 != "":
            emodz = f"{emodz1} | "
    
    match = re.search(r'%(.+)\n', message.text)
    if match:
        emodz1 = match.group(1)
        if emodz1 != "":
            emodz = f"{emodz1} | "
    
    replic = get_replic(message.text)
    
    if message.reply_to_message:
        if message.reply_to_message.from_user.id in no_rp_list:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except:
                pass
            return
        
        user2 = create_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name)
        
        user = create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
        
        if check_monik(user2[0], user2[8]) == True:
            rep_monic = get_monik(user2[0], user2[8])[2]
            
            if user2[5] < rep_monic:
                if user2[8] != "":
                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
            
            
            elif user[5] > user2[5]:
                if user2[8] != "":
                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
        
        if user2[0] in no_rp_list:
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except:
                pass
            return
        
        nick2 = user2[2]
        command = message.text.split(" ")[0]
        if command.lower().endswith("рпи") or command.lower().endswith("rpи"):
            nick2 = morph_word(user2[0], user2[2], user2[4])[0]
        elif command.lower().endswith("рпр") or command.lower().endswith("rpр"):
            nick2 = morph_word(user2[0], user2[2], user2[4])[1]
        elif command.lower().endswith("рпд") or command.lower().endswith("rpд"):
            nick2 = morph_word(user2[0], user2[2], user2[4])[2]
        elif command.lower().endswith("рпв") or command.lower().endswith("rpв"):
            nick2 = morph_word(user2[0], user2[2], user2[4])[3]
        elif command.lower().endswith("рпт") or command.lower().endswith("rpт"):
            nick2 = morph_word(user2[0], user2[2], user2[4])[4]
        elif command.lower().endswith("рпп") or command.lower().endswith("rpп"):
            nick2 = morph_word(user2[0], user2[2], user2[4])[5]
        else:
            nick2 = user2[2]
            
        if "%" in message.text:
            action = message.text.replace(f"{command}", "").split("%")[0]
        else:
            action = message.text.replace(f"{command}", "").split("\n")[0]
        if action == "":
            await message.reply("<b>❌ Укажи действие</b>!\n Пример: !рп Убил")
            return
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        
        rp_text = f"{html.escape(emodz)}<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}"
        
        msg = await message.answer(rp_text.replace("  ", " "), parse_mode="html")
        await do_8_y(user, user2, action, msg)
        return
    
    else:
        match = re.search(r'@(\w+)', message.text)
        if match:
            name = match.group(1)
            
            if check_username(name):
                
                if message.chat.type == 'private':
                    await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    return

                try:
                    member = await pyro_get_chat_member(message.chat.id, name)
                    
                    if check_user(member.user.id):
                        create_user_main(member.user.id, name, member.user.first_name)
                    else:
                        set_username(member.user.id, name)
                    
                    user2 = get_user(member.user.id)
                
                except:
                    await message.reply("<b>❌ Пользователь не найден в базе данных бота!</b>")
                    return
            
            else:
                user2 = get_username(name)
            
            user = create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
        
            if check_monik(user2[0], user2[8]) == True:
                rep_monic = get_monik(user2[0], user2[8])[2]
                
                if user2[5] < rep_monic:
                    if user2[8] != "":
                        user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                
                
                elif user[5] > user2[5]:
                    if user2[8] != "":
                        user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                    
            
            if user2[0] in no_rp_list:
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                except:
                    pass
                return
            nick2 = user2[1]
            command = message.text.split(" ")[0]
            if command.lower().endswith("рпи") or command.lower().endswith("rpи"):
                nick2 = morph_word(user2[0], user2[2], user2[4])[0]
            elif command.lower().endswith("рпр") or command.lower().endswith("rpр"):
                nick2 = morph_word(user2[0], user2[2], user2[4])[1]
            elif command.lower().endswith("рпд") or command.lower().endswith("rpд"):
                nick2 = morph_word(user2[0], user2[2], user2[4])[2]
            elif command.lower().endswith("рпв") or command.lower().endswith("rpв"):
                nick2 = morph_word(user2[0], user2[2], user2[4])[3]
            elif command.lower().endswith("рпт") or command.lower().endswith("rpт"):
                nick2 = morph_word(user2[0], user2[2], user2[4])[4]
            elif command.lower().endswith("рпп") or command.lower().endswith("rpп"):
                nick2 = morph_word(user2[0], user2[2], user2[4])[5]
            else:
                nick2 = user2[2]
            
            if "@" in emodz1:
                action = message.text.replace(f"{command}", "").split("%")[0]
                emodz1 = emodz1.split("@")[0]
                if emodz1 != "":
                    emodz = f"{emodz1}|"
                if "@" in emodz:
                    emodz = ""
            else:
                action = message.text.replace(f"{command}", "").split("@")[0]
            if action == "":
                await message.reply("<b>❌ Укажи действие!</b>\nПример: !рп Обнял")
            
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except:
                pass
            
            rp_text = f"{html.escape(emodz)}<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}"
            msg = await message.answer(rp_text.replace("  ", " "), parse_mode="html")
            await do_8_y(user, user2, action, msg)
            return
        else:
            user = create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
            for entity in message.entities:
                if entity.type == "text_mention":

                    user2_id = entity.user.id

                    user2 = create_user(user2_id, str(user2_id), entity.user.first_name)
                    
                    if check_monik(user2[0], user2[8]) == True:
                        rep_monic = get_monik(user2[0], user2[8])[2]
                        if user2[5] < rep_monic:
                            if user2[8] != "":
                                user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                        elif user[5] > user2[5]:
                            if user2[8] != "":
                                user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
    
                    if user2[0] in no_rp_list:
                        try:
                            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                        except:
                            pass
                        return


                    name = message.text[entity.offset:entity.offset + entity.length]
                    nick2 = user2[2]
                    command = message.text.split(" ")[0]
                    if command.lower().endswith("рпи") or command.lower().endswith("rpи"):
                        nick2 = morph_word(user2[0], user2[2], user2[4])[0]
                    elif command.lower().endswith("рпр") or command.lower().endswith("rpр"):
                        nick2 = morph_word(user2[0], user2[2], user2[4])[1]
                    elif command.lower().endswith("рпд") or command.lower().endswith("rpд"):
                        nick2 = morph_word(user2[0], user2[2], user2[4])[2]
                    elif command.lower().endswith("рпв") or command.lower().endswith("rpв"):
                        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
                    elif command.lower().endswith("рпт") or command.lower().endswith("rpт"):
                        nick2 = morph_word(user2[0], user2[2], user2[4])[4]
                    elif command.lower().endswith("рпп") or command.lower().endswith("rpп"):
                        nick2 = morph_word(user2[0], user2[2], user2[4])[5]
                    else:
                        nick2 = user2[2]
                    
                    if name in emodz1:
                        action = message.text.replace(f"{command}", "").split("%")[0]
                        emodz1 = emodz1.split(name)[0]
                        if emodz1 != "":
                            emodz = f"{emodz1}|"
                        if entity.user.first_name in emodz:
                            emodz = ""
                    else:
                        action = message.text.replace(f"{command}", "").split(name)[0]
    
                    
                    if action == "":
                        await message.reply("<b>❌ Укажи действие!</b>\nПример: !рп Обнял")
                    
                    try:
                        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    except:
                        pass
                    
                    rp_text = f"{html.escape(emodz)}<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}"
                    msg = await message.answer(rp_text.replace("  ", " "), parse_mode="html")
                    await do_8_y(user, user2, action, msg)
                    return
                    

                else:
                    continue

            
            if message.chat.type != 'private':
                members = get_members(message.chat.id)
                for element in members:
                    member = choice(members)
                    user2 = get_user(member[1])
                    if user2[0] in no_rp_list:
                        continue
                    else:
                        if check_monik(user2[0], user2[8]) == True:
                            rep_monic = get_monik(user2[0], user2[8])[2]
                            if user2[5] < rep_monic:
                                if user2[8] != "":
                                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                            elif user[5] > user2[5]:
                                if user2[8] != "":
                                    user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]

                        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                        break
                
                if user2 == None:
                    await message.reply("<b>❌ Укажи действие (или цель)</b>!\n Пример: !рп Убил (в ответ на сообщение)\n Пример: !рп убил @[username] (в воздух)")
                    return
                

               
                if check_monik(user2[0], user2[8]) == True:
                    rep_monic = get_monik(user2[0], user2[8])[2]
                    
                    if user2[5] < rep_monic:
                        if user2[8] != "":
                            user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                    
                    
                    elif user[5] > user2[5]:
                        if user2[8] != "":
                            user2 = [user2[0], user2[1], user2[8], user2[3], user2[4], user2[5], user2[6], user2[7], user2[8]]
                
                if user2[0] in no_rp_list:
                    await message.reply("<b>❌ Укажи действие (или цель)</b>!\n Пример: !рп Убил (в ответ на сообщение)\n Пример: !рп убил @[username] (в воздух)")
                    return
                
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                except:
                    pass
                
                nick2 = user2[2]
                command = message.text.split(" ")[0]
                if command.lower().endswith("рпи") or command.lower().endswith("rpи"):
                    nick2 = morph_word(user2[0], user2[2], user2[4])[0]
                elif command.lower().endswith("рпр") or command.lower().endswith("rpр"):
                    nick2 = morph_word(user2[0], user2[2], user2[4])[1]
                elif command.lower().endswith("рпд") or command.lower().endswith("rpд"):
                    nick2 = morph_word(user2[0], user2[2], user2[4])[2]
                elif command.lower().endswith("рпв") or command.lower().endswith("rpв"):
                    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
                elif command.lower().endswith("рпт") or command.lower().endswith("rpт"):
                    nick2 = morph_word(user2[0], user2[2], user2[4])[4]
                elif command.lower().endswith("рпп") or command.lower().endswith("rpп"):
                    nick2 = morph_word(user2[0], user2[2], user2[4])[5]
                else:
                    nick2 = user2[2]
                    
                if "%" in message.text:
                    action = message.text.replace(f"{command}", "").split("%")[0]
                else:
                    action = message.text.replace(f"{command}", "").split("\n")[0]
                if action == "":
                    await message.reply("<b>❌ Укажи действие</b>!\n Пример: !рп Убил")
                    return
                
                
                rp_text = f"{html.escape(emodz)}<a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}"
                
                msg = await message.answer(rp_text.replace("  ", " "), parse_mode="html")
                await do_8_y(user, user2, action, msg)

            await message.reply("<b>❌ Укажи действие (или цель)</b>!\n Пример: !рп Убил (в ответ на сообщение)\n Пример: !рп убил @[username] (в воздух)")
            return



#ОБЛИЗАТЬ
@dp.message_handler(commands=["украсть"], commands_prefix="/!.") #Cама РП команда
async def rp42(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    result = randint(0, 100)
    
    if result >= 80:
        rpword = ["были арестованы", "был арестован", "была арестована", "было запечатано", "затискивается"]
        rpemodz = ["👤⛓🚓", "👨‍🦲⛓🚓", "👩‍🦲⛓🚓", "👾🪬🔯", "🐱🤗"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    else:
        rpword = ["украли", "украл", "украла", "забрало себе", "похищает"]
        rpemodz = ["🥷🪢😵", "🥷🪢😵", "🥷🪢😵", "👾🪸😵‍💫", "😸🪢😵‍💫"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]

    replic = get_replic(message.text)
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ОБЛИЗАТЬ
@dp.message_handler(commands=["вылечить"], commands_prefix="/!.") #Cама РП команда
async def rp41(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return

    rpword = ["вылечили", "вылечил", "вылечила", "исцелило", "восстанавливает"]
    rpemodz = ["👤💊🙂", "👨‍⚕️💊🙂", "👩‍⚕️💉🙂", "👾💫😮", "😸👅😊"]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    replic = get_replic(message.text)
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#УНИЗИТЬ
@dp.message_handler(commands=["унизить"], commands_prefix="/!.") #Cама РП команда
async def rp40(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    replic = get_replic(message.text)

    user2 = await rp_check(message)
    
    if user2 == None:
        return 0
    if user2[0] in no_rp_list:
        return
    
    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    
    result = randint(0, 100)
    
    if result >= 80:
        rpword = ["были унижены", "был унижен", "была унижена", "было унижено", "силой выкупывается"]
        rpemodz = ["😎👇🦵👤", "😎👇🦵🙇‍♂️", "😎👇🚽🙇‍♀️", "👾🔯→🧞", "🫤😾🧼"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    else:
        rpword = ["унизили", "унизил", "унизила", "унизило", "унижает"]
        rpemodz = ["👤👇🦵", "👨👇🦵", "👩👇🚽" , "👾👁🤡", "😾👀💩"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ОБЛИЗАТЬ
@dp.message_handler(commands=["облизать"], commands_prefix="/!.") #Cама РП команда
async def rp39(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["облизали", "облизал", "облизала", "облизало", "облизывает"]
    rpemodz = ["👤👅😅", "👨👅😅", "👩👅😅", "👾🔞👅😵", "😸👅😂"]

    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    eight_years(message.chat.id, user, user2, msg_info, False)

#НАКАЗАТЬ
@dp.message_handler(commands=["наказать"], commands_prefix="/!.") #Cама РП команда
async def rp38(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0
    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return    
    
    result = randint(0,100)
    if result < 80:
        rpword = ["наказали", "наказал", "наказала", "наказало", "наказывает-мяу"]
        rpemodz = ["👤🤜😖", "👨🤜😖", "👩🔞🌵🏥" , "👾💥⚱️" , "😹💦👟😭"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    else:
        rpword = ["получили пизды от", "получил пизды от", "получила пизды от", "получило пизды от", "получает пизды от"]
        rpemodz = ["👤🤛🤬", "👨🤛🤬", "👩🤛🤬", "👾🤛🤬", "🙀🤛🤬"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    replic = get_replic(message.text)



    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ПОЗДРАВИТЬ
@dp.message_handler(commands=["поздравить"], commands_prefix="/!.") #Cама РП команда
async def rp37(message: types.Message):
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    rpword = ["поздравили", "поздравил", "поздравила", "поздравило", "поздравляет"]
    rpemodz = ["👤🎉", "👨🎊", "👩👏", "👾🎆", "😸🎁"]

    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ПОЗВАТЬ
@dp.message_handler(commands=["позвать"], commands_prefix="/!.") #Cама РП команда
async def rp36(message: types.Message):
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return

    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    replic = get_replic(message.text)
    rpword = ["позвали", "позвал", "позвала", "призвало", "зовёт"]
    rpemodz = ["👤🔔😶", "👨🔔😶", "👩🔔😶", "👾🔊😱", "😸🤌😱"]
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#КАСТРИРОВАТЬ
@dp.message_handler(commands=["кастрировать", "стерилизовать"], commands_prefix="/!.") #Cама РП команда
async def rp35(message: types.Message):
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    rpword = ["стерилизовали", "стерилизовал", "стерилизовала", "прервало род", "стерилизует"]
    rpemodz = ["👤💉", "👨💉", "👩💉", "👾🦠", "😼💉"]

    replic = get_replic(message.text)

    
    if user[4] == 3:
        nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    else:
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    if user2[4] == 0:
        await message.answer(f"{html.escape(rpemodz)}😭 | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
        return
    if user2[4] == 1:
        rpword = ["кастрировали", "кастрировал", "кастрировала", "прервало род", "кастрирует"]
        rpemodz = ["👤✂️╰⋃╯", "👨✂️╰⋃╯", "👩✂️╰⋃╯", "👾⚡️╰⋃╯", "😼✂️╰⋃╯"]
        
        action = rpword[user[4]]
        rpemodz = rpemodz[user[4]]
        await message.answer(f"{html.escape(rpemodz)}😭 | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
        return
    if user2[4] == 2:    
        await message.answer(f"{html.escape(rpemodz)}😭 | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
        return
    if user2[4] == 3:
        await message.answer(f"{html.escape(rpemodz)}😭 | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
        return
    if user2[4] == 4:
        await message.answer(f"{html.escape(rpemodz)}🙀 | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
        return
    else:
        await message.answer("Что-то пошло не так.😭")
        return

#НАГРАДИТЬ
@dp.message_handler(commands=["наградить"], commands_prefix="/!.") #Cама РП команда
async def rp34(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["наградили", "наградил", "наградила", "наградило", "награждает"]
    rpemodz = ["👤🫴🏆", "👨🫴🏆", "👩🫴🏆", "👾🫴🪐", "😸🫴🥇"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if user[0] != user2[0]:
        add_rep(user2[0])

#СЖЕЧЬ
@dp.message_handler(commands=["сжечь"], commands_prefix="/!.") #Cама РП команда
async def rp33(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    replic = get_replic(message.text)
    result = randint(0,100)
    if result < 75:
        rpword = ["сожгли", "сжёг", "сожгла", "сожгло", "сжигает"]
        rpemodz = ["👤🔥💀", "👨🔥💀", "👩🔥💀", "👾:🫥→☀️", "😼🔥💀"]
        mistake = 0
    else:
        rpword = ["сгорели в пламени пожара!", "сгорел в пламени пожара!", "сгорела в пламени пожара!", "исчезло в пламени звезды!", "сгорает в пламени пожара!"]
        rpemodz = ["👤❌🔥💀", "👨❌🔥💀", "👩❌🔥💀", "👾❌☀️", "🙀❌🔥💀"]
        mistake = 1

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    if mistake == 1:
        await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)}{html.escape(replic)}", parse_mode="html")
        return
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    return

#ПОНЮХАТЬ
@dp.message_handler(commands=["понюхать"], commands_prefix="/!.") #Cама РП команда
async def rp32(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["понюхали", "понюхал", "понюхала", "изучило", "обнюхивает"]
    rpemodz = ["👤👃😑", "👨👃😑", "👩👃😑", "👾👁🩻", "😾🔎😑"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ПОХВАЛИТЬ
@dp.message_handler(commands=["похвалить"], commands_prefix="/!.") #Cама РП команда
async def rp31(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["похвалили", "похвалил", "похвалила", "похвалило", "хвалит"]
    rpemodz = ["👤👍😀", "👨👍😀", "👩👍😀", "👾👍🥶", "😼👍😀"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if user[0] != user2[0]:
        add_rep(user2[0])

#ОТРАВИТЬ
@dp.message_handler(commands=["отравить"], commands_prefix="/!.") #Cама РП команда
async def rp30(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    replic = get_replic(message.text)
    result = randint(0, 100)    
    if result < 80:
        mistake = 0
    else:
        mistake = 1
    
    if mistake == 0:
        rpword = ["отравили", "отравил", "отравила", "заразило мемагентом", "мочит"]
        rpemodz = ["👤🧪🥵", "👨🧪🥵", "👩🧪🥵", "👾🪬☠️", "😼💦🤢"]
        
        action = rpword[user[4]]
        rpemodz = rpemodz[user[4]]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
        await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    else:
        rpword = ["отравились", "отравился", "отравилась", "заразилось мемагентом", "попадает под дождь"]
        rpemodz = ["👤🧪🥵", "👨🧪🥵", "👩🧪🥵", "👾🪬☠️", "🌧😿"]
        
        action = rpword[user[4]]
        rpemodz = rpemodz[user[4]]
        await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)}{html.escape(replic)}", parse_mode="html")


#ПОСЛАТЬ НАХУЙ
@dp.message_handler(commands=["послать"], commands_prefix="/!.") #Cама РП команда, или ее начало
async def rp29(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0
    if user2[0] in no_rp_list:
        return
    
    user = get_user(message.from_user.id)
    
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    replic = get_replic(message.text)
    rpword = ["послали", "послал", "послала", "послало", "посылает"]
    rpemodz = ["👤🖕", "👨🖕", "👩🖕", "👾🖕", "😼🖕"]
    
    
    endrp = " нахуй"  #конец рп команды
    if endrp in message.text.lower():
        rpword = ["послали нахуй", "послал нахуй", "послала нахуй", "отправило в ебеня", "указует направление"]
        rpemodz = ["👤👉🔞", "👨👉🔞", "👩👉🔞", "👾:😵‍💫→🌌️", "😼╰⋃╯→"]
        if user[4] == 4:
            nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    
    endrp = " в пизду"  #конец рп команды
    if endrp in message.text.lower():
        rpword = ["послали в пизду", "послал в пизду", "послала в пизду", "реинкарнировало", "указует направление"]
        rpemodz = ["👤👉🔞", "👨👉🔞", "👩👉🔞", "👾:😵‍💫→🤱", "😼👉🔞"]
        if user[4] == 4:
            nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    


    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ДАТЬ ПЯТЬ
@dp.message_handler(commands=["дать"], commands_prefix="/!.") #Cама РП команда
async def rp28(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    replic = get_replic(message.text)
    endrp = " пять"
    if endrp in message.text.lower():
        rpword = ["дали пять", "дал пять", "дала пять", "коснулось руки", "толкает лапкой"]
        rpemodz = ["👤🖐😀", "👨🖐😀", "👩🖐😀", "👾🖐😨", "🐱🫱😀"]
    else:
        return 0

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    if user[4] == 3:
        nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    if user[4] == 4:
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ПОКА
@dp.message_handler(commands=["пока", "попрощаться"], commands_prefix="/!.") #Cама РП команда
async def rp27(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["попрощались с", "попрощался с", "попрощалась с", "попрощалось с", "прощается с"]
    rpemodz = ["👤👋😔", "👨👋😔", "👩👋😔", "👾👋😀", "😿👋😔"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ПОКОРМИТЬ
@dp.message_handler(commands=["покормить"], commands_prefix="/!.") #Cама РП команда
async def rp26(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["покормили", "покормил", "покормила", "подпитало", "кормит"]
    rpemodz = ["👤🫴🍖", "👨🫴🍫", "👩🫴🍬", "👾🫴🦑", "😸🫴🐟"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ИЗВИНИ
@dp.message_handler(commands=["извини", "прости", "извиниться"], commands_prefix="/!.") #Cама РП команда
async def rp25(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["извинились перед", "извинился перед", "извинилась перед", "извинилось перед", "извиняется перед"]
    rpemodz = ["👤🙏🤨", "👨🙏🙂", "👩🙏🙂", "👾🙏😑", "🐱🙏🙂"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ПРИВЕТ
@dp.message_handler(commands=["привет", "приветствовать", "поприветствовать"], commands_prefix="/!.") #Cама РП команда
async def rp24(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["поприветствовали", "поприветствовал", "поприветствовала", "поприветствовало", "машет лапкой"]
    rpemodz = ["👤👋🤨", "👨👋🙂", "👩👋🙂", "👾👋😲", "😺👋🙂"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    if user[4] == 4:
        nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ОТСОСАТЬ
@dp.message_handler(commands=["отсосать", "отлизать"], commands_prefix="/!.") #Cама РП команда
async def rp23(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    
    if user2[4] == 2:
        rpword = ["отлизали у", "отлизал у", "отлизала у", "даровало экстаз", "вылизывает всё у"]
        rpemodz = ["👤👅🧖‍♀️", "👨👅🧖‍♀️", "👩👅👩‍❤️‍👩", "👾🔞💃", "😽🔞😐"]
        if user[4] == 3:
            nick2 = morph_word(user2[0], user2[2], user2[4])[2]
        else:
            nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    
    elif user2[4] == 1:
        rpword = ["отсосали у", "отсосал у", "отсосала у", "отсосало у", "вылизывает всё у"]
        rpemodz = ["👤👅🤨", "👨👅😳", "👩👅😳", "👾🔞😧", "😽🔞😐"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    
    else:
        if "отсосать" in message.text.lower():
            rpword = ["отсосали у", "отсосал у", "отсосала у", "отсосало у", "вылизывает всё у"]
            rpemodz = ["👤👅🤨", "👨👅😳", "👩👅😳", "👾🔞😧", "😽🔞😐"]
            replic = get_replic(message.text)
            nick2 = morph_word(user2[0], user2[2], user2[4])[1]
        if "отлизать" in message.text.lower():
            rpword = ["отлизали у", "отлизал у", "отлизала у", "даровало экстаз", "вылизывает всё у"]
            rpemodz = ["👤👅🧖‍♀️", "👨👅🧖‍♀️", "👩👅👩‍❤️‍👩", "👾🔞💃", "😽🔞😐"]
            if user[4] == 3:
                nick2 = morph_word(user2[0], user2[2], user2[4])[2]
            else:
                nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    
    
    replic = get_replic(message.text)
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]

    
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    
    eight_years(message.chat.id, user, user2, msg_info, True)

#ОТДАТЬСЯ
@dp.message_handler(commands=["отдаться"], commands_prefix="/!.") #Cама РП команда
async def rp22(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["отдались", "отдался", "отдалась", "отдалось", "отдается в руки"]
    rpemodz = ["👤🌶🤨", "👨❤️‍🔥🙃", "👩🍓🙃", "👾🔞😨", "😼🎁🙃"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    
    if user[4] == 4:
        nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if user[4] != 4:
        eight_years(message.chat.id, user, user2, msg_info, True)

#СВЯЗАТЬ
@dp.message_handler(commands=["связать"], commands_prefix="/!.") #Cама РП команда
async def rp21(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return

    replic = get_replic(message.text)

    
    result = randint(0, 100)
    if result >= 80:

        rpword = ["попали в рабство к", "попал в рабство к", "попала в рабство к", "попало в рабство к", "становится питомцем"]
        rpemodz = ["👤⛓⛏", "👨⛓⛏", "👩⛓🔞", "👾→🧞", "🐱🤗"]
        
        if user[4] == 4:
            nick2 = morph_word(user2[0], user2[2], user2[4])[1]
        else:
            nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    else:

        rpword = ["связали", "связал", "связала", "захватило тентаклями", "связывает"]
        rpemodz = ["👤🪢🤐", "👨🪢🤐", "👩🪢🤐", "👾🪸😵‍💫", "😼🪢🤐"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")


#СОБОЛЕЗНОВАТЬ
@dp.message_handler(commands=["соболезновать", "собл"], commands_prefix="/!.") #Cама РП команда
async def rp20(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["соболезнует", "соболезнует", "соболезнует", "соболезнует", "соболезнует"]
    rpemodz = ["👤🫳😭", "👨🫳😭", "👩🫳😭", "👾🫳😭", "😿🫳😭"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#РАССТРЕЛЯТЬ
@dp.message_handler(commands=["расстрелять"], commands_prefix="/!.") #Cама РП команда
async def rp19(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    replic = get_replic(message.text)

    result = randint(0, 100)
    if result >= 80:
        rpword = ["были расстреляны", "был расстрелян", "была расстреляна", "было запечатано", "расстреливается"]
        rpemodz = ["👤🔫😡", "👨🔫😡", "👩🔫😡", "👾🔯😎", "😾🔫😡"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    else:
        rpword = ["расстреляли", "расстрелял", "расстреляла", "помножило на ноль", "расстреливает"]
        rpemodz = ["💀🔫👤", "💀🔫👨", "💀🔫👩", "👾💣☠️", "💀🔫😾"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]    
    
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ЗАСОСАТЬ
@dp.message_handler(commands=["засосать"], commands_prefix="/!.") #Cама РП команда
async def rp18(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    if user2[0] in no_rp_list:
        return
    
    rpword = ["засосали", "засосал", "засосала", "отвакуумировало", "засасывает"]
    rpemodz = ["😘🔞", "👨👄🔞", "👩💋🔞", "👾🌪🌌", "😸🌪📦"]
    replic = get_replic(message.text)


    user = get_user(message.from_user.id)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    eight_years(message.chat.id, user, user2, msg_info, True)

#ПОЦЕЛОВАТЬ
@dp.message_handler(commands=["поцеловать"], commands_prefix="/!.") #Cама РП команда
async def rp17(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["поцеловали", "поцеловал", "поцеловала", "поцеловало", "целует"]
    rpemodz = ["😙", "👨👄", "👩💋", "👾👄😨", "🛸😽"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ЛИЗЬ
@dp.message_handler(commands=["лизь", "лизнуть"], commands_prefix="/!.") #Cама РП команда
async def rp16(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return

    wordrp = "лизнуть"
    if wordrp in message.text.lower():
        ms = False
        rpword = ["лизнули", "лизнул", "лизнула", "лизнуло", "лижет"]
        rpemodz = ["👤👅", "👨👅", "👩👅", "👾🔞👅", "😻👅"]
    else:
        ms = True
        rpword = ["лизь", "лизь", "лизь", "лизЪ", "лизь-мяу"]
        rpemodz = ["👤👅", "👨👅", "👩👅", "👾🔞👅", "😻👅"]
    
    replic = get_replic(message.text)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if ms == True:
        eight_years(message.chat.id, user, user2, msg_info, False)


#ПРИГЛАСИТЬ НА ЧАЙ
@dp.message_handler(commands=["пригласить"], commands_prefix="/!.") #Cама РП команда
async def rp15(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    ms = True
    replic = get_replic(message.text)
    rpword = ["пригласили к себе", "пригласил к себе", "пригласила к себе", "пригласило к себе", "приглашает к себе"]
    rpemodz = ["👤👋🏠", "🙋👋🏠", "🙋👋🏠", "👾👋🌌", "😸👋📦"]
    endrp = " на чай"
    if endrp in message.text.lower():
        ms = False
        rpword = ["пригласили на чай", "пригласил на чай", "пригласила на чай", "пригласило на чай", "приглашает на чай"]
        rpemodz = ["👤👋☕️", "🙋👋☕️", "🙋‍♀️👋☕️", "👾👋🍵", "😸👋🍵"]
    endrp = " на кофе"
    if endrp in message.text.lower():
        ms = False
        rpword = ["пригласили на кофе", "пригласил на кофе", "пригласила на кофе", "пригласило на кофе", "приглашает на кофе"]
        rpemodz = ["👤👋☕️", "🙋👋☕️", "🙋‍♀️👋☕️", "👾👋☕️", "😸👋☕️"]
    endrp = " на пиво"
    if endrp in message.text.lower():
        ms = True
        rpword = ["пригласили на пиво", "пригласил на пиво", "пригласила на пиво", "пригласило на пиво", "приглашает на пиво"]
        rpemodz = ["👤👋🍺", "🙋👋🍺", "🙋‍♀️👋🍺", "👾👋🍻", "😸👋🍻"]

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if ms == True:
        eight_years(message.chat.id, user, user2, msg_info, True)

#ПОЖАТЬ РУКУ
@dp.message_handler(commands=["пожать"], commands_prefix="/!.") #Cама РП команда
async def rp14(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return


    if " руку" in message.text.lower():
        user2 = await rp_check(message)
        if user2 == None:
            return 0
        if user2[0] in no_rp_list:
            return
        user = get_user(message.from_user.id)
        
        rpword = ["пожали руку", "пожал руку", "пожала руку", "пожало руку", "стучит по руке"]
        rpemodz = ["👤🤝🙂", "👨🤝🙂", "👩🤝🙂", "👾🤝😦", "😸🐾🙂"]
        
        if user[4] == 4:
            nick2 = morph_word(user2[0], user2[2], user2[4])[1]
        else:
            nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    
    elif " шею" in message.text.lower():
        user2 = await rp_check(message)
        if user2 == None:
            return 0
        if user2[0] in no_rp_list:
            return
        user = get_user(message.from_user.id)
        
        rpword = ["пожали шею", "задушил", "задушила", "задушило", "душит"]
        rpemodz = ["👤✊😵‍💫", "👨✊😵‍💫", "👩✊😵‍💫", "👾🪬😵", "😸✊😵‍💫"]
        
        if user[4] == 0:
            nick2 = morph_word(user2[0], user2[2], user2[4])[2]
        else:
            nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    else:
        return 0

    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#УДАРИТЬ
@dp.message_handler(commands=["ударить", "уебать"], commands_prefix="/!.") #Cама РП команда
async def rp13(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    if user2[0] in no_rp_list:
        return
    user = get_user(message.from_user.id)
    
    wordrp = "ударить"
    
    if wordrp in message.text.lower():
        result = randint(0, 100)
        if result >= 80:
            rpword = ["ударили мимо", "ударил мимо", "ударила мимо", "отправило в космос", "бьёт мимо"]
            rpemodz = ["👤👊☁️", "👨👊☁️", "👩👊☁️", "👾🌀🌌", "😼👊☁️"]
            if user[4] == 3:
                nick2 = morph_word(user2[0], user2[2], user2[4])[3]
            else:
                nick2 = morph_word(user2[0], user2[2], user2[4])[1]
        
        else:
            rpword = ["ударили", "ударил", "ударила", "отправило в космос", "бьёт"]
            rpemodz = ["👤👊😵", "👨👊😵", "👩👊😵", "👾🌀🌌", "😼👊😵‍📦"]
            nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    else:
        
        wordrp = "уебать"
        if wordrp in message.text.lower():
    
            result = randint(0, 100)
            if result >= 80:
                rpword = ["уебали мимо", "уебал мимо", "уебала мимо", "отправило в небытиё", "въёбывает мимо"]
                rpemodz = ["👤👊☁️", "👨👊☁️", "👩👊☁️", "👾🌀「　」", "😼👊☁️"]
                if user[4] == 3:
                    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
                else:
                    nick2 = morph_word(user2[0], user2[2], user2[4])[1]
            else:
                rpword = ["уебали", "уебал", "уебала", "отправило в небытиё", "въёбывает"]
                rpemodz = ["👤👊😵‍💫", "👨👊😵‍💫", "👩👊😵‍💫", "👾🌀「　」", "😼👊😵‍💫"]
                if user[4] == 4:
                    nick2 = morph_word(user2[0], user2[2], user2[4])[2]
                else:
                    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    
    replic = get_replic(message.text)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#КУСЬ
@dp.message_handler(commands=["кусь"], commands_prefix="/!.") #Cама РП команда
async def rp12(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["сделали кусь", "сделал кусь", "подарила кусь", "пронзило", "кусь целиком"]
    rpemodz = ["👽🦷🙃", "🧛‍♂️🫂🙃", "🧛‍♀️🫦🙃", "👾⚠️☠️", "😸🩸🙃"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    if user[4] == 3 or user[4] == 4:
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    else:
        nick2 = morph_word(user2[0], user2[2], user2[4])[2]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ПОТРОГАТЬ
@dp.message_handler(commands=["потрогать"], commands_prefix="/!.") #Cама РП команда
async def rp11(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["потрогали", "потрогал", "потрогала", "потрогало", "трогает-мяу"]
    rpemodz = ["👤👉😕", "👨👉😕", "👩👉😕", "👾🪬😑", "😸👉😊"]
    replic = get_replic(message.text)

    if user2[4] == 1:
        rpemodz = ["👤🫴🥚🥚", "👨🫴🥚🥚", "👩🫴🥚🥚", "👾🫴🥚🥚", "😸🫴🥚🥚"]
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#СЕКС
@dp.message_handler(commands=["секс"], commands_prefix="/!.") #Cама РП команда
async def rp10(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["делали секс с", "делал секс с", "делала секс с", "делало [данные удалены] с", "делает [мяу] с"]
    rpemodz = ["👤🍓😊", "👨🍓😊", "👩🍓😊", "👾☣️😵‍", "🐈🍋😲"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    
    eight_years(message.chat.id, user, user2, msg_info, True)

#ПОГЛАДИТЬ
@dp.message_handler(commands=["погладить"], commands_prefix="/!.") #Cама РП команда
async def rp9(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["погладили", "погладил", "погладила", "погладило", "поглаживается об"]
    rpemodz = ["👤🫳😌", "👨🫳😌", "👩🫳😌", "👾🫳😨", "😺🦵😌"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ТРАХНУТЬ
@dp.message_handler(commands=["трахнуть"], commands_prefix="/!.") #Cама РП команда
async def rp8(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    

    result = randint(0, 100)
    if result >= 80:
        ms = False
        rpword = ["убежали в ужасе от", "убежал в ужасе от", "убежала в ужасе от", "решило обойти стороной", "убегает в ужасе от"]
        rpemodz = ["👤😱", "👨🏃‍♂️", "👩🏃‍♀️", "👾😱🌌", "🙀📦"]
        if user[4] == 3:
            nick2 = morph_word(user2[0], user2[2], user2[4])[3]
        else:
            nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    
    else:
        ms = True
        rpword = ["трахнули", "трахнул", "трахнула", "трахнуло", "трахает"]
        rpemodz = ["👤🌶😑", "👨🌶😑", "👩🌶😑", "👾🔞☠", "😽🔞😑"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    replic = get_replic(message.text)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if ms == True:
        eight_years(message.chat.id, user, user2, msg_info, True)

#ВЫЕБАТЬ
@dp.message_handler(commands=["выебать"], commands_prefix="/!.") #Cама РП команда
async def rp7(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return

    user2 = await rp_check(message)
    if user2 == None:
        return 0
    if user2[0] in no_rp_list:
        return
    user = get_user(message.from_user.id)
    
    result = randint(0, 100)
    if result >= 80:
        ms = False
        rpword = ["убежали в ужасе от", "убежал в ужасе от", "убежала в ужасе от", "решило обойти стороной", "убегает в ужасе от"]
        rpemodz = ["👤😱", "👨🏃‍♂️", "👩🏃‍♀️", "👾😱🌌", "🙀📦"]
        if user[4] == 3:
            nick2 = morph_word(user2[0], user2[2], user2[4])[3]
        else:
            nick2 = morph_word(user2[0], user2[2], user2[4])[1]
    else:
        ms = True
        rpword = ["выебали", "выебал", "выебала", "выебало", "ебёт с концами"]
        rpemodz = ["👤🌶😵", "👨🌶😵", "👩🌶😵", "👾🌶☠️", "😽🌶😵"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    replic = get_replic(message.text)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if ms == True:
        eight_years(message.chat.id, user, user2, msg_info, True)


#ИЗНАСИЛОВАТЬ
@dp.message_handler(commands=["изнасиловать"], commands_prefix="/!.") #Cама РП команда
async def rp6(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0
    if user2[0] in no_rp_list:
        return
    user = get_user(message.from_user.id)
    
    result = randint(0,100)
    if result < 80:
        ms = True
        rpword = ["изнасиловали", "изнасиловал", "изнасиловала", "изнасиловало", "насилует"]
        rpemodz = ["👤🔞😣", "👨🔞😣", "👩🔞😣", "👾🔞☠️", "😼🔞😣"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    else:
        ms = False
        rpword = ["были изнасилованы", "был изнасилован", "была изнасилована", "было изнасиловано", "насилуетcя"]
        rpemodz = ["😎🔞👤", "😎🔞👨", "😎🔞👩", "😎🔞👾", "😎🔞🙀"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    
    replic = get_replic(message.text)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    msg_info = await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")
    if ms == True:
        eight_years(message.chat.id, user, user2, msg_info, False)
    else:
        eight_years(message.chat.id, user2, user, msg_info, True)

#ПНУТЬ
@dp.message_handler(commands=["пнуть"], commands_prefix="/!.") #Cама РП команда
async def rp5(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return


    result = randint(0, 100)
    if result >= 80:
        rpword = ["пнули камень, а не", "пнул камень, а не", "пнула камень, а не", "пнуло камень, а не", "пинает-мяу камень, а не"]
        rpemodz = ["👤👟→🪨", "👨👞→🪨", "👩🥿→🪨", "👾🦵→🪨", "😾🦵→🪨"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    else:
        rpword = ["пнули", "пнул", "пнула", "пнуло", "пинает-мяу"]
        rpemodz = ["👤👟→😖", "👨👞→😖", "👩🥿→😖", "👾🦵→🌌", "😼🦵→📦"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    replic = get_replic(message.text)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#КУСНУТЬ
@dp.message_handler(commands=["куснуть"], commands_prefix="/!.") #Cама РП команда
async def rp4(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["куснули", "куснул", "куснула", "обучило ворарефилии", "царапкает"]
    rpemodz = ["🦇😙", "🧛😙", "🧛‍♀️😙", "👾⛩👻", "😽🩸😥"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#УКУСИТЬ
@dp.message_handler(commands=["укусить"], commands_prefix="/!.") #Cама РП команда
async def rp3(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["укусили", "укусил", "укусила", "зажевало", "надкусывает"]
    rpemodz = ["🩸🦇", "🩸🧛", "🩸🧛‍♀️", "👾🍖☠️", "😼🥩😭"]
    replic = get_replic(message.text)

    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#ОБНЯТЬ
@dp.message_handler(commands=["обнять"], commands_prefix="/!.") #Cама РП команда
async def rp2(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    user2 = await rp_check(message)
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    
    rpword = ["обняли", "обнял", "обняла", "окутало щупальцами", "обнимает"]
    rpemodz = ["👤🫂", "🤗", "🤗", "👾🤗🫁", "😺🤗"]
    replic = get_replic(message.text)

    if user2[4] != 2:
        rpemodz = ["👤🫂", "👨🫂", "🤗", "👾🤗🫁", "😺🤗"]
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")

#УБИТЬ
@dp.message_handler(commands=["убить"], commands_prefix="/!.") #Cама РП команда
async def rp1(message: types.Message):
    funny = get_funny(message)
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return

    user2 = await rp_check(message)
    
    if user2 == None:
        return 0

    user = get_user(message.from_user.id)
    if user2[0] in no_rp_list:
        return
    

    result = randint(0, 100)
    if result >= 80:
        rpword = ["были арестованы", "был арестован", "была арестована", "было запечатано", "затискивается"]
        rpemodz = ["👤⚔️🚓", "👨‍🦲🪓🚓", "👩‍🦲🔪🚓", "👾🪬🔯", "🐱🤗"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[4]
    else:
        rpword = ["убили", "убил", "убила", "убило", "убивает"]
        rpemodz = ["👤⚔️💀", "👨🪓☠️", "👩🔪⚰️", "👾🪬⚱️", "😸🧨🪦"]
        nick2 = morph_word(user2[0], user2[2], user2[4])[3]
    
    replic = get_replic(message.text)
    
    action = rpword[user[4]]
    rpemodz = rpemodz[user[4]]
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(user[2])}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>{html.escape(replic)}", parse_mode="html")


