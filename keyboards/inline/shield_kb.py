from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


shield_btn = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отключить', callback_data="shield_0")
        ],
        [
            InlineKeyboardButton(text='Антиреклама', callback_data="shield_1")
        ],
        [
            InlineKeyboardButton(text='Антиреклама и Антибот', callback_data="shield_2")
        ]
    ]
)