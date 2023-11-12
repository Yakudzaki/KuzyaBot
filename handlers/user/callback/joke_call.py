from loader import dp, bot
from handlers.user.joke import anti_flood, get_joke

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from random import randint, choice


@dp.callback_query_handler(text="closej")
async def close(call: types.CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(text="updatej")

@dp.throttled(anti_flood,rate=2)

async def update(call: types.CallbackQuery):
    text = await get_joke()
    keyboard = InlineKeyboardMarkup()

    buttons = [
                    InlineKeyboardButton(text="🔄 Обновить", callback_data="updatej"),
                    InlineKeyboardButton(text="🔻 Закрыть", callback_data="closej")
                ]

                keyboard.add(*buttons)

                await call.message.edit_text(text, reply_markup=keyboard)