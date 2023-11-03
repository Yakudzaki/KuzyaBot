from aiogram import types
from loader import bot, dp
import random

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
    
    if callback.data == '1':
        msg1 = "Я выбрал " + rand + f"\nА <a href='tg://user?id={callback.from_user.id}'>ты</a> выбрал 🗿Камень"
        if rand == '🗿Камень':
            msg2 = "У нас ничья🤝"
        elif rand == '✂️Ножницы':
            msg2 = f"<a href='tg://user?id={callback.from_user.id}'>Ты</a> выиграл🥇"
        else:
            msg2 = "Я победил🥇"
    elif callback.data == '2':
        msg1 = "Я выбрал " + rand + f"\nА <a href='tg://user?id={callback.from_user.id}'>ты</a> выбрал ✂️Ножницы"
        if rand == '🗿Камень':
            msg2 = "Я победил🥇"
        elif rand == '✂️Ножницы':
            msg2 = "У нас ничья🤝"
        else:
            msg2 = f"<a href='tg://user?id={callback.from_user.id}'>Ты</a> победил🥇"
    elif callback.data == '3':
        msg1 = "Я выбрал " + rand + f"\nА <a href='tg://user?id={callback.from_user.id}'>ты</a> выбрал 📄Бумагу"
        if rand == '🗿Камень':
            msg2 = f"<a href='tg://user?id={callback.from_user.id}'>Ты</a> победил🥇"
        elif rand == '✂️Ножницы':
            msg2 = "Я победил🥇"
        else:
            msg2 = "У нас ничья🤝"
    
    msg = msg1 + '\n—\n' + msg2
    await callback.message.edit_text(msg)