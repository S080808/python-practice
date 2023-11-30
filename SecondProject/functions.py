import requests, json
from config import *
from db import *
from random import choice

# ### Helping functions
# Если нужна сортировка по годам нужна
# def keyFunc(item):
#    return item[1]
###



#### Brain functions
def getcinemalist(title):
	request = requests.get(f'{cdn_url}short?api_token={cdn_api}&title={title}')
	request_json = json.loads(request.text)
	#Если пользователь ввёл запрос, который выдаёт большое количество фильмов, выведем первые пять, чтобы не загружать сервер.
	try:
		request_json['data'] = request_json['data'][:10] #Выбери нужное количество
	except:
		pass
	cinemalist = [[i['title'], i['year'][:4], i['kp_id']] for i in request_json['data']]
	#cinemalist.sort(key=keyFunc, reverse=True)
	return cinemalist

def get_similar_films(kp_id):
	request = requests.get(f'{kp_api_url}films/{kp_id}/similars', headers={'X-API-KEY': f'{kp_api}'})
	request_json = json.loads(request.text)
	cinemalist = [i['filmId'] for i in request_json['items']]
	return cinemalist

def getcinemainfo(kp_id):
	request = requests.get(f'{kp_api_url}films/{kp_id}', headers={'X-API-KEY': f'{kp_api}'})
	request_json = json.loads(request.text)
	name = request_json['nameRu']
	poster = request_json['posterUrl']
	rating = request_json['ratingKinopoisk']
	year = request_json['year']
	length = request_json['filmLength']
	desc = request_json['description']
	countries = [i['country'] for i in request_json['countries']]
	genres = [i['genre'] for i in request_json['genres']]
	return name, kp_id, poster, rating, year, length, desc, countries, genres


def get_interesting_film():
	page = choice(range(1, 14))
	request = requests.get(f'{kp_api_url}films/top?type=TOP_250_BEST_FILMS&page={page}', headers={'X-API-KEY': f'{kp_api}'})
	request_json = json.loads(request.text)
	return choice(request_json['films'])['filmId']
#####

##### TG functions
def get_state(uid):
	conn, cursor = make_connect()
	cursor.execute("SELECT state FROM users WHERE user_id = ?", (uid, ))
	return cursor.fetchone()[0]

def change_state(uid, state):
    conn, cursor = make_connect()
    cursor.execute("UPDATE users SET state = ? WHERE user_id = ?", (state, uid,))
    conn.commit()	

def check_unic(uid):
    conn, cursor = make_connect()
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (uid, ))
    return cursor.fetchone()[0] == 0

def new_user(uid, name):
    if check_unic(uid):
        conn, cursor = make_connect()
        cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)", (uid, name, None, 0, None))
        conn.commit()

def check_ban(uid):
	conn, cursor = make_connect()
	cursor.execute("SELECT ban FROM users WHERE user_id = ?", (uid, ))
	return cursor.fetchone()[0]==0

def ban_user(uid):
    conn, cursor = make_connect()
    cursor.execute("UPDATE users SET ban = ? WHERE user_id = ?", (1, uid,))
    conn.commit()

def unban_user(uid):
	conn, cursor = make_connect()
	cursor.execute("UPDATE users SET ban = ? WHERE user_id = ?", (0, uid,))
	conn.commit()


def count_users():
	conn, cursor = make_connect()
	cursor.execute("SELECT COUNT(*) from users")  
	return cursor.fetchone()[0]

def get_all_users_id():
	conn, cursor = make_connect()
	cursor.execute("SELECT user_id from users")  
	return cursor.fetchone()



def get_mark_list(uid):
	conn, cursor = make_connect()
	cursor.execute("SELECT favorites FROM users WHERE user_id = ?", (uid, ))
	try:
		mark_list = cursor.fetchone()[0]
		return mark_list.split('֍')
	except:
		return []

def add2mark(uid, film2db):
	mark_list = get_mark_list(uid)
	if film2db not in mark_list:
		mark_list.append(film2db)
		mark_list = '֍'.join(mark_list)
		conn, cursor = make_connect()
		cursor.execute("UPDATE users SET favorites = ? WHERE user_id = ?", (mark_list, uid, ))
		conn.commit()	


def delfrommark(uid, film2db):
	mark_list = get_mark_list(uid)
	if film2db in mark_list:
		mark_list.remove(film2db)
		mark_list = '֍'.join(mark_list)
		conn, cursor = make_connect()
		cursor.execute("UPDATE users SET favorites = ? WHERE user_id = ?", (mark_list, uid, ))
		conn.commit()

#####
