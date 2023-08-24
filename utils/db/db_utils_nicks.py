import sqlite3
import html
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()

cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS nicks (
    user_id    INTEGER REFERENCES users (user_id) ON DELETE CASCADE UNIQUE ON CONFLICT REPLACE,
    nick_orig TEXT NOT NULL DEFAULT '',
    nick_nomn TEXT NOT NULL DEFAULT '',
    nick_gent TEXT NOT NULL DEFAULT '',
    nick_datv TEXT NOT NULL DEFAULT '',
    nick_accs TEXT NOT NULL DEFAULT '',
    nick_ablt TEXT NOT NULL DEFAULT '',
    nick_loct TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (
        user_id
    )
    REFERENCES users (user_id)
    )
""")

connect.commit()


def get_users_nick(id):

    cursor.execute("SELECT * FROM nicks WHERE user_id = ?", (id,))
    user = cursor.fetchone()
    return user


def check_users_nick(id):

    cursor.execute("SELECT * FROM nicks WHERE user_id = ?", (id,))
    result = cursor.fetchone()
    
    if result == None:
        return True
    else:
        return False

def create_user_nick(user_id, nick_orig, nick_nomn, nick_gent, nick_datv, nick_accs, nick_ablt, nick_loct):
    
    cursor.execute("INSERT INTO nicks VALUES(?,?,?,?,?,?,?,?)", (user_id, nick_orig, nick_nomn, nick_gent, nick_datv, nick_accs, nick_ablt, nick_loct,))
    connect.commit()
    
    user_nick = [user_id, nick_orig, nick_nomn, nick_gent, nick_datv, nick_accs, nick_ablt, nick_loct]
    return user_nick

def set_nick_nomn(user_id, nick_nomn):
    cursor.execute("UPDATE nicks SET nick_nomn = ? WHERE user_id = ?", (nick_nomn, user_id,))
    connect.commit()


def set_nick_gent(user_id, nick_gent):
    cursor.execute("UPDATE nicks SET nick_gent = ? WHERE user_id = ?", (nick_gent, user_id,))
    connect.commit()
    
def set_nick_datv(user_id, nick_datv):
    cursor.execute("UPDATE nicks SET nick_datv = ? WHERE user_id = ?", (nick_datv, user_id,))
    connect.commit()
    
    
def set_nick_accs(user_id, nick_accs):
    cursor.execute("UPDATE nicks SET nick_accs = ? WHERE user_id = ?", (nick_accs, user_id,))
    connect.commit()
    
def set_nick_ablt(user_id, nick_ablt):
    cursor.execute("UPDATE nicks SET nick_ablt = ? WHERE user_id = ?", (nick_ablt, user_id,))
    connect.commit()
    
def set_nick_loct(user_id, nick_loct):
    cursor.execute("UPDATE nicks SET nick_loct = ? WHERE user_id = ?", (nick_loct, user_id,))
    connect.commit()