from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from .sign_up import ask_age
from patterns import welcome_text
from main import db
import states
router = Router()

# The /start and /editprofile commands are processed here

@router.message(Command("start"))
async def user_start(message: Message, state: FSMContext) -> None:
    if await db.user_exists(message.from_user.id):
        await state.set_state(states.MainMenu.menu)
        return
    await message.answer(
        text=welcome_text
    )
    await ask_age(message, state)

@router.message(Command("editprofile"))
async def edit_profile(message: Message, state: FSMContext) -> None:
    if db.user_exists(message.from_user.id):
        await db.delete_user(message.from_user.id)
        await state.clear()
        await ask_age(message, state)
