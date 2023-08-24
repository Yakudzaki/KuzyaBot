import sqlite3
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS want_love (
    user_id   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    want_to_love   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,

    FOREIGN KEY (
        user_id
    )
    REFERENCES users (user_id),
    FOREIGN KEY (
        want_to_love
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()

def create_wlove(user_id, wloveer): #Кто желает стать интимом и у кого
    cursor.execute("INSERT INTO want_love VALUES(?,?)", (user_id, wloveer,))
    connect.commit()

def check_wlove(user_id, wlover): #проверить желание первого, стать интимом второго
    cursor.execute("SELECT * FROM want_love WHERE user_id = ? AND want_to_love = ?", (user_id, wlover,))
    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True
        
def delete_wlove(user_id, wlover): #удалить желание первого, стать интимом второго
    cursor.execute("DELETE FROM want_love WHERE user_id = ? AND want_to_love = ?", (user_id, wlover,))
    connect.commit()

def delete_all_wlove(user_id): #удалить все желания стать интимом у юзера
    cursor.execute("DELETE FROM want_love WHERE user_id = ?", (user_id,))
    connect.commit()

def get_wloves(user_id): #получить список людей, интимом которых хочет стать юзер
    cursor.execute(f"SELECT want_to_love FROM want_love WHERE user_id = {user_id}")
    wloveer = cursor.fetchall()

    return wloveer
    
def get_wlovers(user_id): #получить список людей, которые хотят стать интимом юзера
    cursor.execute(f"SELECT user_id FROM want_love WHERE want_to_love = {user_id}")
    wloveer = cursor.fetchall()

    return wloveer