from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


dev_btn = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📊 Статистика', callback_data='stat'),
            InlineKeyboardButton(text='🛑 Бан-лист', callback_data='ban-list')
        ],
        [
            InlineKeyboardButton(text='📤 Рассылка', callback_data='rass')
        ]
    ]
)
