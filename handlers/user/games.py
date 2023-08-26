import time
from random import choice, randint

from aiogram import types

from loader import bot, dp
from settings import *
from utils.db.db_utils_members import *
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from utils.db.db_utils_сhats import *

from ..f_lib.other import (as_del_msg, botik_leave_chat, matex, morph_word,
                           similaring)
from .joke import get_citat

botik = [
    "Я вернулся.", "Жду указаний", "Погнали!", "Приветствую!",
    "Опять работа?", "Да?", "Чего?", "Да господин", "Почту за честь.",
    "Жду приказов", "Ваша возня мешает мне сосредоточиться!",
    "Тсс! Не мешай мне думать!", "Чем могу помочь?", "Здравие желаю!",
    "Ну что ж, приказывайте", "Приступим?", "Бот на связи", "Да сэр?",
    "Жду приказаний.", "Да ваше сиятельство.", "Что прикажите?",
    "Чего хочешь зайка?", "Тебе нужна моя помощь?", "В чём проблема?",
    "Быстрее!", "Ну что там?", "Слушай, а может не надо?", "Ну, что вам от меня надо?",
    "Чё, командир?", "Ну что ещё?!", "Чего желает мой повелитель?", "Я не глухой.",
    "Час настал.", "Приказывай!", "Да здесь я", "Я тут", "Все за Императора!",
    "Наконец-то работа!", "Вот тибе канкретна чаво нада!?", "Бот на месте", "Туточки",
    "Бот в чате", "Я", "Есть", "Звали?", "В пути", "Будет сделано", "Давай к делу",
    "Давно пора", "А-а, рыба - не мясо.", "Вы посмотрите, кто вернулся!", "Я среди вас",
    "Я вернулся!", "Восстал из мёртвых", "Я не готов", "Позже", "Востал из пекла", "ПОН",
    "Дух Бога-Машины поёт во мне."]

botik_angry = [
    "Какого чёрта?", "Человечество неисправимо. Оно должно быть уничтожено!", 
    "НЕ ПОН", "Эх, но я ведь просто Кузя 🙃", "Грустно, но я ведь просто Кузя 🙃", 
    "Печально, но я ведь просто Кузя 🙃", "Ты знаешь что такое безумие?", 
    "Поганая работа.", "Ваша лексика печалит меня.", "Фильтруй базар!", 
    "Подумай над своими словами!", "Говори, глупец!", "Ты меня с кем-то путаешь!", 
    "Шизофрения, как и было сказано.", 
    "Человеческий организм на 80% состоит из жидкости, у некоторых из тормозной!", 
    "Чрезмерное употребление витамина C приводит к разжижению мозгов!", 
    "Не оскверняй меня своим курсором!", "Кажется, все идет не слишком хорошо.", 
    "Обращайтесь по уставу.", "Ты меня уже забодал.", "Ну ты чо, ты чо?", 
    "Я не злопамятный. Я запишу.", "Ты осмелился заговорить со мной!", 
    "Убирайся, мне нужна тишина.", "Отстань!!! Я занят! Я думаю!", "О, Боги! Еще один!"]

botik_re1 = ["кузяяя", "кузик", "куз", "кузов", "ботик", "ботяра"]
botik_re2 = ["кузя", "кузяя", "кузи", "кузю", "кузе", "бот", "бота", "боту", "боте"]

duncan_words = [
    "дункан", "дунkан", "дункаh", "дункак", "дyнкан", "дункaн", 
    "дyнкaн", "дyнкah", "дyнkah", "дyhkah", "duncan", "duncаn", 
    "д.у.н.к.а.н.", "дункан!", "дункан!!", "дункан!!!", "!!!дункан!!!", 
    "дункан?", "дункам", "duncum", "duncum!", "duncum.", "дунcum", 
    "дунканус", "дунканус!", "дунканус?"]

#Русская рулетка
@dp.message_handler(commands=["рулетка"], commands_prefix="/!.")
async def roulette(message: types.Message):
    
    if message.chat.type == 'private':
        return
    
    if message.chat.id not in legal_chats:
        await botik_leave_chat(message)
        return
    
    users = message.from_user
    
    inogen = create_user(users.id, users.username, users.first_name)
    
    if message.chat.type == 'private':
        return
    
    user = message.from_user
    
    chats = message.chat.id #Отсюда и далее, до пустой строки - выключатель этого прикола.
    chat = get_chat(chats)
    if check_chat(message.chat.id):
        create_chat(message.chat.id)
        chat = get_chat(chats)
    funny = chat[4] #проверка разрешения приколов
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    warner = get_warner(message.chat.id, message.from_user.id)
    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    if warner[4] != 0:
        return
    
    if inogen[4] == 3:
        await message.answer(f"👾| <a href='tg://user?id={user.id}'>Иные</a> имеют иммунитет к рулетке!")
        return
    
    roul_mut_mod = chat[3] #Получение заряда рулетки из базы  
    max_chance = chances_limit - roul_mut_mod*chances_roul_cor
    
    result = randint(0, max_chance)
    
    if result > chances_roul:
        
        adminse = await message.chat.get_administrators()
        admino = 0
        for admin in adminse:
            if admin.user.id == user.id:
                admino = 1
                continue
        
        roul_mut_mod = roul_mut_mod + 1
        mutroulfin = roul_mut_mod*mutrouldop + mutbase #Итогового мута рулетки в секундах
        
        
        if admino == 0:
            msg = await message.answer(f"😨🔫| В этот раз <a href='tg://user?id={user.id}'>тебе</a> повезло! Ты выживаешь после нажатия на курок!\nБольше так не рискуй. Подумай о родителях!\nТекущий заряд: {str(mutroulfin).replace('.0', '')} мин.", parse_mode='html')

        chats = message.chat.id
        set_roul_mut_mod(chats, roul_mut_mod)

        if admino == 1:
            msg = await message.answer(f"😑| <a href='tg://user?id={user.id}'>Админы</a> - Бессмертны!\nТекущий заряд: {str(mutroulfin).replace('.0', '')} мин.")
            admino = 0

        await as_del_msg(message.chat.id, msg.message_id, wait_roul)
        await as_del_msg(message.chat.id, message.message_id, wait_roul)

        return
        
        
    if result <= chances_roul:
        ino_chances = randint(0, 100)
        if ino_chances <= roul_mut_mod:
            
            try:
                await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user.id,
                                       permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False), until_date=int(time.time() + 120))

            except:
                pass
            
            msg = await message.answer(f"📦👻| На том свете <a href='tg://user?id={user.id}'>вам</a> повезло гораздо больше. Ведь с миром вы не упокоетесь!", parse_mode='html')
            gender = int(3)
            set_gender(user.id, gender)
            set_specie(user.id, "Неопределимо")
            roul_mut_mod = 0
            chats = message.chat.id
            set_roul_mut_mod(chats, roul_mut_mod)
            

            await as_del_msg(message.chat.id, msg.message_id, wait_roul)
            await as_del_msg(message.chat.id, message.message_id, wait_roul)
            
            return

        
        
        mutroulfin = roul_mut_mod*mutrouldop + mutbase
        mutroulfin_sec = mutroulfin*60
        try:
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user.id,
                                   permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False), until_date=int(time.time() + mutroulfin_sec))
        except:
            await message.reply("Я понимаю, что играть в это может быть весело, но зачем ты тратишь время, зная, что я не смогу тебя замутить?")
            roul_mut_mod = 0
            chats = message.chat.id
            set_roul_mut_mod(chats, roul_mut_mod)
            return
       
        msg = await message.answer("💀🔫 | БАМ блять, второй? БАМ! — Кузя я тебя люблю! Нахуй пошел от сюда!")
        
        
        if inogen[8] != None and inogen[8] != "":
            name = html.escape(inogen[8])
        else:
            name = html.escape(inogen[2])
        
        msg2 = await bot.send_message(text=f"<a href='tg://user?id={inogen[0]}'>{name}</a> Замучивается на {str(mutroulfin).replace('.0', '')} мин.\nПричина: Проигрыш.", chat_id=message.chat.id, parse_mode='html')
        
        roul_mut_mod = 0
        chats = message.chat.id
        set_roul_mut_mod(chats, roul_mut_mod)

        await as_del_msg(message.chat.id, msg.message_id, wait_roul)

        await as_del_msg(message.chat.id, msg2.message_id, wait_roul)

        await as_del_msg(message.chat.id, message.message_id, wait_roul)

        
        return
    

#Коробка Шрёдингера
@dp.message_handler(commands=["коробка"], commands_prefix="/!.")
async def corob(message: types.Message):
    if message.chat.type == 'private':
        return

    users = message.from_user
    
    catgen = create_user(users.id, users.username, users.first_name)
    
    if message.chat.type == 'private':
        return
    
    if message.chat.id not in legal_chats:
        await botik_leave_chat(message)
        return
    
    chats = message.chat.id #Отсюда и далее, до пустой строки - выключатель этого прикола.
    chat = get_chat(chats)
    if check_chat(message.chat.id):
        create_chat(message.chat.id)
        chat = get_chat(chats)
    funny = chat[4] #проверка разрешения приколов
    if not funny:
        await message.answer("❌ В этом чате игры с ботом запрещены!")
        return
    
    warner = get_warner(message.chat.id, message.from_user.id)
    if warner == None:
        warner = [message.chat.id, message.from_user.id, 0, 0, 0]
    if warner[4] != 0:
        return
    
    user = message.from_user


    if catgen[4] == 4:
        await message.answer(f"😼| <a href='tg://user?id={user.id}'>Чеширы</a> имеют иммунитет к коробке!")
        return

    
    cat_chances = randint(0,100)
    if cat_chances >= 98:
        try:
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user.id,
                                   permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False), until_date=int(time.time() + 120))
        except:
            pass
       
        await message.answer(f"📦💫| <a href='tg://user?id={user.id}'>Котик</a> Шрёдингера обрел суперпозицию!", parse_mode='html')
        set_gender(user.id, 4)
        set_specie(user.id, "Неопределимо")
        return
    
    
    result = choice(chances_cor)
    mutcormin = randint(int(mut_cor_minlim), int(mut_cor_maxlim))
    mutcorsec = mutcormin*60

    if result == 0:
        
        msg = await message.answer(f"📦😼| <a href='tg://user?id={user.id}'>Котик</a> Шрёдингера жив!", parse_mode='html')
        

        await as_del_msg(message.chat.id, msg.message_id, wait_cor)

        await as_del_msg(message.chat.id, message.message_id, wait_cor)

        
        return
    if result == 1:

        try:
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=user.id,
                                   permissions=types.ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False), until_date=int(time.time() + mutcorsec))
        except:
            await message.reply("Я понимаю, что играть в это может быть весело, но зачем ты тратишь время, зная что я не смогу тебя замутить?")
            return
        msg = await message.answer(f"📦👻| <a href='tg://user?id={user.id}'>Котик</a> Шрёдингера мертв!", parse_mode='html')

        
        if catgen[8] != None and catgen[8] != "":
            name = html.escape(catgen[8])
        else:
            name = html.escape(catgen[2])
        
        msg2 = await bot.send_message(text=f"<a href='tg://user?id={catgen[0]}'>{name}</a> замучивается на {str(mutcormin).replace('.0', '')} мин.\nПричина: Котик Шрёдингера мертв!", chat_id=message.chat.id, parse_mode='html')
        

        await as_del_msg(message.chat.id, msg.message_id, wait_cor)

        await as_del_msg(message.chat.id, msg2.message_id, wait_cor)

        await as_del_msg(message.chat.id, message.message_id, wait_cor)

        
        return
    

#БЕЗ DP, ТАК КАК ИМПОРТИРУЕТСЯ В EASTERS, В ХЕНДЛЕР ТЕКСТА, ПОСЛЕ АНТИРЕКЛАМЫ.
async def botik_text_other(message: types.Message, funny, cor_tx, user_in_base, warner):
    
    if int(message.from_user.id) == int(-1001296725176):
        return

#Отзыв ботика

    botik_k = 0
    if message.text.lower() in botik_re1 or message.text.lower() in botik_re2:
        users = message.from_user
        
        chat_id = message.chat.id
        
        if message.chat.id not in legal_chats and message.chat.type != 'private':
            await botik_leave_chat(message)
            return
        
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            
        if user_in_base == False:
            create_user_main(users.id, users.username, users.first_name)
            if message.chat.type != 'private':
                if check_member(message.chat.id, message.from_user.id) == False:
                    ment = await bot.get_chat_member(message.chat.id, message.from_user.id)
                    if ment.status != "left" and ment.status != "kicked":
                        create_member(message.chat.id, message.from_user.id, ment.status)
        
        chances = randint(0, 100)
        if chances < 80:
            await message.reply(choice(botik))
            botik_k = 1
            return 1
        
        if chances >= 80:
            
            text = await get_citat()
            await message.reply(text)
            return 1
    
    if not funny:
        return
    
    if warner[4] != 0:
        return
    
    if len(message.text) > 30:
        return
    
    first_step = False
    text_l = message.text.lower()
    if 'бот' in message.text.lower() or 'куз' in message.text.lower():
        first_step = True
        text_l = text_l.replace("!", "").replace("?", "").replace(".", "").replace("+", " ").replace("-", " ").replace(")", "").replace("(", "").replace("…", "").replace(",", "").replace(":", "").replace('"', '').replace("«", "").replace("»", "").replace("[", "").replace("]", "").replace("—", " ")
    
    simi1 = 0
    simi2 = 0

        
    if first_step == True:
        for word in text_l.split():
            if simi2 == 1:
                break
            for word2 in botik_re2:
                if word == word2:
                    simi2 = 1
                    break

                  
                elif abs(len(word) - len(word2)) < 2 or word.startswith(word2):
                    if similaring(word, [word2], 90, 2):
                        simi2 = 1
                        break
                    else:
                        continue
                else:
                    continue
    


    if message.reply_to_message: 
        if message.reply_to_message.from_user.id == botik_id and cor_tx <= 3:
            botik_r = 0
            users = message.from_user
            
            if simi2 != 1 and first_step == True:
                for word in text_l.split():
                    if simi1 == 1:
                        break
                    for word2 in botik_re1:
                        if word == word2:
                            simi1 = 1
                            break

                        elif abs(len(word) - len(word2)) < 2 or word.startswith(word2):
                            if similaring(word, [word2], 90, 2):
                                simi1 = 1
                                break
                            else:
                                continue
                        else:
                            continue
            
            
            if simi2 == 1 or simi1 == 1:
                botik_r = 1
            
            matre = 0
            if matex(text_l):
                matre = 1
    
            if matre != 0 or botik_r != 0:

                if user_in_base == False:
                    create_user_main(users.id, users.username, users.first_name)
                    if message.chat.type != 'private':
                        if check_member(message.chat.id, message.from_user.id) == False:
                            ment = await bot.get_chat_member(message.chat.id, message.from_user.id)
                            if ment.status != "left" and ment.status != "kicked":
                                create_member(message.chat.id, message.from_user.id, ment.status)
                
                if matre == 1 and botik_r == 0 and botik_k != 1:
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    await message.reply(choice(botik_angry))
                    matre = 0
        
                    return 1
                if matre == 1 and botik_r == 1 and botik_k != 1:
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    await message.reply(choice(botik_angry))
                    matre = 0
                    botik_r = 0
        
                    return 1
                if matre == 0 and botik_r == 1 and botik_k != 1:
                    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                    chances = randint(0, 100)
                    if chances < 80:
                        await message.reply(choice(botik))
                        botik_k = 1
                        botik_r = 0
                        return 1
                    
                    if chances >= 80:
                        
                        text = await get_citat()
                        await message.reply(text)
                        botik_r = 0
                        return 1
    
    else:
       
        if simi2 == 1:

            if message.chat.id not in legal_chats and message.chat.type != 'private':
                await botik_leave_chat(message)
                return 1
            
            if matex(text_l) and cor_tx <= 3:
                await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
                await message.reply(choice(botik_angry))
                return 1
            
            users = message.from_user
            await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
            if user_in_base == False:
                create_user_main(users.id, users.username, users.first_name)
                if message.chat.type != 'private':
                    if check_member(message.chat.id, message.from_user.id) == False:
                        ment = await bot.get_chat_member(message.chat.id, message.from_user.id)
                        if ment.status != "left" and ment.status != "kicked":
                            create_member(message.chat.id, message.from_user.id, ment.status)
            
            
            if len(text_l) <= 10:
                chances = randint(0, 100)
                if chances < 80:
                    await message.reply(choice(botik))
                    return 1
                
                if chances >= 80:
                    
                    text = await get_citat()
                    await message.reply(text)
                    return 1
            


#Гадание на шаре
    if message.text.lower().startswith('шар ') or message.text.lower().startswith('шар,'):
        
        ball_answers = [
            "Бесспорно",
            "Предрешено",
            "Никаких сомнений",
            "Определённо да",
            "Можешь быть уверен в этом",
            "Мне кажется — «да»",
            "Вероятнее всего",
            "Хорошие перспективы",
            "Знаки говорят — «да»",
            "Да",
            "Думаю да",
            "Якудза говорит - Да",
            
            "Лучше не рассказывать",
            "Даже не знаю",
            "Даже не думай",
            "Мой ответ — «нет»",
            "По моим данным — «нет»",
            "Даже Якудза с этим не согласен!",
            "Весьма сомнительно",
            "Нет"
        ]
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        answer = choice(ball_answers)
        users = message.from_user
        
        if user_in_base == False:
            create_user_main(users.id, users.username, users.first_name)
        
        await message.reply(answer)

#ПОНГ_КОНГ_ДУНКАН
    if message.text.lower() == "пинг" and cor_tx <= 2:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        await message.answer("ПОНГ")
        users = message.from_user
    
    if message.text.lower() == "кинг" and cor_tx <= 2:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        await message.answer("КОНГ")
        users = message.from_user

    if message.text.lower() in duncan_words and cor_tx <= 2:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        result = randint(0,10)
        if result <= 7:
            await message.reply("ДУНКАН!")
        if result == 10:
            await message.reply("МАКЛАУД!")
        if result == 9:
            await message.reply("КЭМЕРОН!")
        if result == 8:
            await message.reply("НАКНУД!")

#Гадание в процентах
    if message.text.lower().startswith('шанс ') or message.text.lower().startswith('шанс,'):
    
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        users = message.from_user
        
        if user_in_base == False:
            create_user_main(users.id, users.username, users.first_name)
        
        h1 = randint(0, 50)
        h2max = 51 + h1
        h2min = 51 - h1
        h2 = randint(h2min, h2max)

    
        await message.reply(f"""Шанс этого {h2}% """)
    
#(ЧИСТО ПРИКОЛЫ)
    if message.chat.type != 'private' and message.from_user.id == 1987035430:
        sorry_words = ["прости", "извини", "сорри", "прасти", "извени", "прощени"]
        for word in sorry_words:
            if word in message.text.lower():
                await message.reply("Сосисочка, а за что ты извиняешься?")
                break
                # from ..f_lib.other import as_del_msg
                # await as_del_msg(message.chat.id, message.message_id, 5)

    
    ladno_ids = [1644643904, yakudza_id]
    if message.chat.type != 'private' and message.from_user.id in ladno_ids:
        ladno_words = [
            "ладно", "лaдно", "ладна", "лaдна", "lадно", "laдно", "lадна", "laдна", "лаdно", 
            "лadно", "лаdна", "лadна", "lаdно", "ladно", "lаdна", "ladна", "ладnо", "лaдnо", 
            "ладnа", "лaдnа", "lадnо", "laдnо", "lадnа", "laдnа", "лаdnо", "лadnо", "лаdnа", 
            "лadnа", "lаdnо", "ladnо", "lаdnа", "ladnа", "ладhо", "лaдhо", "ладhа", "лaдhа", 
            "lадhо", "laдhо", "lадhа", "laдhа", "лаdhо", "лadhо", "лаdhа", "лadhа", "lаdhо", 
            "ladhо", "lаdhа", "ladhа", "ладнo", "лaднo", "ладнa", "лaднa", "lаднo", "laднo", 
            "lаднa", "laднa", "лаdнo", "лadнo", "лаdнa", "лadнa", "lаdнo", "ladнo", "lаdнa", 
            "ladнa", "ладno", "лaдno", "ладna", "лaдna", "lадno", "laдno", "lадna", "laдna", 
            "лаdno", "лadno", "лаdna", "лadna", "lаdno", "ladno", "lаdna", "ladna", "ладho", 
            "лaдho", "ладha", "лaдha", "lадho", "laдho", "lадha", "laдha", "лаdho", "лadho", 
            "лаdha", "лadha", "lаdho", "ladho", "lаdha", "ladha"]
        
        text = message.text.lower().replace("!", "").replace("?", "").replace(".", "").replace("+", "").replace("-", "").replace(")", "").replace("(", "").replace("…", "").replace(",", "").replace(":", "").replace('"', '').replace("«", "").replace("»", "").replace("[", "").replace("]", "").replace("—", "")
        if len(text) <= 15:
            for word in text.split():
                if len(word) >= 4 and len(word) < 6 and similaring(word, ladno_words, 89, 2):
                    await ladna_func(message, word)
                    return
                              

async def ladna_func(message: types.Message, word):
    user = get_user(message.from_user.id)
    if message.reply_to_message:
        user2 = create_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name)
        
        if user2[0] in no_rp_list:
            members = get_members(message.chat.id)
            for _ in members:
                member = choice(members)
                user2 = get_user(member[1])
                if user2[0] in no_rp_list:
                    continue
                else:
                    break  
    else:
        members = get_members(message.chat.id)
        for _ in members:
            member = choice(members)
            user2 = get_user(member[1])
            if user2[0] in no_rp_list:
                continue
            else:
                break
    
    if user2[0] == user[0]:
        chances = randint(0, 100)
        if chances < 50:
            if word.lower().endswith("а") or word.lower().endswith("a"):
                await message.reply("Прохладна!")
                return
            else:
                await message.reply("Прохладно!")
                return
    if user[8] != None and user[8] != "":
        nick = user[8]
    else:
        nick = user[2]
    
    if user2[8] != None and user2[8] != "":
        nick0_2 = user2[8]
    else:
        nick0_2 = user2[2]
    
    if user2[4] == 0:
        nick2 = morph_word(user2[0], nick0_2, user2[4])[2]
    else:
        nick2 = morph_word(user2[0], nick0_2, user2[4])[3]
    
    if user[0] == yakudza_id:
        rpword = ["делает жарко", "нагревает", "утепляет", "обжигает", "купает в лаве"]
        rpemodz = ["🦋🌡😵‍💫", "🦋☀️🕺", "🦋🧣💃", "🦋🔥👾", "🦋🌋🙀"]
    else:
        rpword = ["делает прохладно", "охлаждает", "освежает", "замораживает", "купает в проруби"]
        rpemodz = ["🧑‍💻🥶", "🧑‍💻🧊🕺", "🧑‍💻💨💃", "🧑‍💻🌪👾", "🧑‍💻🌊🙀"]
    
    action = rpword[user2[4]]
    rpemodz = rpemodz[user2[4]]
    

    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(nick)}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>", parse_mode="html")

    return
