from aiogram import types
from loader import dp
from utils.db.db_utils_clans import get_top_clans, get_clans_count_players

@dp.message_handler(commands=['кланы', 'список кланов', 'топ кланов', 'clans'], commands_prefix='!?./')
async def clans_top_list(message: types.Message):
    clans_top = get_top_clans()
    msg_text = f'🔝 Топ {len(clans_top)} кланов:\n\n'

    for i, clan in enumerate(clans_top):
        players_count = get_clans_count_players(clan[0])
        money = f'{clan[4]:,}'.replace(',', '.')
        if i < 3:
            msg_text += f'{get_place_emoji(i + 1)}. {clan[1]} | {players_count} уч. | Казна: {money} монет.\n'
        else:
            msg_text += f'{i + 1}. {clan[1]} | {players_count} уч. | Казна: {money} монет.\n'

    await message.answer(msg_text)

def get_place_emoji(place):
    if place == 1:
        return "1⃣"
    elif place == 2:
        return "2⃣"
    elif place == 3:
        return "3⃣"
    else:
        return place
