from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)

# File includes all reply keyboards used in the code

def yes_no_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="да"),
                KeyboardButton(text="нет")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    return kb

def menu_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1"),
                KeyboardButton(text="2"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    return kb

def gender_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Я парень"),
                KeyboardButton(text="Я девушка")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    return kb

def look_for_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Парни"),
                KeyboardButton(text="Девушки")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    return kb

def scrolling_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❤️"),
                KeyboardButton(text="👎"),
                KeyboardButton(text="💤")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    return kb

def only_button_kb(text: str):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=text)
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    return kb
