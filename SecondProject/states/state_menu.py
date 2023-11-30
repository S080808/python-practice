from aiogram.filters.state import StatesGroup, State

class MainMenu(StatesGroup):
    menu = State()
    scrolling = State()
    deleting_profile = State()
    ask_deleting_profile = State()
    choosing_option = State()
    evaluate = State()
    waiting_for_answer = State()