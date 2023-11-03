from aiogram import types
from loader import bot, dp
import random

@dp.callback_query_handler(lambda c: c.data in ['1', '2', '3'])
async def process_callback_yes(callback: types.CallbackQuery):

    for entity in callback.message.entities:
        if entity.type != "text_mention":
            await callback.message.answer("Это не твоя кнопка!", show_alert=True)
            return
        else:
            if entity.user.id != callback.from_user.id:
                await callback.message.answer("Это не твоя кнопка!", show_alert=True)
                return
    
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумагу"])
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    if callback.data == '1':
        await callback.message.answer("Я выбрал " + rand + f"\nА <a href='tg://user?id={callback.from_user.id}'>ты</a> выбрал 🗿Камень")
        if rand == '🗿Камень':
            await callback.message.answer("У нас ничья🤝")
        elif rand == '✂️Ножницы':
            await callback.message.answer(f"<a href='tg://user?id={callback.from_user.id}'>Ты</a> выиграл🥇")
        else:
            await callback.message.answer("Я победил🥇")
    elif callback.data == '2':
        await callback.message.answer("Я выбрал " + rand + f"\nА <a href='tg://user?id={callback.from_user.id}'>ты</a> выбрал ✂️Ножницы")
        if rand == '🗿Камень':
            await callback.message.answer("Я победил🥇")
        elif rand == '✂️Ножницы':
            await callback.message.answer("У нас ничья🤝")
        else:
            await callback.message.answer(f"<a href='tg://user?id={callback.from_user.id}'>Ты</a> победил🥇")
    elif callback.data == '3':
        await callback.message.answer("Я выбрал " + rand + f"\nА <a href='tg://user?id={callback.from_user.id}'>ты</a> выбрал 📄Бумагу")
        if rand == '🗿Камень':
            await callback.message.answer(f"<a href='tg://user?id={callback.from_user.id}'>Ты</a> победил🥇")
        elif rand == '✂️Ножницы':
            await callback.message.answer("Я победил🥇")
        else:
            await callback.message.answer("У нас ничья🤝")
