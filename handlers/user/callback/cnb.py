from aiogram import types
from loader import bot, dp
import random
from utils.db.db_utils_users import *
@dp.callback_query_handler(lambda c: c.data in ['1', '2', '3'])
async def process_callback_yes(callback: types.CallbackQuery):

    for entity in callback.message.entities:
        if entity.type != "text_mention":
            await callback.answer("Это не твоя кнопка!", show_alert=True)
            return
        else:
            if entity.user.id != callback.from_user.id:
                await callback.answer("Это не твоя кнопка!", show_alert=True)
                return
    
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумагу"])
    # await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user = get_user(callback.from_user.id)
    
    role = ['👤', '👨', '👩', '👾', '😿']
    cnb_em = f"{role[user[4]]}| "
    
    role_ch = ['выбрали', 'выбрал', 'выбрала', 'выбрало', 'выбираешь']
    cnb_ch = role_ch[user[4]]
    
    role_win = ['победили', 'победил', 'победила', 'победило', 'побеждаешь']
    cnb_win = role_win[user[4]]
    
    role_me = ['Вы', 'Ты', 'Ты', 'Ты', 'Ты']
    cnb_me = role_me[user[4]]
    
    if callback.data == '1':
        msg1 = "🤖| Я выбрал " + rand + f"\n{cnb_em}А <a href='tg://user?id={callback.from_user.id}'>{cnb_me.lower()}</a> {cnb_ch} 🗿Камень"
        if rand == '🗿Камень':
            msg2 = "У нас ничья🤝"
        elif rand == '✂️Ножницы':
            msg2 = f"<a href='tg://user?id={callback.from_user.id}'>{cnb_me}</a> {cnb_win}🥇"
        else:
            msg2 = "Я победил🥇"
    elif callback.data == '2':
        msg1 = "🤖| Я выбрал " + rand + f"\n{cnb_em}А <a href='tg://user?id={callback.from_user.id}'>{cnb_me.lower()}</a> {cnb_ch} ✂️Ножницы"
        if rand == '🗿Камень':
            msg2 = "Я победил🥇"
        elif rand == '✂️Ножницы':
            msg2 = "У нас ничья🤝"
        else:
            msg2 = f"<a href='tg://user?id={callback.from_user.id}'>{cnb_me}</a> {cnb_win}🥇"
    elif callback.data == '3':
        msg1 = "🤖| Я выбрал " + rand + f"\n{cnb_em}А <a href='tg://user?id={callback.from_user.id}'>{cnb_me.lower()}</a> {cnb_ch} 📄Бумагу"
        if rand == '🗿Камень':
            msg2 = f"<a href='tg://user?id={callback.from_user.id}'>{cnb_me}</a> {cnb_win}🥇"
        elif rand == '✂️Ножницы':
            msg2 = "Я победил🥇"
        else:
            msg2 = "У нас ничья🤝"
    msg2 = "⚔️| " + msg2
    msg = msg1 + '\n—\n' + msg2
    await callback.message.edit_text(msg)