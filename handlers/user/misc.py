from loader import dp, bot
from aiogram import types

from utils.db.db_utils_users import *
from utils.db.db_utils_сhats import *
from utils.db.db_utils_nicks import *
from utils.db.db_utils_warning import *

from utils.db.relations.db_utils_moniker import *
from settings import *
from ..f_lib.other import message_user_get, morph_word_simple, similaring, years_letter, update_morph, as_del_msg
import html

@dp.message_handler(commands=["username"], commands_prefix="!/.")
async def username_handler(message: types.Message):
    users = message.from_user
    
    try:
        moniker = get_max_monik(users.id)
        if moniker != None:
            set_moniker(users.id, moniker[1])
    except:
        pass
    
    

    create_user(users.id, users.username, users.first_name)
    
    user = message.from_user
    
    username = user.username
    
    if username != None:
            set_username(user.id, username)
            msg = await message.reply("<b>✅ Ваше Username успешно обновлено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
    else:
            set_username(user.id, user.id)
            msg = await message.reply("<b>✅ Ваше Username успешно обновлено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return



@dp.message_handler(commands=["прозвище", "прозвище-и", "прозвище-р", "прозвище-д", "прозвище-в", "прозвище-т", "прозвище-п", "розвище"], commands_prefix="+пП")
async def nick_handler(message: types.Message):

    
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    users = message.from_user
    user = create_user(users.id, users.username, users.first_name)
    command = message.text.split()[0]
    
    if message.reply_to_message:
        us = message.reply_to_message.from_user
        user = create_user(us.id, us.username, us.first_name)
        monikse = get_monik(user[0], user[8])
        
        if check_users_nick(user[0]):
            morph = morph_word_simple(user[2], user[4])
            nick = create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])
        
        if monikse == None or user[8] == "" or user[8] == None:
            msg = await message.reply("<b>❌ У него нет прозвища!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        
        if monikse[3] == '' and monikse[4] == '' and monikse[5] == '' and monikse[6] == '' and monikse[7] == '' and monikse[8] == '':
            no_monik = True
        elif monikse[3] == None and monikse[4] == None and monikse[5] == None and monikse[6] == None and monikse[7] == None and monikse[8] != None:
            no_monik = True
        else:
            no_monik = False
        
        if no_monik:
            monico = morph_word_simple(user[8], user[4])
            set_monik_nomn(user[0], user[8], monico[0])
            set_monik_gent(user[0], user[8], monico[1])
            set_monik_datv(user[0], user[8], monico[2])
            set_monik_accs(user[0], user[8], monico[3])
            set_monik_ablt(user[0], user[8], monico[4])
            set_monik_loct(user[0], user[8], monico[5])

        monikse = get_monik(user[0], user[8])
        msg = await message.reply(f"🎭 Прозвище - {html.escape(monikse[1])}\n—\nПадежи:\
                \n{html.escape(monikse[3])} — именительный.\
                \n{html.escape(monikse[4])} — родительный.\
                \n{html.escape(monikse[5])} — дательный.\
                \n{html.escape(monikse[6])} — винительный.\
                \n{html.escape(monikse[7])} — творительный.\
                \n{html.escape(monikse[8])} — предложный.\
                \n—\
                \n<code>+ты</code> (прозвище) - сменить основное прозвище кому-то другому.\
                \n<code>падежи</code> — вызвать справку по падежам.\
                \n<code>+прозвище</code> (любой символ) - вернуть падежи прозвища к стандарту.")
        
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    
    if check_users_nick(user[0]):
        morph = morph_word_simple(user[2], user[4])
        nick = create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])
    
    monic = message.text.replace(f"{command} ", "").replace(f"{command}", "")
    raises = [""]
    monikse = get_monik(user[0], user[8])
    if monikse == None or user[8] == "" or user[8] == None:
        msg = await message.reply("<b>❌ У вас нет прозвища!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    
    if monikse[3] == '' and monikse[4] == '' and monikse[5] == '' and monikse[6] == '' and monikse[7] == '' and monikse[8] == '':
        no_monik = True
    elif monikse[3] == None and monikse[4] == None and monikse[5] == None and monikse[6] == None and monikse[7] == None and monikse[8] != None:
        no_monik = True
    else:
        no_monik = False
    
    if no_monik:
        monico = morph_word_simple(user[8], user[4])
        set_monik_nomn(user[0], user[8], monico[0])
        set_monik_gent(user[0], user[8], monico[1])
        set_monik_datv(user[0], user[8], monico[2])
        set_monik_accs(user[0], user[8], monico[3])
        set_monik_ablt(user[0], user[8], monico[4])
        set_monik_loct(user[0], user[8], monico[5])
        
    
    
    if monic in raises or command.lower().startswith("прозвище"):
        monikse = get_monik(user[0], user[8])
        msg = await message.reply(f"🎭 Твоё прозвище - {html.escape(user[8])}\n—\nПадежи:\
        \n{html.escape(monikse[3])} — именительный. (<code>+прозвище-и</code> прозвище)\
        \n{html.escape(monikse[4])} — родительный. (<code>+прозвище-р</code> прозвище)\
        \n{html.escape(monikse[5])} — дательный. (<code>+прозвище-д</code> прозвище)\
        \n{html.escape(monikse[6])} — винительный. (<code>+прозвище-в</code> прозвище)\
        \n{html.escape(monikse[7])} — творительный. (<code>+прозвище-т</code> прозвище)\
        \n{html.escape(monikse[8])} — предложный. (<code>+прозвище-п</code> прозвище)\
        \n—\
        \n<code>+ты</code> (прозвище) - сменить основное прозвище кому-то другому.\
        \n<code>падежи</code> — вызвать справку по падежам.\
        \n<code>+прозвище</code> (любой символ) - вернуть падежи прозвища к стандарту.\
        \n—\
        \nПС. В скобках справа от падежей указаны команды, чтобы менять склонения своего прозвища.")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    
    
    elif len(monic) > 25:
        msg = await message.reply("<b>❌ прозвище не может содержать больше 25 символов!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    
    elif "https://" in monic:
        msg = await message.reply("<b>❌ прозвище не может содержать ссылок!</b>")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    
    else:
        if monic not in raises and command.lower().endswith("прозвище"):
            monico = morph_word_simple(user[8], user[4])
            set_monik_nomn(user[0], user[8], monico[0])
            set_monik_gent(user[0], user[8], monico[1])
            set_monik_datv(user[0], user[8], monico[2])
            set_monik_accs(user[0], user[8], monico[3])
            set_monik_ablt(user[0], user[8], monico[4])
            set_monik_loct(user[0], user[8], monico[5])
            
            msg = await message.reply(f"🎭 Твоё прозвище - {html.escape(user[8])}\n—\nПадежи:\
            \n{html.escape(monico[0])} — именительный. (<code>+прозвище-и</code> прозвище)\
            \n{html.escape(monico[1])} — родительный. (<code>+прозвище-р</code> прозвище)\
            \n{html.escape(monico[2])} — дательный. (<code>+прозвище-д</code> прозвище)\
            \n{html.escape(monico[3])} — винительный. (<code>+прозвище-в</code> прозвище)\
            \n{html.escape(monico[4])} — творительный. (<code>+прозвище-т</code> прозвище)\
            \n{html.escape(monico[5])} — предложный. (<code>+прозвище-п</code> прозвище)\
            \n—\
            \n<code>падежи</code> — вызвать справку по падежам.\
            \n<code>+ты</code> (прозвище) - сменить основное прозвище кому-то другому.\
            \n—\
            \nПС. В скобках справа от падежей указаны команды, чтобы менять склонения своего прозвища.")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        if command.lower().endswith("прозвище"):
            return
        
        moni = monic.split()
        mono_morph = morph_word_simple(user[8], user[4])
        
        if command.lower().endswith("прозвище-и"):
            mono = mono_morph[0].split()
        elif command.lower().endswith("прозвище-р"):
            mono = mono_morph[1].split()
        elif command.lower().endswith("прозвище-д"):
            mono = mono_morph[2].split()
        elif command.lower().endswith("прозвище-в"):
            mono = mono_morph[3].split()
        elif command.lower().endswith("прозвище-т"):
            mono = mono_morph[4].split()
        elif command.lower().endswith("прозвище-п"):
            mono = mono_morph[5].split()

        else:
            mono = user[8].split()

        
        if len(moni) != len(mono):
            msg = await message.reply("<b>❌ Отличается количество слов!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        stop = False
        i = 0
        while stop == False:
            try:
                moni_i = moni[i].lower()
                mono_i = mono[i].lower()
                i = i + 1
                
                if len(moni_i) > len(mono_i) + 2:
                    msg = await message.reply("<b>❌ Отличается более чем на два знака!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return
                
                if len(moni_i) < len(mono_i) - 2:
                    msg = await message.reply("<b>❌ Отличается более чем на два знака!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return
                parameter = int(round(100 - ( 100 * ( 2 / len(mono_i) ) )))

                
                if parameter > 90:
                    parameter = 90
                
                if parameter < 60:
                    parameter = 60
                
                if similaring(moni_i, [mono_i], parameter, 2) != True:
                    
                    msg = await message.reply("<b>❌ Cильно отличается!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                    return
                
            except:
                stop = True
       

        if command.lower().endswith("прозвище-р"):
            set_monik_gent(user[0], user[8], monic)
            msg = await message.reply("<b>✅ Прозвище-р успешно изменено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("прозвище-д"):
            set_monik_datv(user[0], user[8], monic)
            msg = await message.reply("<b>✅ Прозвище-д успешно изменено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("прозвище-в"):
            set_monik_accs(user[0], user[8], monic)
            msg = await message.reply("<b>✅ Прозвище-в успешно изменено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("прозвище-т"):
            set_monik_ablt(user[0], user[8], monic)
            msg = await message.reply("<b>✅ Прозвище-т успешно изменено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("прозвище-п"):
            set_monik_loct(user[0], user[8], monic)
            msg = await message.reply("<b>✅ Прозвище-п успешно изменено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("прозвище-и"):
            set_monik_nomn(user[0], user[8], monic)
            msg = await message.reply("<b>✅ Прозвище-и успешно изменено!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        else:
            msg = await message.reply("<b>✅ Что-то пошло не так!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        





@dp.message_handler(commands=["ник", "ник-и", "ник-р", "ник-д", "ник-в", "ник-т", "ник-п"], commands_prefix="+")
async def nick_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    users = message.from_user
    user = create_user(users.id, users.username, users.first_name)
    command = message.text.split()[0]
    
    if check_users_nick(user[0]):
        morph = morph_word_simple(user[2], user[4])
        nick = create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])
    
    nick = message.text.replace(f"{command} ", "").replace(f"{command}", "")
    raises = [""]
    
    if nick in raises:
        morph = morph_word_simple(user[2], user[4])
        create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])
        msg = await message.reply("<b>❌ Укажите ник!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    
    elif len(nick) > 20:
        
        if command.lower().endswith("ник"):
            msg = await message.reply("<b>❌ Ник не может содержать больше 20 символов!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        elif len(nick) > 25:
            msg = await message.reply("<b>❌ Ник не может содержать больше 25 символов!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return

    elif "https://" in nick:
        msg = await message.reply("<b>❌ Ник не может содержать ссылок!</b>")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await as_del_msg(message.chat.id, msg.message_id, time_del)
    
    else:
        if command.lower().endswith("ник"):
            if check_nick(nick) == True:
                msg = await message.reply("<b>✅ Ник уже занят!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            
            set_nick(user[0], nick)
            user = get_user(user[0])
            morph = morph_word_simple(user[2], user[4])
            create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])
            msg = await message.reply("<b>✅ Ник успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        elif command.lower().endswith("ник-и"):
            set_nick_nomn(user[0], nick)
            msg = await message.reply("<b>✅ Ник-и успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("ник-р"):
            set_nick_gent(user[0], nick)
            msg = await message.reply("<b>✅ Ник-р успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("ник-д"):
            set_nick_datv(user[0], nick)
            msg = await message.reply("<b>✅ Ник-д успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("ник-в"):
            set_nick_accs(user[0], nick)
            msg = await message.reply("<b>✅ Ник-в успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("ник-т"):
            set_nick_ablt(user[0], nick)
            msg = await message.reply("<b>✅ Ник-т успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif command.lower().endswith("ник-п"):
            set_nick_loct(user[0], nick)
            msg = await message.reply("<b>✅ Ник-п успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        else:
            if check_nick(nick) == True:
                msg = await message.reply("<b>❌ Ник уже занят!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            
            set_nick(user[0], nick)
            morph = morph_word_simple(user[2], user[4])
            nick = create_user_nick(user[0], user[2], morph[0], morph[1], morph[2], morph[3], morph[4], morph[5])
            msg = await message.reply("<b>✅ Ник успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return





@dp.message_handler(commands=["ты"], commands_prefix="+")
async def moniker_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    if message.reply_to_message:
        us = message.reply_to_message.from_user
        usern = create_user(us.id, us.username, us.first_name)
            
        if usern[0] in no_rp_list:
            return
        
        users = message.from_user
        user = create_user(users.id, users.username, users.first_name)
        
        
        if user == usern:
            msg = await message.reply("<b>❌ Эта команда неприменима к самому себе!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        # if user[5] < 0:
            # await message.reply("<b>❌ У вас недостаточно репутации для этого!</b>")
            # return
        mix = user[5]/10
        
        add_rep_monik = int(round(mix)) + 1
        command = message.text.split()[0]
        moniker = message.text.replace(command + " ", "").strip() 

        if moniker == command:
            msg = await message.reply("<b>❌ Укажите прозвище!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        elif len(moniker) > 20:
            msg = await message.reply("<b>❌ Прозвище не может содержать больше 20 символов!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        
        elif "https://" in moniker:
            msg = await message.reply("<b>❌ Прозвище не может содержать ссылок!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            return
        
        
        if check_monik(usern[0], moniker) == False: #Ищем усиляемое прозвище в базе. False -  Не нашли. Любое первое - будет таким.
            create_monik(usern[0], moniker)
            
            add_z_rep(usern[0], moniker, add_rep_monik) #Добавляем репутацию прозвищу.
            take_rep(user[0])
            
            msg = await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={user[0]}'>-1</a>)")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            
            msg = await message.reply("<b>✅ Прозвище успешно создано!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            
            try:
                moniker = get_max_monik(usern[0])
                if moniker != None:
                    if moniker[1] != usern[8]:
                        set_moniker(usern[0], moniker[1])
                        msg = await message.reply("<b>✅ Прозвище успешно изменено!</b>")
                        await as_del_msg(message.chat.id, msg.message_id, time_del)
            except:
                pass
            
            return
        
        else:
            add_z_rep(usern[0], moniker, add_rep_monik) #Добавляем репутацию прозвищу.
            take_rep(user[0])
            
            msg = await message.answer(f"❌ Понижение засчитано (<a href='tg://user?id={user[0]}'>-1</a>)")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            try:
                monikerm = get_max_monik(usern[0])
                if monikerm != None:
                    if monikerm[1] != usern[8]:
                        msg = await message.reply("<b>✅ Прозвище успешно изменено!</b>")
                        await as_del_msg(message.chat.id, msg.message_id, time_del)
                        set_moniker(usern[0], monikerm[1])
                    else:
                        if moniker == monikerm[1]:
                            msg = await message.reply("<b>✅ Текущее прозвище успешно усилено!</b>")
                            await as_del_msg(message.chat.id, msg.message_id, time_del)
                        else:
                            msg = await message.reply("<b>✅ Прозвище успешно усилено!</b>")
                            await as_del_msg(message.chat.id, msg.message_id, time_del)
            except:
                pass

    else:
        msg = await message.reply("<b>❌ Эту команду следует применять в ответ на сообщение!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return




@dp.message_handler(commands=["био"], commands_prefix="+")
async def bio_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    users = message.from_user
    create_user(users.id, users.username, users.first_name)
    bio = message.text.replace("+био ", "").replace("+Био ", "")
    raises = ["+био", "+Био", ""]
    if bio in raises:
        msg = await message.reply("<b>❌ Укажите текст!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    elif len(bio) > 50:
        msg = await message.reply("<b>❌ Био не может содержать больше 50 символов!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    elif "https://" in bio:
        msg = await message.reply("<b>❌ Био не может содержать ссылок!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        return
    else:
        user = message.from_user
        set_bio(user.id, bio)
        msg = await message.reply("<b>✅ Био успешно изменено!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return


@dp.message_handler(commands=["вид"], commands_prefix="+")
async def bio_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    users = message.from_user
    create_user(users.id, users.username, users.first_name)
    
    specie = message.text.replace("+вид ", "").replace("+Вид ", "")
    raises = ["+вид", "+Вид", ""]
    if specie in raises:
        msg = await message.reply("<b>❌ Укажите текст!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    elif len(specie) > 20:
        msg = await message.reply("<b>❌ Вид не может содержать больше 20 символов!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    elif "https://" in specie:
        msg = await message.reply("<b>❌ Вид не может содержать ссылок!</b>")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    else:
       
        set_specie(users.id, specie)
        
        user = get_user(users.id)
        
        if user[4] == 3 or user[4] == 4:
            set_gender(users.id, 0)
        msg = await message.reply("<b>✅ Вид успешно изменён!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return


@dp.message_handler(commands=["пол"], commands_prefix="+")
async def gender_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    gender = message.text.replace("+пол ", "").replace("+Пол ", "")
    raises = ["+пол", "+Пол", ""]
    users = message.from_user
    user = create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    update_morph(user[0])
    
    
    if user[4] == 3 or user[4] == 4:
        if gender in raises:
            msg = await message.reply("<b>❌ Укажите текст!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif len(gender) > 20:
            msg = await message.reply("<b>❌ Пол не может содержать больше 20 символов!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        elif "https://" in gender:
            msg = await message.reply("<b>❌ Пол не может содержать ссылок!</b>")
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
        else:
            set_specie(users.id, gender)
            msg = await message.reply("<b>✅ Пол успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
    if gender in raises:

        msg = await message.reply("<b>❌ Укажите значение!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    
    allow = 0
    for izvrat in botovod_id:
        if message.from_user.id == izvrat:
            allow = 1
            continue

    if allow == 0:
        if gender != "0" and gender != "1" and gender != "2":
            if "муж" in message.text.lower():

                set_gender(user[0], 1)
                msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            elif "жен" in message.text.lower(): 

                set_gender(user[0], 2)
                msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            else:    
                msg = await message.reply("<b>❌ Укажите верное значение!</b>\nПример: +пол 1\n0 - [-]; 1 - Парень; 2 - Девушка")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
        else:
            users = message.from_user
            set_gender(users.id, gender)
            msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return
    if allow == 1:
        if gender != "0" and gender != "1" and gender != "2" and gender != "3" and gender != "4":
            if "муж" in message.text.lower():
                set_gender(user[0], 1)
                msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            elif "жен" in message.text.lower(): 
                set_gender(user[0], 2)
                msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            elif "ино" in message.text.lower(): 
                set_gender(user[0], 3)
                msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            elif "кот" in message.text.lower() or "чешир" in message.text.lower(): 
                set_gender(user[0], 4)
                msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
            else:    
                msg = await message.reply("<b>❌ Укажите верное значение!</b>\nПример: +пол 1\n0 - [-]; 1 - Парень; 2 - Девушка")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return

        else:
            users = message.from_user
            set_gender(users.id, gender)
            if int(gender) == 3 or int(gender) == 4:
                set_specie(users.id, "Неопределимо")
                msg = await message.reply("<b> ✅ Вид успешно изменён!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
            msg = await message.reply("<b> ✅ Пол успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
            return


# Текущие мут, репа и шанс антимата
@dp.message_handler(commands=['антимат',], commands_prefix='!?./')
async def get_antimat(message: types.Message):
    if message.chat.type == 'private':
        return
    warner = get_warner(message.chat.id, message.from_user.id)
    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    if warner[4] != 0:
        return
    
    chats = message.chat.id
    chat = get_chat(chats)
    if check_chat(message.chat.id):
        create_chat(message.chat.id)

        chat = get_chat(chats)
        msg = await message.reply(f"🎲 Шанс антимата - {str(chat[1])} процентов.\n⏳ Мут антимата - {str(chat[2])} секунд.\n👑 Репутация антимата - [{str(chat[7]).replace('1', 'Включено').replace('0', 'Выключено')}].")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return
    else:
        msg = await message.reply(f"🎲 Шанс антимата - {str(chat[1])} процентов.\n⏳ Мут антимата - {str(chat[2])} секунд.\n👑 Репутация антимата - [{str(chat[7]).replace('1', 'Включено').replace('0', 'Выключено')}].")
        await as_del_msg(message.chat.id, msg.message_id, time_del)



# УЗНАТЬ ПРИВЕТСТВИЕ
@dp.message_handler(commands=['приветствие',], commands_prefix='!?./')
async def get_welcome(message: types.Message):
    if message.chat.type == 'private':
        return
    
    warner = get_warner(message.chat.id, message.from_user.id)
    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    if warner[4] != 0:
        return
    
    chats = message.chat.id
    chat = get_chat(chats)
    if check_chat(message.chat.id):
        create_chat(message.chat.id)

        chat = get_chat(chats)

    msg = await message.reply(f"👋 Текущее приветствие: \n{chat[5]}[Никнейм]{chat[6]}", parse_mode='html')
    await as_del_msg(message.chat.id, msg.message_id, time_del)



#Узнать состояние спамлимитов
@dp.message_handler(commands=["спамлимиты"], commands_prefix="/!.")
async def secmat_handler(message: types.Message):
    if message.chat.type == 'private':
        return

    warner = get_warner(message.chat.id, message.from_user.id)
    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    if warner[4] != 0:
        return
    
    chats = message.chat.id
    chat = get_chat(chats)
    if check_chat(message.chat.id):
            create_chat(message.chat.id)
            chat = get_chat(chats)
            
    msg = await message.reply(f"⛔️ Текущий статус спам-лимитов в чате:\
                        \n Предел текстовых сообщений — {chat[9]} шт. подряд\
                        \n Предел видео-сообщений — {chat[10]} шт. подряд\
                        \n Предел GIF-сообщений — {chat[11]} шт. подряд\
                        \n Предел фото-сообщений — {chat[8]} шт. подряд\
                        \n Предел для стикеров — {chat[12]} шт. подряд\
                        \n")
    await as_del_msg(message.chat.id, msg.message_id, time_del)
    return
    
@dp.message_handler(commands=["возраст", "озраст"], commands_prefix="+вВ")
async def gender_handler(message: types.Message):
    if message.chat.type != 'private':
        warner = get_warner(message.chat.id, message.from_user.id)
        if warner == None:
            warner = [message.chat.id, message.from_user.id, 0, 0, 0]
        if warner[4] != 0:
            return
    
    
    command = message.text.split()[0]
    if "+" not in command:
        if len(message.text.split()) > 1:
            return

    age = message.text.replace(f"{command} ", "").replace(f"{command}", "")
    raises = [""]
    users = message.from_user
    user = create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    

    if age in raises or "+" not in command:
        age = user[6]
        msg = await message.reply(f"<b>Ваш возраст составляет {age} {years_letter(age)}!</b>")
        await as_del_msg(message.chat.id, msg.message_id, time_del)
        return

    try:
        age = int(age)
        if age >= 0:
            set_age(users.id, age)
            msg = await message.reply("<b> ✅ Ваш возраст успешно изменён!</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
        else:
            msg = await message.reply("<b> Вы из будущего?</b>")
            await as_del_msg(message.chat.id, msg.message_id, time_del)
    
    except:
        try:
            age = age.split()[0]
            try:
                age = int(age)
                if age >= 0:
                    set_age(users.id, age)
                    msg = await message.reply("<b> ✅ Ваш возраст успешно изменён!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                else:
                    msg = await message.reply("<b> Вы из будущего?</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
            
            except:
                msg = await message.reply("<b>❌ Укажите число!</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return
        except:
            try:
                age = int(age)
                if age >= 0:
                    set_age(users.id, age)
                    msg = await message.reply("<b> ✅ Ваш возраст успешно изменён!</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
                else:
                    msg = await message.reply("<b> Вы из будущего?</b>")
                    await as_del_msg(message.chat.id, msg.message_id, time_del)
            
            except:
                msg = await message.reply("<b>Вы старше вселенной?</b>")
                await as_del_msg(message.chat.id, msg.message_id, time_del)
                return