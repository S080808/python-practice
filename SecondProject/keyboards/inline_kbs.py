from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# File includes all inline keyboards used in the code

def like_dislike_kb(liking_user_id):
    kb = InlineKeyboardMarkup(inline_keyboard=
        [
            [
            InlineKeyboardButton(
                text="❤️",
                callback_data=f"like:{liking_user_id}"
            ),
            InlineKeyboardButton(
                text="👎",
                callback_data=f"dislike:{liking_user_id}"
            )
            ]
        ]
    )
    return kb
