from aiogram import Dispatcher

from .admin_only import IsAdmin, IsAdminCb


# Функция которая выполняет установку кастомных фильтров
def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsAdminCb)
