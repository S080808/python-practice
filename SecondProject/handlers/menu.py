import time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardRemove

from keyboards.reply_kbs import menu_kb, scrolling_kb, yes_no_kb
from patterns import menu_text, not_found, liked_message
from keyboards.inline_kbs import like_dislike_kb
from main import db, bot
import states

router = Router()

# Main file with handlers

def likes(num: int) -> str:
    """
    Returns word "лайки" in a correct form
    :param num: gets number of "лайки"
    """
    if (num % 10 == 1 and num % 100 != 11):
        return "лайк"
    elif (num % 10 in [2, 3, 4] and num % 100 not in [12, 13, 14]):
        return "лайка"
    else:
        return "лайков"

async def print_profile(user: list, chat_id, reply) -> None:
    """
    Prints user's profile
    :param user: a list with user's information
    :param chat_id: id of the user to whom the profile will be sent
    :param reply: keyboard
    :return:
    """
    with open(f"pictures/{user[6]}.jpg", "rb") as buffer:
        caption = f"{user[1]}, {user[2]}"
        if len(user[5]) != 0:
            caption += f" - {user[5]}\n"
        await bot.send_photo(
            chat_id,
            BufferedInputFile(
                buffer.read(),
                filename="image"
            ),
            caption=caption,
            reply_markup=reply
        )

@router.message(Command("myprofile"), states.MainMenu.menu)
async def main_menu(message: Message) -> None:
    """
    Displays the user profile and the main menu of the chatbot.

     When invoked, this feature displays the user's profile details, including photo and number of likes received.
     The function then provides the user with a main menu for further interaction with the bot.
    """
    user = await db.get_user(message.from_user.id)
    await message.answer("Так выглядит твоя анкета")
    await print_profile(user, message.from_user.id, None)
    await message.answer(f"За всё время ты получил(a) {user[7]} {likes(user[7])} ❤️")

    await message.answer(
        text=menu_text,
        reply_markup=menu_kb()
    )


@router.message(states.MainMenu.menu, F.text == "2")
async def ask_delete_profile(message: Message, state: FSMContext) -> None:
    """
    Ask if user is sure he wants to delete his profile.
    """
    await message.answer("Ты точно хочешь удалить анкету?", reply_markup=yes_no_kb())
    await state.set_state(states.MainMenu.deleting_profile)


@router.message(states.MainMenu.deleting_profile)
async def delete_profile(message: Message, state: FSMContext):
    """
    Deleting user's profile.
    """
    if (message.text.lower() in ["да", "нет"]):
        if (message.text.lower() == "да"):
            await message.answer("Отлично, твоя анкета удалена.\nЕсли хочешь создать новую, нажми /start 👈")
            await db.delete_user(message.from_user.id)
            await state.clear()
        else:
            print("нет")
            await state.set_state(states.MainMenu.menu)
            await main_menu(message)


@router.message(states.MainMenu.menu, F.text == "1")
async def start_scrolling(message: Message, state: FSMContext):
    """
    Start of scrolling users' profiles process.
    """
    await message.answer("Начало поиска анкет 🔎")
    await state.set_state(states.MainMenu.scrolling)
    await scrolling(message, state)


@router.message(states.MainMenu.scrolling)
async def scrolling(message: Message, state: FSMContext) -> None:
    """
    Process of finding new profiles from database which match user's priorities.
    """

    time.sleep(0.5)
    find_user_id = await db.find_profiles(message.from_user.id)
    print(find_user_id)
    find_user = await db.get_user(find_user_id)
    await state.update_data(find_user_id=find_user_id)
    print(find_user)
    if (find_user_id == -1 or find_user == None):
        await message.answer(not_found)
        await message.answer("Завершение поиска анкет 💤")
        await state.set_state(states.MainMenu.menu)
        await main_menu(message)
        return
    await print_profile(find_user, message.from_user.id, scrolling_kb())
    await state.set_state(states.MainMenu.evaluate)



@router.message(states.MainMenu.evaluate)
async def reaction(message: Message, state: FSMContext) -> None:
    """
    Process of user reacting on another user's profile.
    """
    data = await state.get_data()
    find_user_id = data.get("find_user_id")
    find_user = await db.get_user(find_user_id)
    user = await db.get_user(message.from_user.id)
    if message.text == "❤️":
        await db.increment_like(find_user_id)

        await bot.send_message(find_user_id, liked_message(find_user[3]))
        await print_profile(user, find_user_id, ReplyKeyboardRemove())
        await bot.send_message(find_user_id, "Хочешь продолжить общение в лс?", reply_markup=like_dislike_kb(message.from_user.username))

        await state.set_state(states.MainMenu.scrolling)
        await scrolling(message, state)

    elif message.text == "💤":
        await state.set_state(states.MainMenu.menu)
        await message.answer("Завершение поиска анкет 💤")
        await main_menu(message)

    elif message.text == "👎":
        await state.set_state(states.MainMenu.scrolling)
        await scrolling(message, state)