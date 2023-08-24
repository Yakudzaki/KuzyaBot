import sqlite3
from app import db_file
path = db_file 


connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS love (
    lover1   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    lover2   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,

    FOREIGN KEY (
        lover1
    )
    REFERENCES users (user_id),
    FOREIGN KEY (
        lover2
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()

def create_love(lover1, lover2): #Регистрация гражданского брака
    cursor.execute("INSERT INTO love VALUES(?,?)", (lover1, lover2,))
    connect.commit()
    
def delete_love(lover1, lover2): #Удаление регистрации гражданского брака
    cursor.execute("DELETE FROM love WHERE lover1 = ? AND lover2 = ?", (lover1, lover2,))

    cursor.execute("DELETE FROM love WHERE lover2 = ? AND lover1 = ?", (lover1, lover2,))
    connect.commit()

def delete_all_love(lover): #Удаление всех браков юзера
    cursor.execute(f"DELETE FROM love WHERE lover1 = {lover} OR lover2 = {lover}")

    connect.commit()

def get_love(lover): #Получить список всех любовников и любовниц юзера. Выдается в виде… Списка из списков. Включающих айди самого юзера. Так что… 
    cursor.execute(f"SELECT lover1, lover2 FROM love WHERE lover1 = {lover} OR lover2 = {lover}")
    lover = cursor.fetchall()

    return lover
    
def check_love(lover1, lover2): #Проверить наличие гражданского брака между юзерами.
    cursor.execute("SELECT * FROM love WHERE lover1 = ? AND lover2 = ?", (lover1, lover2,))
    result1 = cursor.fetchone()
    
    cursor.execute("SELECT * FROM love WHERE lover2 = ? AND lover1 = ?", (lover1, lover2,))
    result2 = cursor.fetchone()

    
    if result1 is None and result2 is None:
        return False
    else:
        return True