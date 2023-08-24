import sqlite3
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS marry (
    marryer1   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    marryer2   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,

    FOREIGN KEY (
        marryer1
    )
    REFERENCES users (user_id),
    FOREIGN KEY (
        marryer2
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()

def create_marry(marryer1, marryer2): #Регистрация свдьбы
    cursor.execute("INSERT INTO marry VALUES(?,?)", (marryer1, marryer2,))
    connect.commit()
    
def delete_marry(marryer1, marryer2): #Удаление регистрации свадьбы
    cursor.execute("DELETE FROM marry WHERE marryer1 = ? AND marryer2 = ?", (marryer1, marryer2,))

    cursor.execute("DELETE FROM marry WHERE marryer2 = ? AND marryer1 = ?", (marryer1, marryer2,))
    connect.commit()
    
def delete_all_marry(marryer): #Удалить все свадьбы юзера
    cursor.execute(f"DELETE FROM marry WHERE marryer1 = {marryer} OR marryer2 = {marryer}")

    connect.commit()
    
def get_marry(marryer): #Получить всех супругов юзера. В списке будут и айди самого юзера. Так что, смотрите.
    cursor.execute(f"SELECT marryer2, marryer1 FROM marry WHERE marryer1 = {marryer} OR marryer2 = {marryer}")
    marryer = cursor.fetchall()


    return marryer

def check_marry(marryer1, marryer2): #Проверить, есть ли свадьба. Если есть - то True.
    cursor.execute("SELECT * FROM marry WHERE marryer1 = ? AND marryer2 = ?", (marryer1, marryer2,))
    result1 = cursor.fetchone()
    
    cursor.execute("SELECT * FROM marry WHERE marryer2 = ? AND marryer1 = ?", (marryer1, marryer2,))
    result2 = cursor.fetchone()

   
    if result1 is None and result2 is None:
        return False
    else:
        return True