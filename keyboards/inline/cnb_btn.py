from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cnb_btn = InlineKeyboardMarkup(row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🗿 Камень', callback_data='1'),
            InlineKeyboardButton(text='✂️ Ножницы', callback_data='2'),
            InlineKeyboardButton(text='🧻 Бумага', callback_data='3')
        ]
    ]
                              )
