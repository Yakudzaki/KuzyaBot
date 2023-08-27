from aiogram import types
from loader import dp
from utils.db.db_utils_clans import get_top_clans, get_clans_count_players


@dp.message_handler(commands=['кланы', 'список кланов', 'топ кланов', 'clans'], commands_prefix='!?./')
async def clans_top_list(message: types.Message):
    clans_top = get_top_clans()
    msg_text = f'Топ {len(clans_top)} кланов:\n\n'

    for i, clan in enumerate(clans_top):
        players_count = get_clans_count_players(clan[0])
        msg_text += f'{i + 1}. {clan[1]} | {players_count} уч. | Казна: {clan[4]:.} монет.\n'

    await message.answer(msg_text)
