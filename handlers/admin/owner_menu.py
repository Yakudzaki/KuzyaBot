from aiogram import types
from loader import dp, bot
from settings import botovod_id, legal_chats
from keyboards.inline.dev_kb import dev_btn



@dp.message_handler(commands=["!дев", "!dev"], private=True)
async def dev_handler(message: types.Message):
	user = message.from_user.id
	
	if user not in botovod_id:
		await message.answer("Чёрт! Ты меня взломал :(")
		return
	
	else:
		await message.answer("Добро пожаловать в меню разработчика", reply_markup=dev_btn)
