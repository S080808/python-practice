from functions import *
from config import *
import keyboard
import db
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import logging
from random import choice
import asyncio

# ####
# Callbackdata codes:
# kp_ =  send film info by kinopoisk id 
# sf_ = send simmilar films by kinopoisk id
# mark_ = add to favourites list
# unmark_ = delete from favoutites 
# ####



async def check_sub(uid:int):
	user_channel_status = await bot.get_chat_member(chat_id=f'@{channel_id}', user_id=uid)
	return [True if user_channel_status['status'] != 'left' else False][0]

async def check_good(message, uid): #Проверка на бан и подписку одновременно
	if await check_sub(uid):
		if check_ban(uid):
			return True
		else:
			await message.answer('К сожалению, вы забанены', reply_markup=types.ReplyKeyboardRemove())
			#change_state(uid, None) ?????
			return False
	else:
		await message.answer(f'❌ Ошибка. Чтобы пользоваться ботом - нужно подписаться на канал\n🍿 @{channel_id} 🍿\nПосле подписки нажми 🔄 *Проверить подписку* ', reply_markup=keyboard.subscribe2channel(channel_id), parse_mode='Markdown')
		change_state(uid, None)
		return False




logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d.%m %H:%M:%S')

db.create_tables()
bot = Bot(token)
dp = Dispatcher(bot)

###START
@dp.message_handler(commands='start')
async def start_message(message: types.Message):
	username = message.from_user.username
	uid = message.from_user.id
	if await check_sub(uid):
		if check_unic(uid):
			new_user(uid, username)
		if check_ban(uid):
			change_state(uid, 0)
			await message.answer('Рад тебя видеть❕\nДавай скорее что-нибудь посмотрим\nЖми на /what2watch, если не знаешь что посмотреть', reply_markup=keyboard.main_kb(), parse_mode='Markdown')
		else:
			await message.answer('К сожалению, вы забанены', reply_markup=types.ReplyKeyboardRemove())
			change_state(uid, None)
	else:
		await message.answer(f'❌ Ошибка. Чтобы пользоваться ботом - нужно подписаться на канал\n🍿 @{channel_id} 🍿\nПосле подписки нажми 🔄 *Проверить подписку* ', reply_markup=keyboard.subscribe2channel(channel_id), parse_mode='Markdown')
		change_state(uid, None)


@dp.message_handler(commands='what2watch')
async def what2watch(message: types.Message):
	if await check_good( message,message.from_user.id):
		kp_id = get_interesting_film()
		title, kp_id, poster, rating, year, length, desc, countries, genres = getcinemainfo(kp_id)
		country = ', '.join(countries)
		genre = ', '.join(genres)
		await message.answer(f'''🎬 {title} [|]({poster}) {year}\n\n▫️ Рейтинг: {rating}\n▫️ Жанр: {genre}\n▫️ Страна: {country}\n▫️ Длительность: {length} мин.\n\n▫️Описание:\n{desc}\n\n\n[🎥 Смотреть сейчас]({player}{kp_id})''', parse_mode='Markdown', reply_markup=keyboard.film_profile(kp_id, title, message.from_user.id))

###ADMIN
@dp.message_handler(commands='admin')
async def admin_panel(message: types.Message):
	if message.from_user.id == admin_id:
		await message.answer('Добро пожаловать!', reply_markup=keyboard.admin_kb())




# States:
#
#-4 - distribution
#-3 - to unban user
#-2 - to ban user
#-1 - send message by userid
# 0 - main menu
# 1 - choose type of searching
# 2 - find film by title
# 3 - find film by kinopoisk code
# 4 - communication with the administrator


@dp.message_handler(content_types = ['text'])
async def send_text(message: types.Message):
	text = message.text
	uid = message.from_user.id
	state = get_state(uid)
	if await check_good(message,uid):
		if text == "💫 Назад в главное меню":
			await message.answer('Возвращаемся в главное меню...', reply_markup=keyboard.main_kb())
			change_state(uid,0)

		elif state == 1:
			if text == '🔹 По названию':
				await message.answer('Введите название', reply_markup=keyboard.finding())
				change_state(uid, 2)
			elif text == '🔹 По коду Kinopoisk':
				await message.answer('Введите код Кинопоиска', reply_markup=keyboard.finding())
				change_state(uid, 3)

		elif state == 2:
			await message.answer('Поиск...')
			cinema_list = getcinemalist(text.lower().capitalize())
			print(*cinema_list)
			if len(cinema_list)==0:
				await message.reply('К сожалению, я не смог ничего найти по данному запросу. Убедитесь, что название введено без ошибок', reply_markup = keyboard.finding())
			else:
				await message.answer('Уточните свой выбор или введите другое название:', reply_markup=keyboard.choose_film_inkb(cinema_list))
		
		elif state == 3:
			try:
				kp_id = int(text)
				await message.answer('Поиск...')
				try:
					title, kp_id, poster, rating, year, length, desc, countries, genres = getcinemainfo(kp_id)
					country = ', '.join(countries)
					genre = ', '.join(genres)
					await message.answer(f'''🎬 {title} [|]({poster}) {year}\n\n▫️ Рейтинг: {rating}\n▫️ Жанр: {genre}\n▫️ Страна: {country}\n▫️ Длительность: {length} мин.\n\n▫️Описание:\n{desc}\n\n\n[🎥 Смотреть сейчас]({player}{kp_id})''', parse_mode='Markdown', reply_markup=keyboard.film_profile(kp_id, title, uid))
				except:
					await message.reply('К сожалению, я не смог ничего найти. Убедитесь, что ввели код верно')
			except:
				await message.reply('Убедитесь, что код состоит только из цифр')


		elif state == 4:
			await bot.send_message(communication_channel, f'{text}\nuser_id = {uid}\nusername = @{message.from_user.username}')
			change_state(uid,0)
			await message.answer('Обращение успешно отправлено.', reply_markup = keyboard.main_kb())
		
		elif state == -1 and uid == admin_id:
			try:
				index = text.index('/')
				await bot.send_message(int(text[:index]), text[index+1:])
				await message.answer('Сообщение успешно отправлено', reply_markup = keyboard.main_kb())
				change_state(uid, 0)
			except:
				await message.reply('Введите сообщение в формате user_id/message')

		elif state == -2 and uid == admin_id:
			try:
				ban_id = int(text)
				ban_user(ban_id)
				await message.answer(f'Ползователь  с user_id - {ban_id} успешно заблокирован', reply_markup = keyboard.main_kb())
				change_state(uid, 0)
			except:
				await message.answer('К сожалению, я не смог никого заблокировать, убедитесь, что ввели верный user_id. Попробуйте ещё раз')

		elif state == -3 and uid == admin_id:
			try:
				unban_id = int(text)
				unban_user(unban_id)
				await message.answer(f'Пользователь c user_id - {unban_id} успешно разбанен.', reply_markup=keyboard.main_kb())
				change_state(uid, 0)
			except:
				await message.answer('К сожалению, я не смог никого разблокировать, убедитесь, что ввели верный user_id. Попробуйте ещё раз')
		
		elif state == -4 and uid == admin_id:
			try:
				for i in get_all_users_id():
					try:
						await bot.send_message(i, text)
					except:
						bot.send_message(communication_channel, f'Сообзение пользователю с user_id - {i} не было доставлено')
				await message.answer(f'Сообщение с текстом: \n{text}\nУспешно отправлено', reply_markup=keyboard.main_kb())
				change_state(uid, 0)
			except:
				await message.answer('К сожалению, сообщение не было доставлено')
				change_state(uid, 0)

		elif text == "🕵‍♂️Найти фильм":
			await message.answer(f'Выберите способ поиска: ', reply_markup=keyboard.find_film())
			change_state(uid, 1)

		elif text == '🧐Что посмотреть':
			kp_id = get_interesting_film()
			title, kp_id, poster, rating, year, length, desc, countries, genres = getcinemainfo(kp_id)
			country = ', '.join(countries)
			genre = ', '.join(genres)
			await message.answer(f'''🎬 {title} [|]({poster}) {year}\n\n▫️ Рейтинг: {rating}\n▫️ Жанр: {genre}\n▫️ Страна: {country}\n▫️ Длительность: {length} мин.\n\n▫️Описание:\n{desc}\n\n\n[🎥 Смотреть сейчас]({player}{kp_id})''', parse_mode='Markdown', reply_markup=keyboard.film_profile(kp_id, title, uid))

		elif text == '❔Связаться с администрацией':
			await message.answer('Напишите ваше обращение и с вами свяжутся в ближайшее время', reply_markup = keyboard.finding())
			change_state(uid, 4)

		elif text == '⭐ Избранное':
			try:
				cinema_list = [i.split('\\') for i in get_mark_list(uid)]
				while [''] in cinema_list:
					cinema_list.remove([''])
				await message.answer(f'На текущий момент у вас {len(cinema_list)}/25 избранных картин.\nВаши любимые фильмы:', reply_markup=keyboard.choose_film_inkb(cinema_list))
			except:
				await message.answer('У вас нет любимых фильмов 😮')

@dp.callback_query_handler(lambda c: c.data[:4] == 'adm_')
async def admin_panel(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	data = callback_query.data
	if callback_query.from_user.id == admin_id: 
		if data == 'adm_sendmes':		
			await bot.send_message(admin_id, 'Введите user_id и сообщение в формате: user_id/message', reply_markup = keyboard.finding())
			change_state(admin_id, -1)
		elif data == 'adm_ban':
			await bot.send_message(admin_id, 'Введите user_id человека, которого нужно забанить', reply_markup = keyboard.finding())
			change_state(admin_id, -2)
		elif data == 'adm_unban':
			await bot.send_message(admin_id, 'Введите user_id человека, которого нужно разбанить', reply_markup = keyboard.finding())
			change_state(admin_id, -3)	
		elif data == 'adm_userscount':
			await bot.send_message(admin_id, f'Количество пользователей - {count_users()}', reply_markup = keyboard.main_kb())
		elif data == 'adm_base':
			await bot.send_document(admin_id, open('bot.db', 'rb'))
		elif data == 'adm_distrib':
			await bot.send_message(admin_id, 'Введите текст для рассылки:', reply_markup=keyboard.finding())
			change_state(admin_id, -4)


@dp.callback_query_handler(lambda c: c.data[:3]=='kp_')
async def film_profile(callback_query: types.CallbackQuery):
	if await check_sub(callback_query.from_user.id):
		if check_ban(callback_query.from_user.id):
			await bot.answer_callback_query(callback_query.id)
			kp_id = callback_query.data
			title, kp_id, poster, rating, year, length, desc, countries, genres = getcinemainfo(kp_id[3:])
			country = ', '.join(countries)
			genre = ', '.join(genres)
			await bot.send_message(callback_query.from_user.id, f'''🎬 {title} [|]({poster}) {year}\n\n▫️ Рейтинг: {rating}\n▫️ Жанр: {genre}\n▫️ Страна: {country}\n▫️ Длительность: {length} мин.\n\n▫️Описание:\n{desc}\n\n\n[🎥 Смотреть сейчас]({player}{kp_id})''', parse_mode='Markdown', reply_markup=keyboard.film_profile(kp_id, title, callback_query.from_user.id))
		else:
			await message.answer('К сожалению, вы забанены', reply_markup=types.ReplyKeyboardRemove())
	else:
		await message.answer(f'❌ Ошибка. Чтобы пользоваться ботом - нужно подписаться на канал\n🍿 @{channel_id} 🍿\nПосле подписки нажми 🔄 *Проверить подписку* ', reply_markup=keyboard.subscribe2channel(channel_id), parse_mode='Markdown')
		change_state(callback_query.from_user.id, None)


###Similar
@dp.callback_query_handler(lambda c: c.data[:3]=='sf_')
async def similar_films(callback_query: types.CallbackQuery):
	if await check_sub(callback_query.from_user.id):
		if check_ban(callback_query.from_user.id):
			await bot.answer_callback_query(callback_query.id)
			kp_id = callback_query.data
			kp_id = kp_id[3:]
			similar_list = get_similar_films(kp_id)
			title, kp_id, poster, rating, year, length, desc, countries, genres = getcinemainfo(choice(similar_list))
			country = ', '.join(countries)
			genre = ', '.join(genres)
			await bot.send_message(callback_query.from_user.id, f'''🎬 {title} [|]({poster}) {year}\n\n▫️ Рейтинг: {rating}\n▫️ Жанр: {genre}\n▫️ Страна: {country}\n▫️ Длительность: {length} мин.\n\n▫️Описание:\n{desc}\n\n\n[🎥 Смотреть сейчас]({player}{kp_id})''', parse_mode='Markdown', reply_markup=keyboard.film_profile(kp_id, title, callback_query.from_user.id))
		else:
			await message.answer('К сожалению, вы забанены', reply_markup=types.ReplyKeyboardRemove())
	else:
		await message.answer(f'❌ Ошибка. Чтобы пользоваться ботом - нужно подписаться на канал\n🍿 @{channel_id} 🍿\nПосле подписки нажми 🔄 *Проверить подписку* ', reply_markup=keyboard.subscribe2channel(channel_id), parse_mode='Markdown')
		change_state(callback_query.from_user.id, None)

@dp.callback_query_handler(lambda c: c.data == 'check_sub')
async def check_sub_callback(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if await check_sub(callback_query.from_user.id):
		await bot.send_message(callback_query.from_user.id, '✅ Доступ разрешён', reply_markup = keyboard.main_kb())
	else:
		await bot.send_message(callback_query.from_user.id, f'✴ Вы не подписаны на @{channel_id} - подпишитесь ☺', reply_markup = keyboard.main_kb())


@dp.callback_query_handler(lambda c: c.data[:5] == 'mark_')
async def add_to_mark(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if await check_sub(callback_query.from_user.id):
		if check_ban(callback_query.from_user.id):	
			if len(get_mark_list(callback_query.from_user.id)) <26:
				try:
					add2mark(callback_query.from_user.id, callback_query.data[5:])
					await bot.send_message(callback_query.from_user.id, 'Фильм успешно добавлен в избранное')
				except:
					await bot.send_message(callback_query.from_user.id, 'к сожалению, мне не удалось добавить фильм в избранное')
			else:
				await bot.send_message(callback_query.from_user.id, 'К сожалению, количество ваших избранных фильмов превышает максимум')
	else:
		await message.answer(f'❌ Ошибка. Чтобы пользоваться ботом - нужно подписаться на канал\n🍿 @{channel_id} 🍿\nПосле подписки нажми 🔄 *Проверить подписку* ', reply_markup=keyboard.subscribe2channel(channel_id), parse_mode='Markdown')
		change_state(callback_query.from_user.id, None)


@dp.callback_query_handler(lambda c: c.data[:7] == 'unmark_')
async def add_to_mark(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if await check_sub(callback_query.from_user.id):
		if check_ban(callback_query.from_user.id):	
			try:
				delfrommark(callback_query.from_user.id, callback_query.data[7:])
				await bot.send_message(callback_query.from_user.id, 'Фильм успешно удалён из избранных')
			except:
				await bot.send_message(callback_query.from_user.id, 'К сожалению, мне не удалось удалить фильм из избранных') 
		else:
			await message.answer('К сожалению, вы забанены', reply_markup=types.ReplyKeyboardRemove())
	else:
		await message.answer(f'❌ Ошибка. Чтобы пользоваться ботом - нужно подписаться на канал\n🍿 @{channel_id} 🍿\nПосле подписки нажми 🔄 *Проверить подписку* ', reply_markup=keyboard.subscribe2channel(channel_id), parse_mode='Markdown')
		change_state(callback_query.from_user.id, None)




# ###Autoposting
# async def post_random_film(channel_id:int):
# 	await asyncio.sleep(TIMEOUT)








if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)