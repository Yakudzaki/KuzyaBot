import sqlite3
<<<<<<< HEAD
from app import db_file as path
=======
#from app import db_file as path
from app import db_file
path = db_file 
>>>>>>> 6ff942c02045a8e69b583897a3f5effd3efe3107

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

def get_clan(clan_id: int):
    cursor.execute("SELECT * FROM clans WHERE id = ?", (clan_id, ))
    return cursor.fetchone()


def get_top_clans(limit: int = 10):
    cursor.execute(f'SELECT * FROM clans ORDER BY balance DESC LIMIT ?;', (limit, ))
    return cursor.fetchall()

def get_clans_count_players(clan_id: int) -> int:
    cursor.execute('SELECT COUNT(*) FROM users WHERE clan_id = ?;', (clan_id, ))
    return cursor.fetchone()[0]