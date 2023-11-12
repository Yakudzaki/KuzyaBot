from loader import dp, bot
from handlers.user.meme import anti_flood

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputMediaPhoto

from random import randint, choice
import aiohttp
from bs4 import BeautifulSoup


@dp.callback_query_handler(text="close")
async def close(call: types.CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(text="update")

@dp.throttled(anti_flood,rate=2)

async def update(call: types.CallbackQuery):

    try:
        random_site = randint(1, 2857)

        url = f"https://www.memify.ru/memes/{random_site}"

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                content = await response.text()

                soup = BeautifulSoup(content, "html.parser")

                items = soup.find_all("div", {"class": "infinite-item card"})

                random_item = choice(items)

                second_a = random_item.find_all("a")[1]

                keyboard = types.InlineKeyboardMarkup()

                buttons = [

                    types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update")

                ]

                keyboard.add(*buttons)

                await call.message.edit_media(InputMediaPhoto(second_a.get("href")))
                await call.message.edit_caption(f"Обновлено", reply_markup=keyboard)

    except Exception as e:

        print(e)