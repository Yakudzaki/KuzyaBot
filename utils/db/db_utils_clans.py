import sqlite3
#from app import db_file as path
path = "C:/Users/Sveta/OneDrive/Рабочий стол/Project/KuzyaBot/utils/db/kuzya.db"

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

def get_clan(clan_id: int):
    cursor.execute("SELECT * FROM clans WHERE id = ?", (clan_id, ))
    return cursor.fetchone()


def get_top_clans(limit: int = 10):
    cursor.execute(f'SELECT * FROM clans ORDER BY balance DESC LIMIT ?;', (limit, ))
    return cursor.fetchall()

