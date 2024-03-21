from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram import Bot, Dispatcher, executor, types
import hmtai
import asyncio
from loader import dp, bot

WORD_MAP = {
    'Анал': 'anal',
    'Жопа': 'ass',
    'БДСМ': 'bdsm',
    'Кам': 'cum',
    'Классика': 'classic',
    'Кремпай': 'creampie',
    'Манга': 'manga',
    'Хентай': 'hentai',
    'Инцест': 'incest',
    'Мастурбация': 'masturbation',
    'Публично': 'public',
    'Оргия': 'orgy',
    'Куколд': 'cuckold',
    'Эротика': 'ero',
    'Юри': 'yuri',
    'Тентакли': 'tentacles',
    'Неко': 'nsfwNeko',
    'Обои': 'nsfwMobileWallpaper'
}

eng = {}
CLEAR_INTERVAL_SECONDS = 3600

async def clear_dictionary():
    while True:
        await asyncio.sleep(CLEAR_INTERVAL_SECONDS)
        eng.clear()
        print("Словарь eng был очищен.")


def generate_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    for russian_word, english_word in WORD_MAP.items():
        keyboard.insert(InlineKeyboardButton(text=russian_word, callback_data=f"pic_{english_word}"))
    return keyboard


def update_kb(id):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='Обновить', callback_data=f'refresh_{eng[id]}'))
    return kb



@dp.message_handler(commands=['search', 'хенпоиск'], commands_prefix="/!.")
async def search_pics(message: types.Message):
    if message.chat.type != 'private':
        await message.reply("Эта команда доступна только в личных сообщениях!")
        return
    
    user_text = message.text.lower().split(' ', 1)[-1]
    for russian_word, english_word in WORD_MAP.items():
        if russian_word.lower() == user_text.lower():
            hentai_photo_url = hmtai.get("hmtai", english_word)
            eng[message.message_id] = english_word
            await bot.send_photo(message.from_user.id, photo=hentai_photo_url, reply_markup=update_kb(message.message_id))
            break
    else:
        await message.reply("Категория не найдена.")


@dp.message_handler(commands=['hentai', 'хентай', 'хентыч'], commands_prefix="/!.")
async def search_command(message: types.Message):
    if message.chat.type != 'private':
        await message.reply("Эта команда доступна только в личных сообщениях!")
        return
    await message.reply("Выберите категорию: \n\n(Тем самым, подтвердив, что вам уже есть восемнадцать лет, и взяв всю ответственность на себя)", reply_markup=generate_inline_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('pic_'))
async def update_picture(callback_query: types.CallbackQuery):
    _, category = callback_query.data.split('_', 1)
    eng[callback_query.message.message_id] = category
    hentai_photo_url = hmtai.get("hmtai", category)
    await bot.send_photo(callback_query.from_user.id, photo=hentai_photo_url, reply_markup=update_kb(callback_query.message.message_id))
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('refresh_'))
async def refresh_picture(callback_query: types.CallbackQuery):
    _, category = callback_query.data.split('_', 1)
    hentai_photo_url = hmtai.get("hmtai", category)
    eng[callback_query.message.message_id] = category
    try:
        await bot.edit_message_media(types.InputMediaPhoto(hentai_photo_url), callback_query.from_user.id, callback_query.message.message_id)
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=update_kb(callback_query.message.message_id))
        await bot.answer_callback_query(callback_query.id)
    except Exception as e:
        await callback_query.message.answer(f"Ошибка обновления")
