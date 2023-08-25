from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


buttons = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💡 Основное', callback_data='osnova'),
            InlineKeyboardButton(text='👾 Триггеры', callback_data='funny')
        ],
        [
            InlineKeyboardButton(text='👮 Модерация', callback_data='moder')
        ]
    ]
)

buttons_fun = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💡 Основное', callback_data='osnova')
        ],
        [
            InlineKeyboardButton(text='👮 Модерация', callback_data='moder')
        ]
    ]
)

buttons_osn = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👾 Триггеры', callback_data='funny')
        ],
        [
            InlineKeyboardButton(text='👮 Модерация', callback_data='moder')
        ]
    ]
)

buttons_mod = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💡 Основное', callback_data='osnova')
        ],
        [
            InlineKeyboardButton(text='👾 Триггеры', callback_data='funny')
        ]
    ]
)