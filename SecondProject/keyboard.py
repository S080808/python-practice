from aiogram import types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from functions import getcinemalist, get_similar_films, get_mark_list
from config import *

def main_kb():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row("🕵‍♂️Найти фильм", "🔍Найти актёра")
	markup.row("🧐Что посмотреть", "❔Связаться с администрацией")
	markup.row('⭐ Избранное')
	return markup

def find_film():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row("🔹 По названию")
	markup.row("🔹 По коду Kinopoisk")
	markup.row("💫 Назад в главное меню")
	return markup

def admin_kb():
	inline_kb = types.InlineKeyboardMarkup()
	inline_kb.add(types.InlineKeyboardButton('Написать сообщение', callback_data = 'adm_sendmes'))
	inline_kb.add(types.InlineKeyboardButton('Забанить', callback_data = 'adm_ban'))
	inline_kb.add(types.InlineKeyboardButton('Разбанить', callback_data = 'adm_unban'))
	inline_kb.add(types.InlineKeyboardButton('Количество пользователей', callback_data ='adm_userscount'))
	inline_kb.add(types.InlineKeyboardButton('База данных', callback_data = 'adm_base'))
	inline_kb.add(types.InlineKeyboardButton('Рассылка', callback_data = 'adm_distrib'))
	return inline_kb

def choose_film_inkb(cinema_list):
	inline_kb = types.InlineKeyboardMarkup(resize_keyboard=True)
	if len(cinema_list[0]) == 3:
		for i in range(len(cinema_list)):
			# if len(cinema_list[i][0])>18:
			# 	cinema_list[i][0] = cinema_list[i][0][:5] + '...'
			inline_kb.add(types.InlineKeyboardButton(f'{cinema_list[i][0]} - {cinema_list[i][1]}', callback_data=f'kp_{cinema_list[i][2]}'))
	else:
		for i in range(len(cinema_list)):
			# if len(cinema_list[i][0])>18:
			# 	cinema_list[i][0] = cinema_list[i][0][:5] + '...'
			inline_kb.add(types.InlineKeyboardButton(f'{cinema_list[i][0]}', callback_data=f'kp_{cinema_list[i][1]}'))
	return inline_kb

def finding():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row("💫 Назад в главное меню")
	return markup

def film_profile(kp_id, title, uid):
	inline_kb = types.InlineKeyboardMarkup()
	inline_kb.add(types.InlineKeyboardButton('🍿 Смотреть сейчас 🍿', url=f'{player}{kp_id}'))
	if len(get_similar_films(kp_id))!=0:
		inline_kb.add(types.InlineKeyboardButton('🎬 Похожие фильмы 🎬', callback_data = f'sf_{kp_id}'))
	if f'{title}\\{kp_id}' not in get_mark_list(uid):
		inline_kb.add(types.InlineKeyboardButton('⭐ Добавить в избранное ⭐', callback_data = f'mark_{title}\\{kp_id}'))
	else:
		inline_kb.add(types.InlineKeyboardButton('⭐ Удалить из избранного ⭐', callback_data = f'unmark_{title}\\{kp_id}'))
	return inline_kb

def subscribe2channel(channel_id:str):
	inline_kb = types.InlineKeyboardMarkup()
	inline_kb.add(types.InlineKeyboardButton('❇ Подписаться сейчас', url=f't.me/{channel_id}'))
	inline_kb.add(types.InlineKeyboardButton('🔄 Проверить подписку', callback_data='check_sub'))
	return inline_kb