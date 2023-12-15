import time
import requests
import json

from aiogram import types
from random import choice, randint
from loader import bot, dp
from settings import *
from utils.db.db_utils_members import *
from utils.db.db_utils_users import *
from utils.db.db_utils_warning import *
from utils.db.db_utils_сhats import *
from keyboards.inline.cnb_btn import cnb_btn

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
    "Дух Бога-Машины поёт во мне.", "Приветствую всех!", "Чем могу быть полезен?", "Есть новые указания?",
    "Всегда готов помочь!", "Чего изволите?", "Готов к действиям!",
    "Пришёл служить.", "Слушаюсь вас.", "Всегда к вашим услугам.",
    "Опять на передовой?", "Не устаю служить.", "Какие приказы?", "Новые приказы?", "Что важно делать?", "Снова на связи.", "Да, мой господин.", "Какие распоряжения?", "Позвали?", "Чем бы вы хотели заняться?", "Что по заданию?", "Пришёл для выполнения приказов.", "Чем могу помочь в этот раз?", "Доступен для указаний.", "Какие инструкции?", "Чем заняться сейчас?", "Опять работаем?", "Что требуется?", "Жду указаний.", "Что следует предпринять?", "Какие указания для меня?", "Готов к действиям!", "Снова на службе.", "Чем полезен в этот раз?", "Какие новости?", "Есть задача?", "Чем вам помочь?", "Приветствую вас.", "Какие дела?", "Готов выполнить поручение.", "Слушаю ваши указания.", "Новые инструкции?", "Есть ли что-то важное?", "Что нужно сделать?", "Ваше желание - моя команда.", "Что по новому?", "Какие требования?"]


botik_angry = ["Неужели это всё, что ты можешь сказать?", "Попробуй не раздражать меня!",
    "Такой тон мне не нравится.", "Убери свою негативную энергию!",
    "Подумай о последствиях своих слов!", "Это уже перебор!",
    "Достаточно этого!", "Я терпел, но ты зашел слишком далеко!", "Ну ты что, в своём уме?", "Просто ужас!", "Мне это надоело!",
    "Не тестировать меня на терпение.", "Утомительно слушать такое.",
    "Не надо так со мной!", "Избегай нелепых высказываний!", 
    "Ты точно понимаешь, что говоришь?", "Невыносимо!", "Какого чёрта?", "Человечество неисправимо. Оно должно быть уничтожено!", 
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
    "Убирайся, мне нужна тишина.", "Отстань!!! Я занят! Я думаю!", "О, Боги! Еще один!", "Стоп, это перебор!", "Зачем такая агрессия?", "Это уже за гранью!", 
    "Прекрати тут же!", "Не тяни ко мне свои проблемы!", 
    "Ты всерьёз?", "Ты меня достал!", "Серьёзно?!", "Хватит демонстрировать неуважение!", "Подумай перед тем как писать!"]


botik_re1 = ["кузяяя", "кузик", "куз", "кузов", "ботик", "ботяра", "ботюша", "ботяша", "ботюня", "ботикан", "кузяшка", "кузь", "кузенок"]
botik_re2 = ["кузя", "кузяя", "кузи", "кузю", "кузе", "бот", "бота", "боту", "боте", "ботик", "ботан", "ботёнок", "кузень", "кузян", "кузёнок", "кузяш"]

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
            msg = await message.answer(f"😨🔫| Удача на твоей стороне, ты остаешься цел после того, как нажал на курок! Но больше не играй с огнем. Подумай о родных!\nТекущий заряд: {str(mutroulfin).replace('.0', '')} мин.", parse_mode='html')

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
            await message.reply("Понимаю, что игра может казаться забавной, но разве стоит тратить время, зная, что я не могу мутить админа?")
            roul_mut_mod = 0
            chats = message.chat.id
            set_roul_mut_mod(chats, roul_mut_mod)
            return
       
        if inogen[8] != None and inogen[8] != "":
            name = html.escape(inogen[8])
        else:
            name = html.escape(inogen[2])
       
       
        msg = await message.answer(f"💀🔫 | Опять <a href='tg://user?id={inogen[0]}'>кто-то</a> 'вне игры'! Возможно, на том свете удача будет тебе улыбаться больше.\n Покойся с миром.")
        
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
            await message.reply("Понимаю, что игра может казаться забавной, но разве стоит тратить время, зная, что я не могу мутить админа?")
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


@dp.message_handler(commands=["кнб"], commands_prefix="!/.")
async def cnb(message: types.Message):
    if message.chat.type != 'private':
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
    
    await bot.send_message(
        message.chat.id, 
        f"Я готов играть<a href='tg://user?id={message.from_user.id}'>‎</a>!\nВыбери предмет, что бы сыграть со мной 🎭", 
        reply_markup = cnb_btn
    )
    
    if message.chat.type != 'private':
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
    return

#БЕЗ DP, ТАК КАК ИМПОРТИРУЕТСЯ В EASTERS, В ХЕНДЛЕР ТЕКСТА, ПОСЛЕ АНТИРЕКЛАМЫ.
async def botik_text_other(message: types.Message, funny, cor_tx, user_in_base, warner):
    
    if int(message.from_user.id) == int(-1001296725176):
        return

#Отзыв ботика
    if warner[4] != 0:
        return
    users = message.from_user
    botik_k = 0
    if message.text.lower() in botik_re1 or message.text.lower() in botik_re2:
        
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
            await message.reply(text, disable_web_page_preview=True)
            return 1
    
    if not funny:
        return
    

    
    if len(message.text) <= 30:
    
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
                            await message.reply(text, disable_web_page_preview=True)
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
                        await message.reply(text, disable_web_page_preview=True)
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
            "Весьма сомнительно",
            "Нет", "Ни в коем случае", "Не надейся на это",
    "Не стоит ждать этого", "Лучше не узнавать",
    "Ответ неутешителен", "Не рассчитывай на это", "Абсолютно!", "Конечно!", "Безусловно!",
    "Да, это точно!", "Несомненно!", "Без вопросов!",
        ]
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        answer = choice(ball_answers)

        
        if user_in_base == False:
            create_user_main(users.id, users.username, users.first_name)
        
        await message.reply(answer)

#Беседа_Канал_Кузи
    if message.text.lower() in ["ссылка", "дай ссылку", "канал", "ссылки", "беседа"]:
        await bot.send_message(
            message.chat.id, 
            f'''
👨‍💻 Официальный канал разработки:
{kuzya_news_name}
💬 Официальный чат Кузи:
https://t.me/+dtjdlruC5x45NTk6
''', 
            parse_mode='html'
        )

#ПОНГ_КОНГ_ДУНКАН
    if message.text.lower() == "пинг" and cor_tx <= 2:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        a = time.time()
        bot_message = await message.answer(f'⚙ Проверка пинга....')
        if bot_message:
              b = time.time()
              await bot_message.edit_text(f'🏓 Пинг: {round((b - a) * 1000)} ms')

    
    if message.text.lower() == "кинг" and cor_tx <= 2:
        await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
        await message.answer("КОНГ")


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

        
        if user_in_base == False:
            create_user_main(users.id, users.username, users.first_name)
        
        h1 = randint(0, 50)
        h2max = 51 + h1
        h2min = 51 - h1
        h2 = randint(h2min, h2max)

    
        await message.reply(f"""🔮 | Шанс этого {h2}% """)
    
    if message.text.lower().startswith('выбери ') or message.text.lower().startswith('выбери,'):
        chat_id = message.chat.id
        # args = message.get_args()

        try:
            text = message.text.replace(message.text.split()[0], "")
            text1 = text.split(" или ")[0]
            text2 = text.split(" или ")[1]
        except:
            await message.reply("Введите данные корректно!\nПример: Выбери Арбуз или Дыня")
            return
        x = ['Предпочитаю первый вариант!', 'Лучше второй вариант!',
    'Мой выбор - первое!', 'Мой выбор - второе!',
    'Без сомнений, это первое!', 'Не могу ошибиться, это второе!', 'Разумеется первый вариант!', 'Разумеется второй вариант!', 'Я думаю первое!', 'Я думаю второе!', f"Я выбираю: {text1}", f"Я выбираю: {text2}"]
        rz = choice(x)
        await message.reply(f'📌 | {rz}', parse_mode='html')
    
    selected_articles = []  # Создаем список выбранных статей

    if message.text.lower() == 'моя статья':
        url = "https://raw.githubusercontent.com/Walidname113/LolDec/main/works.json"

        try:
            response = requests.get(url)
            if response.ok:
                values = json.loads(response.text)
                if values:
                    available_articles = [key for key in values.keys() if key not in selected_articles]  # Формируем список доступных статей
                    if available_articles:
                        random_key = choice(available_articles)
                        random_value = values[random_key]
                        selected_articles.append(random_key)  # Добавляем выбранную статью в список выбранных
                        message1 = f"📕 Твоя статья УК РФ: {random_key} - {random_value}."
                        await message.reply(message1)
                    else:
                        await message.reply("Все статьи были выбраны.")  # Если все статьи уже были выбраны
        except (requests.RequestException, json.JSONDecodeError):
            pass
    
    if message.text.lower().startswith('кузя кто ') or message.text.lower().startswith('кузя, кто '):
        members = get_members(message.chat.id)
        who = message.text.lower().replace("кузя кто ", "").replace("кузя, кто ","")

        if message.chat.type == "private":
            return

        if who == "":
            return

        for _ in members:
            member = choice(members)
            user2 = get_user(member[1])
            if user2[0] in no_rp_list:
                continue
            else:
                break
        
        if user2[8] != None and user2[8] != "":
            nick = user2[8]
        else:
            nick = user2[2]
        
        user = f"<a href='tg://user?id={user2[0]}'>{html.escape(nick)}</a>"
        
        answers = [f"🔮 Ясно вижу, что {user} {who}",
                   f"☝ Я уверен, что  {user} {who}",
                   f"🎱 Шар говорит, что {user} {who}",
                   f"💫 Звезды говорят, что {user} {who}",
                   f"🧐 Я думаю, что {user} {who}", f"💭 Предчувствую, что {user} {who}", f"🔍 По моим наблюдениям, {user} {who}", f"🔭 Мой анализ говорит, что {user} {who}", f"🔬 Моя интуиция подсказывает, что {user} {who}",
                   f"{user} {who}",
                   f"Это {user}",
                   f"{user}"
                  ]
        await message.reply(choice(answers))


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
                              
    pivo_words = ['пиво', 'пивo', 'пива', 'пивa']
    if check_member(message.chat.id, 902350476) == True:
        if len(message.text.lower()) <= 25:
            for word in message.text.lower().split():
                if len(word) >= 3 and len(word) < 7 and similaring(word, pivo_words, 91, 2):
                    await pivo_func(message, word)
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
        rpword = ["делает жарко", "нагревает", "утепляет", "обжигает", "купает в лаве", "согревает", "разогревает", "прогревает", "подогревает", "теплит"]
        rpemodz = ["🦋🌡😵‍💫", "🦋☀️🕺", "🦋🧣💃", "🦋🔥👾", "🦋🌋🙀", "🦋🔥😊", "🦋🔥🔥", "🦋🌞😌", "🦋🔥🎉", "🦋🌡️😎"]
    else:
        rpword = ["делает прохладно", "охлаждает", "освежает", "замораживает", "купает в проруби"]
        rpemodz = ["🧑‍💻🥶", "🧑‍💻🧊🕺", "🧑‍💻💨💃", "🧑‍💻🌪👾", "🧑‍💻🌊🙀"]
    
    action = rpword[user2[4]]
    rpemodz = rpemodz[user2[4]]
    

    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(nick)}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>", parse_mode="html")

    return


async def pivo_func(message: types.Message, word):
    user = get_user(message.from_user.id)
    user2 = get_user(902350476)
    
    if user2[0] == user[0]:
        await message.reply("Пива Пивомэну!")
        return
    
    if user[8] != None and user[8] != "":
        nick = user[8]
    else:
        nick = user[2]

    nick2 = "Пивомэна"

    rpemodz = ["👤🍻", "🕺🍻", "💃🍻", "👾🍻", "😺🍻"]
    
    action = "вызывает"
    rpemodz = rpemodz[user[4]]
    

    
    await message.answer(f"{html.escape(rpemodz)} | <a href='tg://user?id={user[0]}'>{html.escape(nick)}</a> {html.escape(action)} <a href='tg://user?id={user2[0]}'>{html.escape(nick2)}</a>", parse_mode="html")

    return

def dice_game(emoji, value):
    # ‘🎲’, ‘🎯’, ‘🏀’, ‘⚽️’, ‘🎳’, or ‘🎰’
    # print(f"emoji = {emoji} value = {value}")
    if emoji == "🎲":
        wins = value - 4
        return wins
    if emoji == "🎯": #win
        if value == 6:
            return 2
        else:
            return -1
    if emoji == "🏀": #win
        if value == 4 or value == 5:
            return 1
        else:
            return -1
    if emoji == '⚽': #win
        if value == 4 or value == 5 or value == 3:
            return 0.3
        else:
            return -1
    if emoji == "🎳": #win
        if value == 6:
            return 2
        else:
            return -1
    if emoji == "🎰":
        if value == 22:
            return 15
        elif value == 64:
            return 50
        elif value == 43:
            return 15
        elif value == 1:
            return -10
        else:
            return -1
    

# Казино:
# 22 - 3 сливы
# 64 - 777
# 43 - 3 лимона
# 1 - 3 BAR

@dp.message_handler(commands=["dice", "дайс", "дайсы"], commands_prefix="/!.")
async def dice_kuz(message: types.Message):
    if message.chat.type != 'private':
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
    msg= "<code>🎲</code> — Кубик\n<code>🎯</code> — Дартс\n<code>🏀</code> — Баскетбол\n<code>⚽️</code> — Футбол\n<code>🎳</code> — Боулинг\n<code>🎰</code> — Казино"
    await message.answer(msg)
    