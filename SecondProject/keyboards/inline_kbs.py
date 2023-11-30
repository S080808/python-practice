from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# File includes all inline keyboards used in the code

def like_dislike_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=
        [
            [
            InlineKeyboardButton(
                text="❤️",
                callback_data="like"
            ),
            InlineKeyboardButton(
                text="👎",
                callback_data="dislike"
            )
            ]
        ]
    )
    return kb
