from loader import dp, bot
from aiogram import types
from .base_text import final_text, final_any
from .base_media import *

# Хендлер видео
@dp.message_handler(content_types=['video'])
async def video_handler(message: types.Message):
    await final_video(message)

# Хендлер анимация
@dp.message_handler(content_types=['animation'])
async def animation_handler(message: types.Message):
    await final_animation(message)

# Хендлер фото
@dp.message_handler(content_types=['photo'])
async def photo_handler(message: types.Message):
    await final_photo(message)

# Хендлер стикеры
@dp.message_handler(content_types=['sticker'])
async def sticker_handler(message: types.Message):
    await final_sticker(message)

# Хендлер кругетсы
@dp.message_handler(content_types=['video_note'])
async def videonote_handler(message: types.Message):
    await final_videonote(message)

# Хендлер голос
@dp.message_handler(content_types=['voice'])
async def voice_handler(message: types.Message):
    await final_voice(message)

# Хендлер музыка
@dp.message_handler(content_types=['audio'])
async def audio_handler(message: types.Message):
    await final_audio(message)

# Хендлер игры
@dp.message_handler(content_types=['game'])
async def game_handler(message: types.Message):
    await final_game(message)

# Хендлер текст
@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message):
    stop = await final_text(message) #Если stop != None, то сообщение уже удалено…
    return

# Хендлер остальное
@dp.message_handler(content_types=['any'])
async def any_handler(message: types.Message):
    await final_any(message)

