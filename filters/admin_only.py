from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS
from loader import bot


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        user_id = message.from_user.id
        return user_id in ADMINS
    
class IsAdminCb(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user_id = call.from_user.id
        return user_id in ADMINS