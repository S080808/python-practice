from aiogram.filters.state import StatesGroup, State

class SigningUser(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_look_for = State()
    waiting_for_description = State()
    waiting_for_photo = State()