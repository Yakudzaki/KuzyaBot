import sqlite3
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS want_marry (
    user_id   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    want_to_marry   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,

    FOREIGN KEY (
        user_id
    )
    REFERENCES users (user_id),
    FOREIGN KEY (
        want_to_marry
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()


def create_wmarry(user_id, wmarryer): #Кто желает стать супругом и у кого
    cursor.execute("INSERT INTO want_marry VALUES(?,?)", (user_id, wmarryer,))
    connect.commit()

def check_wmarry(user_id, wmarryer): #проверить желание первого, стать супругом второго
    cursor.execute("SELECT * FROM want_marry WHERE user_id = ? AND want_to_marry = ?", (user_id, wmarryer,))
    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True
        
def delete_wmarry(user_id, wmarryer): #удалить желание первого, стать супругом второго
    cursor.execute("DELETE FROM want_marry WHERE user_id = ? AND want_to_marry = ?", (user_id, wmarryer,))
    connect.commit()

def delete_all_wmarry(user_id): #удалить все желания стать супругами у юзера
    cursor.execute("DELETE FROM want_marry WHERE user_id = ?", (user_id,))
    connect.commit()

def get_wmarrys(user_id): #получить список людей, супругом которых хочет стать юзер
    cursor.execute(f"SELECT want_to_marry FROM want_marry WHERE user_id = {user_id}")
    wmarryer = cursor.fetchall()

    return wmarryer
    
def get_wmarryers(user_id): #получить список людей, которые хотят стать супругом юзера
    cursor.execute(f"SELECT user_id FROM want_marry WHERE want_to_marry = {user_id}")
    wmarryer = cursor.fetchall()

    return wmarryer