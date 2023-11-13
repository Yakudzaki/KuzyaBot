reprekl = 10 #Уровень репутации юзера, выше которой, он может постить спорные сообщения.
time_del = 300 #Время, в секундах, после истечения которого, Кузя будет удалять многие свои сообщения. (0 - удаление отключено)

rep_converg_g = 5 #(0-11)Затруднение для сближения показателей репутации (плюсы от старших к младшим) (11 - полный блок)
rep_separat_g = 2 #(0-11)Затруднение для разделения показателей репутации (плюс от младших к старшим) (11 - полный блок)

rep_converg_b = 5 #(0-11)Затруднение для сближения показателей репутации (минусы от младших к старшим) (11 - полный блок)
rep_separat_b = 2 #(0-11)Затруднение для разделения показателей репутации (минусы от старших к младшим) (11 - полный блок)

hide_ver = [1,1,0,0] #Шансы что оповещение о повышении репутации будет спрятано. 0 - не будет спрятно, 1 - будет спрятано.

adminmatnote = 50 #Уровень шанса антимата, выше которого админы не получают сообщения о своём мате. (если 0 - никогда || если 100 - всегда || 50 - если шанс антимата в чате выше 50, то админы могут свободно материться)

admins = [5548351085, 1069481559, 979139697, 556640068, 1002807451, 564097497, 1381205848] #Админы целевого чата. (не знаю зачем оно было, но сохранил)

mutbase = 3 #Базовое значение мута рулетки в минутах. (Не рекомендуется ставить меньше 2) 
mutrouldop = 3 #Приращение мута в минутах с каждым выигрышем в рулетку.
chances_roul = 10 #Шанс в процентах, проиграть в рулетку. Базисный, с ним сравнвается итог, после расчетов влияния зарядов.
chances_roul_cor = 10 #Влияние холостых выстрелов на шансы в рулетке.
chances_limit = 60 #Начальное значение максимальных шансов, с каждым холостым выстрелом убывает на [chances_roul_cor]
wait_roul = 360 #Через сколько секунд Кузя зачистит чат от сообщений рулетки

chances_roul_str = "? / ?" #Описание шансов рулетки для меню .help

mut_cor_minlim = 2 #Минимальная длительность мута в минутах при игре в коробку. (Не рекомендуется ставить меньше 2)
mut_cor_maxlim = 18 #Максимальная длительность мута в минутах при игре в коробку.
chances_cor = [0,1] #Вероятности при игре в коробку. (1 - смерть! 0 - жизнь!)
chances_cor_str = "1 / 2" #Описание шансов для меню .help
wait_cor = 360 #Через сколько секунд Кузя зачистит чат от сообщений коробки
logal_chat = -1001973433579
legal_chats = [-1001499340172, -1002052062710, -1001933008358, -1001983864862, -1001552627374, -1001748129974, logal_chat, -1001943077906, -1001942334732] #Разрешенные чаты (-1002052062710 - КузяЧат), ( -1001933008358 - СКС)  (1001499340172 - ОэТ) ( -1001983864862 - Чат Хуя Ебланыча, -1001552627374 Чат ПивоМена, -1001748129974 - Мафия Гудмана, -1001973433579 - лог) 


yakudza_id = 5542378501 #Айди главного разраба.
yakudza_url = "https://t.me/Yakudza_Drill" #Ссылка на профиль главного разработчика
botik_id = 6554535982 # Айди этого ботика, для корректной работы должно соответствовать истине.
botik_username = "@KuzyaRobot"


botovod_id = [5759932615, yakudza_id, 5730177063] #айди ботоводов, и VIP.
kuzya_news_id = -1001809772196 # Айди канала новостей про Кузю.
kuzya_news = "KuzyaDev"
kuzya_news_link = f"https://t.me/{kuzya_news}"
kuzya_news_name = f"@{kuzya_news}"
helpers_ids = [5246100940, 1644643904, 556640068, 979139697, 1002807451, 1069481559] #Айдишники тех, кому можно делать перезапуск в случае чего.



topa_chat_id = -1001499340172 #Айди чата Топы.
topa_chat_rules = "https://t.me/c/1499340172/2255554" #Ссылка на сообщение с правилами чата в чате Топы.
topa_chat_invite = "https://t.me/+X185wlT3u1s1MmRi" # Пригласительная ссылка в чат Топы.
topa_username = "topatella" #Исключается из команды вызова админов. Используется в admins.py и shield.py.
topa_id = 249620355 #Айди Самого ТОПЫ. Инопришеленца, Евгения Попадинца.




whitelist = [777000, 136817688, 1087968824, botik_id,  topa_chat_id, yakudza_id, topa_id, kuzya_news_id] #Список айди, которым всегда можно постить рекламу. И от кого можно репостить рекламу. 777000 - телеграм, 136817688 - Канал-бот, 1087968824 - анонимный админ-бот.

no_rp_list = [777000, 136817688, 1087968824, topa_id] #Список айди, на которых не работают РП и вообще.

member_add = True #Добавлять ли при каждом сообщении в чате(которое не ответ на сообщение) юзера из базы кузи, в список членов чата (мемберы). True - добавлять, False - не добавлять.
user_add = False #Добавлять ли при каждом сообщении в чате(которое не ответ на сообщение) человека, как в базу юзеров, так и в базу мемберов. True - добавлять, False - не добавлять.
goodbye = True #Включить (True) или выключить (False) усиленное прощание, даже если телега не пишет сообщение об уходе чела из чата.



message_transfer_id = 0
reply_transfer = 0

text_name = ""
text_id = 0

reps_user_id = 0

kuzer1 = 0
kuzer2 = 0