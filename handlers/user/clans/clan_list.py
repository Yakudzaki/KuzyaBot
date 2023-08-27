from aiogram import types
from loader import dp
from utils.db.db_utils_clans import get_top_clans


@dp.message_handler(commands=['кланы', 'список кланов', 'топ кланов', 'clans'], commands_prefix='!?./')
async def clans_top_list(message: types.Message):
    clans_top = get_top_clans()
    msg_text = 'Топ 10 кланов:\n\n'

    for i, clan in enumerate(clans_top):
        msg_text += f'{i+1}. {clan[1]} | Казна: {clan[4]} монет.\n'

    await message.answer(msg_text)
