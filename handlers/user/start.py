from loader import dp, bot
from aiogram import types
from loguru import logger
from app import server_dir
from aiogram.dispatcher.filters import CommandStart
from utils.db.db_utils_users import create_user
from utils.db.db_utils_сhats import check_chat, create_chat_with_info
from settings import legal_chats, topa_chat_invite, yakudza_url, botovod_id, helpers_ids


class CommandHandler:
    def __init__(self, dp):
        self.dp = dp

    async def start(self, message: types.Message) -> None:
        if message.chat.id not in legal_chats and message.chat.type != 'private':
            await message.answer(
                f"❌ Я создан исключительно для чата <a href='{topa_chat_invite}'>Опа Это Топа</a>!",
                parse_mode="html", disable_web_page_preview=True)
            await message.answer(
                f"Айди вашего чата: [{str(message.chat.id)}]\nДоговаривайтесь с <a href='{yakudza_url}'>создателем</a> бота.",
                parse_mode="html", disable_web_page_preview=True)

            if check_chat(message.chat.id):
                create_chat_with_info(message.chat.id, f"НЕЛЕГАЛ: {message.chat.title}, @{message.chat.username}, {message.chat.first_name}, {message.chat.last_name}")

            await bot.leave_chat(message.chat.id)
            return

        user = message.from_user
        create_user(user.id, user.username, user.first_name)
        await message.answer(f"Привет, {user.first_name}, я Кузя!\n\nИспользуй  /help что-бы ознакомиться с командами.")

    async def restart_botovod(self, message: types.Message) -> None:
        if message.from_user.id in botovod_id:
            await message.answer("Кузя идет на перезапуск!")
            from subprocess import call
            call('Kuzya restart.bat')
        else:
            await message.answer("У вас недостаточно полномочий!")

    async def logs(self, message: types.Message) -> None:
        if message.from_user.id in botovod_id:
            await bot.send_document(message.chat.id, open(server_dir + f"\logging0.log", "rb"),
                                    reply_to_message_id=message.message_id)


command_handler = CommandHandler(dp)

@dp.message_handler(CommandStart())
async def start_handler(message: types.Message) -> None:
    await command_handler.start(message)

@dp.message_handler(commands=['перезапуск', 'restart', 'рестарт'], commands_prefix="!./")
async def restart_botovod_handler(message: types.Message) -> None:
    await command_handler.restart_botovod(message)

@dp.message_handler(lambda message: message.text.lower() == "логи")
async def logs_handler(message: types.Message) -> None:
    await command_handler.logs(message)