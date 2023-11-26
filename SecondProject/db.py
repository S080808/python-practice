import sqlite3

def make_connect():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    return conn, cursor
def create_tables():
    conn, cursor = make_connect()
    try:
        cursor.execute("CREATE TABLE users(user_id INTEGER, name, state INTEGER, ban INTEGER, favorites)")
    except:
        pass