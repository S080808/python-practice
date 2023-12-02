from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.reply_kbs import gender_kb, look_for_kb, only_button_kb
from .menu import main_menu
from main import bot
from main import db
import states

# File includes registration handlers

router = Router()

async def ask_age(message: Message, state: FSMContext):
    """
    Asks user for his age.
    """
    await state.update_data(id=message.from_user.id)
    await message.answer(
        "Сколько тебе лет? 🙊",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(states.SigningUser.waiting_for_age)


@router.message(states.SigningUser.waiting_for_age, F.text)
async def ask_gender(message: Message, state: FSMContext):
    """
        Asks user for his gender.
    """
    age = message.text
    await state.update_data(age=age)
    if not age.isnumeric() or not (1 <= int(age) <= 100):
        await message.answer(
            text="Пожалуйста, введи корректный возраст ❌")
        return
    await message.answer(
        "Определимся с полом 😏",
        reply_markup=gender_kb())
    await state.set_state(states.SigningUser.waiting_for_gender)


@router.message(states.SigningUser.waiting_for_gender)
async def ask_look_for(message: Message, state: FSMContext):
    """
        Asks user about who he is looking for.
    """
    gender = message.text
    if gender.lower() not in ["я парень", "я девушка"]:
        await message.answer(
            "Нет такого варианта ответа, выбери из предложенных, пожалуйста 😅",
            reply_markup=gender_kb())
        return
    if gender.lower() == "я парень":
        await state.update_data(gender="пар")
    else:
        await state.update_data(gender="дев")
    await message.answer(
        "Кто тебе интересен? 🤗",
        reply_markup=look_for_kb())
    await state.set_state(states.SigningUser.waiting_for_look_for)


@router.message(states.SigningUser.waiting_for_look_for)
async def ask_name(message: Message, state: FSMContext):
    """
        Asks user for his name.
    """
    look_for = message.text
    if look_for.lower() not in ["парни", "девушки"]:
        await message.answer(
            "Нет такого варианта ответа, выбери из предложенных, пожалуйста 😅",
            reply_markup=look_for_kb())
        return
    if look_for.lower() == "парни":
        await state.update_data(look_for="пар")
    else:
        await state.update_data(look_for="дев")
    await message.answer(
        "Придумай <b>username</b> для своей анкеты 👑",
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(states.SigningUser.waiting_for_name)


@router.message(states.SigningUser.waiting_for_name)
async def ask_description(message: Message, state: FSMContext):
    """
        Asks user for his profile description.
    """
    name = message.text
    await state.update_data(name=name)
    await message.answer("Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. Это поможет лучше подобрать тебе компанию 🤓",
                         reply_markup=only_button_kb("Пропустить"))
    await state.set_state(states.SigningUser.waiting_for_description)


@router.message(states.SigningUser.waiting_for_description, F.text)
async def ask_picture(message: Message, state: FSMContext):
    """
        Asks user for his profile picture.
    """
    description = message.text
    if description.lower() == "пропустить":
        await state.update_data(description="")
    else:
        await state.update_data(description=description)

    await message.answer("Теперь пришли свою фотографию, её будут видеть другие пользователи 🤩",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(states.SigningUser.waiting_for_photo)


@router.message(states.SigningUser.waiting_for_photo, F.photo)
async def download_photo(message: Message, state: FSMContext):
    """
        Downloads user's profile photo.
    """
    picture_id = message.photo[-1].file_id
    await state.update_data(picture_id=picture_id)
    await bot.download(
        message.photo[-1],
        destination=f"pictures/{message.photo[-1].file_id}.jpg"
    )

    user = await state.get_data()
    await db.add_user(user.get('id'), user.get('name'), user.get('age'), user.get('gender'),
                user.get('look_for'), user.get('description'), user.get('picture_id'), 0, message.from_user.username)
    print(await db.get_user(user.get('id')))

    await state.set_state(states.MainMenu.menu)

    await message.answer("Твоя анкета была успешно создана 🎉")
    await main_menu(message)

@router.message(states.SigningUser.waiting_for_photo)
async def skip_photo(message: Message):
    """
    If user's message is invalid asks him try again.
    """
    await message.answer('Пожалуйста, пришли фотографию')