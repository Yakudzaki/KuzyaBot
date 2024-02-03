from loader import dp, bot
from handlers.user.joke import anti_flood, get_joke

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.callback_query_handler(text="closej")
async def close(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(f"{call.from_user.first_name} закрыл сообщение с шутками!")


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