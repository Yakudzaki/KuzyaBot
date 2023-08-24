import sqlite3
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS want_sibl (
    user_id   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    want_to_sibl  INTEGER REFERENCES users (user_id) ON DELETE CASCADE,

    FOREIGN KEY (
        user_id
    )
    REFERENCES users (user_id),
    FOREIGN KEY (
        want_to_sibl
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()

def create_wsibl(user_id, wsibler): #Кто желает стать брадом, и у кого
    cursor.execute("INSERT INTO want_sibl VALUES(?,?)", (user_id, wsibler,))
    connect.commit()

def check_wsibl(user_id, wsibler): #проверить желание первого, стать брадом второго
    cursor.execute("SELECT * FROM want_sibl WHERE user_id = ? AND want_to_sibl = ?", (user_id, wsibler,))
    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True
        
def delete_wsibl(user_id, wsibler): #удалить желание первого, стать брадом второго
    cursor.execute("DELETE FROM want_sibl WHERE user_id = ? AND want_to_sibl = ?", (user_id, wsibler,))
    connect.commit()

def delete_all_wsibl(user_id): #удалить все желания юзера стать кому-то брадом
    cursor.execute("DELETE FROM want_sibl WHERE user_id = ?", (user_id,))
    connect.commit()

def get_wsibles(user_id): #получить список людей, брадом которых хочет стать юзер
    cursor.execute(f"SELECT want_to_sibl FROM want_sibl WHERE user_id = {user_id}")
    wsibler = cursor.fetchall()

    return wsibler
    
def get_wsiblers(user_id): #получить список людей, которые хотят стать брадом юзера
    cursor.execute(f"SELECT user_id FROM want_sibl WHERE want_to_sibl = {user_id}")
    wsibler = cursor.fetchall()

    return wsibler