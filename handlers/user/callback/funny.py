from loader import dp, bot
from keyboards.inline.help_kb import buttons_fun
from aiogram import types
from settings import *


@dp.callback_query_handler(text='funny')
async def funny_help(call: types.CallbackQuery):
    await call.message.edit_text("<b>👾 Триггеры</b>\n\n"
                           "<b>— Поддерживаемые префиксы</b> — <code>/</code>, <code>!</code>, <code>.</code>\n\n"

                           f"▷ <code>!рулетка</code> — Сыграть в рулетку ({chances_roul_str}). (Проигрыш = мут на {str(mutbase)} мин. Растет при выигрышах на {str(mutrouldop)} мин.)\n"
                           f"▷ <code>!коробка</code> — Кот Шрёдингера ({chances_cor_str}). (Котик мёртв = мут на ({str(mut_cor_minlim)} - {str(mut_cor_maxlim)}) мин.)\n"
                           "▷ <code>!кнб</code> — Сыграть в камень ножницы бумагу с Кузей.\n\n"
                           "▷ <code>!say</code> или <code>!Скажи</code> (текст или ответ на сообщение которое должен сказать бот) — Бот напишет указанный текст.\n"
                           "▷ <code>!Шутка</code> — Бот отправит шутку :)\n\n"

                           "▷ <code>!username</code> — обновить свой username в базе Кузи.\n"
                           "▷ <code>+Ник</code> (ник) — Указать ник.\n"
                           "▷ <code>+Ты</code> (клика) — Указать прозвище собеседнику.\n"

                           "▷ <code>+Вид</code> (текст) — Указать вид.\n"
                           "▷ <code>+Возраст</code> (число) — Указать возраст.\n"
                           "▷ <code>+Пол</code> (0-2) — Установить свой пол в базе Кузи. (0 - засекречено; 1 - парень; 2 - девушка)\n"
                           "▷ <code>+Био</code> (текст) — Указать био.\n"
                           "▷ <code>+Био html: </code>(текст) — Указать био, с учетом html, (после двоеточия нужен пробел).\n\n"

                           "▷ <code>!Рп</code> (действие) — Выполняется действие над юзером, на чье сообщение был сделан ответ с указанным действием.\n"
                           "▷ <code>!Список рп</code> — Запросить список фиксированных РП-команд.\n\n"   

                           "▷ <code>!Мануал рп</code> — Запросить подробную инструкцию для РП-команд.\n\n" 

                           "▷ <code>Профиль</code> — Показать профиль.\n"
                           "▷ <code>Ник</code> — Посмотреть пддробно свой ник и команды для падежей.\n"
                           "▷ <code>Прозвища</code> — Посмотреть все прозвища у себя или у собеседника, если отправить команду в ответ на его сообщение.\n"
                           "▷ <code>Прозвище</code> — Раскладка по падежам своего основного прозвища. И команды.\n"
                           "▷ <code>Био</code> — Посмотреть своё био.\n"
                           "▷ <code>Пол</code> — Узнать свой пол.\n"
                           "▷ <code>Возраст</code> — Узнать свой возраст.\n"
                           "▷ <code>Вид</code> — Узнать свой вид.\n\n"

                           "▷ <code>Отношения</code> — Узнать своё реальное семейное положение. Если написать в ответ на чужое сообщение, то Кузя расскажет уже не про вас.\n"
                           "▷ <code>!ЗАГС</code> — Узнать команды для изменения своего семейного положения.\n\n"

                           "▷ <code>Бот</code> или <code>Кузя</code> — Проверить работоспособность бота.\n"
                           "▷ <code>Шар</code> (вопрос) — Отвечает на ваш вопрос ответом 'да' или 'нет'.\n"
                           "▷ <code>Шанс</code> — показывает вероятность события, указанного в предложении.\n", parse_mode="html", reply_markup=buttons_fun)
