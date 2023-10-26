from aiogram import types
from loader import bot, dp


@dp.callback_query_handler(lambda c: c.data in ['1', '2', '3'])
async def process_callback_yes(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id != callback.message.chat.id:
        return
    
    rand = random.choice(["🗿Камень", "✂️Ножницы", "📄Бумага"])
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    if callback.data == '1':
        await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал 🗿Камень")
        if rand == '🗿Камень':
            await callback.message.answer("У нас ничья🤝")
        elif rand == '✂️Ножницы':
            await callback.message.answer("Ты выиграл🥇")
        else:
            await callback.message.answer("Я победил🥇")
    elif callback.data == '2':
        await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал ✂️Ножницы")
        if rand == '🗿Камень':
            await callback.message.answer("Я победил🥇")
        elif rand == '✂️Ножницы':
            await callback.message.answer("У нас ничья🤝")
        else:
            await callback.message.answer("Ты победил🥇")
    elif callback.data == '3':
        await callback.message.answer("Я выбрал " + rand + "\nА ты выбрал 📄Бумага")
        if rand == '🗿Камень':
            await callback.message.answer("Ты победил🥇")
        elif rand == '✂️Ножницы':
            await callback.message.answer("Я победил🥇")
        else:
            await callback.message.answer("У нас ничья🤝")
