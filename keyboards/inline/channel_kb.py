from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import kuzya_news_link

channel_btn = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подписаться', url=kuzya_news_link)
        ]
    ]
                              )
