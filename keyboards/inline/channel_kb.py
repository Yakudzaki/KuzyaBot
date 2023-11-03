from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


channel_btn = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подписаться', url='https://t.me/KuzyaBotNews')
        ]
    ]
                              )
