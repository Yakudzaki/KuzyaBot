from aiogram import types
from loader import dp
from utils.db.db_utils_clans import get_top_clans, get_clans_count_players
import asyncio
import random

@dp.message_handler(commands=['кланы', 'список кланов', 'топ кланов', 'clans'], commands_prefix='!?./')
async def clans_top_list(message: types.Message):
    clans_top = get_top_clans()
    msg_text = f'🔝 Топ {len(clans_top)} кланов:\n\n'

    for i, clan in enumerate(clans_top):
        players_count = get_clans_count_players(clan[0])
        money = f'{clan[4]:,}'.replace(',', '.')
        msg_text += f'{get_smail(i + 1)} {clan[1]} | {players_count} уч. | Казна: {money} кузиров.\n'
        
        # отправляем ссылку в рандомный момент времени
        if random.choice([True, False]):
            msg += "\n<a> href='https://t.me/Kuzya_News'>🗞 Канал с новостями</a>"
    
    await message.answer(msg_text, disable_web_page_preview=True)
