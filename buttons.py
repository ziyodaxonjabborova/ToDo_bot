from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           InlineKeyboardMarkup,InlineKeyboardButton
                          )



CRUD_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Add task")],
        [KeyboardButton(text="📋 See tasks")],
        [KeyboardButton(text="✏️ Update task")],
        [KeyboardButton(text="🗑 Delete task")]
    ],
    resize_keyboard=True, 
    one_time_keyboard=False 
)


SEE_BUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 All", callback_data="see_all"),
            InlineKeyboardButton(text="🕓 Pending", callback_data="see_pending"),
            InlineKeyboardButton(text="✅ Done", callback_data="see_done")
        ]
    ]
)

BACK_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⬅️ Back")]
    ],
    resize_keyboard=True
)

UPDATE_BUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Nomi o'zgartirish", callback_data="update_name"),
            InlineKeyboardButton(text="🔄 Status o'zgartirish", callback_data="update_status")
        ],

    ]
)

