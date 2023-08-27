import sqlite3
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS moniks (
    moniker_id   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    monik TEXT NOT NULL DEFAULT '',
    count_monik INTEGER,
    monik_nomn TEXT NOT NULL DEFAULT '',
    monik_gent TEXT NOT NULL DEFAULT '',
    monik_datv TEXT NOT NULL DEFAULT '',
    monik_accs TEXT NOT NULL DEFAULT '',
    monik_ablt TEXT NOT NULL DEFAULT '',
    monik_loct TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (
        moniker_id
    )
    REFERENCES users (user_id)
    )
""")



connect.commit()

def create_monik(moniker_id, monik): #Регистрация прозвища за юзером
    cursor.execute("INSERT INTO moniks VALUES(?,?,?,?,?,?,?,?,?)", (moniker_id, monik, 0, "", "", "", "", "", "",))
    connect.commit()

def add_m_rep(moniker_id, monik): #Добавить один репутации к прозвищу.

    cursor.execute("UPDATE moniks SET count_monik = count_monik + 1 WHERE moniker_id = ? and monik = ?", (moniker_id, monik,))
    connect.commit()

def add_z_rep(moniker_id, monik, num): #Добавить число репутации к прозвищу.

    cursor.execute(f"UPDATE moniks SET count_monik = count_monik + ? WHERE moniker_id = ? and monik = ?", (num, moniker_id, monik,))
    connect.commit()

def check_monik(moniker_id, monik): #проверить, есть ли у хумана  некое прозвище.

    cursor.execute("SELECT * FROM moniks WHERE moniker_id = ? AND monik = ?", (moniker_id, monik,))
    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True

def check_moniks(moniker_id): #проверить, есть ли у хумана  прозвище, хоть какое-то.

    cursor.execute("SELECT * FROM moniks WHERE moniker_id = ?", (moniker_id,))
    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True

def get_monik(moniker_id, monik): #Вытащить данные о прозвище.

    cursor.execute("SELECT * FROM moniks WHERE moniker_id = ? AND monik = ?", (moniker_id, monik,))
    result = cursor.fetchone()
    return result


def get_max_monik(moniker_id, limit: int = 2): #получить самое сильное прозвище. (под цифрой [1])
    cursor.execute(f"SELECT * FROM moniks WHERE moniker_id = ? ORDER BY count_monik DESC LIMIT ?", (moniker_id, limit, ))
    monik = cursor.fetchone()
    # check_monik(moniker_id, "") 
    return monik

def get_all_moniks(moniker_id, limit: int = 50): #получить все прозвища чела.
    cursor.execute(f"SELECT * FROM moniks WHERE moniker_id = ? ORDER BY count_monik DESC LIMIT ?", (moniker_id, limit, ))
    moniks = cursor.fetchall()
    # check_monik(moniker_id, "") 
    return moniks





def set_monik_nomn(moniker_id, monik, monik_nomn):
    cursor.execute("UPDATE moniks SET monik_nomn = ? WHERE moniker_id = ? AND monik = ?", (monik_nomn, moniker_id, monik,))
    connect.commit()


def set_monik_gent(moniker_id, monik, monik_gent):
    cursor.execute("UPDATE moniks SET monik_gent = ? WHERE moniker_id = ? AND monik = ?", (monik_gent, moniker_id, monik,))
    connect.commit()
    
def set_monik_datv(moniker_id, monik, monik_datv):
    cursor.execute("UPDATE moniks SET monik_datv = ? WHERE moniker_id = ? AND monik = ?", (monik_datv, moniker_id, monik,))
    connect.commit()
    
    
def set_monik_accs(moniker_id, monik, monik_accs):
    cursor.execute("UPDATE moniks SET monik_accs = ? WHERE moniker_id = ? AND monik = ?", (monik_accs, moniker_id, monik,))
    connect.commit()
    
def set_monik_ablt(moniker_id, monik, monik_ablt):
    cursor.execute("UPDATE moniks SET monik_ablt = ? WHERE moniker_id = ? AND monik = ?", (monik_ablt, moniker_id, monik,))
    connect.commit()
    
def set_monik_loct(moniker_id, monik, monik_loct):
    cursor.execute("UPDATE moniks SET monik_loct = ? WHERE moniker_id = ? AND monik = ?", (monik_loct, moniker_id, monik,))
    connect.commit()