from loader import dp, bot
from keyboards.inline.help_kb import buttons_osn
from aiogram import types



@dp.callback_query_handler(text='osnova')
async def osnova_help(call: types.CallbackQuery):
    await call.message.edit_text("<b>💡 Основные команды</b>\n\n"
                           "<b>— Поддерживаемые префиксы</b> - <code>/</code>, <code>!</code>, <code>.</code>\n\n"
                           "● <code>/start</code> — Запуск бота\n"
                           "● <code>!Хелп</code> или <code>/help</code> — Помощь\n\n"
                           "● <code>!Вики</code> (текст) — Поиск в Википедии\n"
                           "● <code>!Рандом</code> — Рандомная статья с Википедии\n"
                           "● <code>!Погода</code> (город) — Узнать погоду в городе\n"
                           "● <code>!Гороскоп</code> — Узнать гороскоп.\n"
                           "● <code>!Мем</code> — Показать мемчик\n"
                           "● <code>!Тян</code> — Показать аниме-тян\n"
                           "● <code>!q</code> — Сделать стикер из сообщения. (писать в ответ на чужое сообщение)\n"
                           "● <code>!Рекорд</code> (можно ответом на сообщение, а можно указать аргумент) — Текст в аудио\n", parse_mode="html", reply_markup=buttons_osn)
