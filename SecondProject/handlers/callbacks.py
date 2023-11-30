from aiogram import types, Router
from aiogram.fsm.context import FSMContext
import states
router = Router()

# If a user rates a profile with a like, a message is sent to the user who received the reaction.
# Processing of like and dislike callbacks is called.

@router.callback_query(lambda c: c.data == 'like')
async def handle_like(query: types.CallbackQuery, state: FSMContext) -> None:
    find_user = await state.get_data()
    find_user_id = find_user.get('find_user_id')
    await query.message.answer(f"Вот ссылка на пользователя tg://user?id={find_user_id}")
    await query.message.answer("Чтобы вернуться к профилю, нажми /myprofile 👈",)
    await state.set_state(states.MainMenu.menu)
    await query.answer()

@router.callback_query(lambda c: c.data == 'dislike')
async def handle_dislike(query: types.CallbackQuery, state: FSMContext) -> None:
    await query.message.answer("Чтобы вернуться к профилю, нажми /myprofile 👈")
    state.set_state(states.MainMenu.menu)
    await query.answer()
