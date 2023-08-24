import sqlite3
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS sibl (
    sibler1   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    sibler2   INTEGER REFERENCES users (user_id) ON DELETE CASCADE,

    FOREIGN KEY (
        sibler1
    )
    REFERENCES users (user_id),
    FOREIGN KEY (
        sibler2
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()


def create_sibl(sibler1, sibler2): #Регистрация родственников
    cursor.execute("INSERT INTO sibl VALUES(?,?)", (sibler1, sibler2,))
    connect.commit()
    
def delete_sibl(sibler1, sibler2): #Удаление регистрации родственников.
    cursor.execute("DELETE FROM sibl WHERE sibler1 = ? AND sibler2 = ?", (sibler1, sibler2,))

    cursor.execute("DELETE FROM sibl WHERE sibler2 = ? AND sibler1 = ?", (sibler1, sibler2,))
    connect.commit()

def delete_all_sibl(sibler): #Удаление регистрации родственников.
    cursor.execute(f"DELETE FROM sibl WHERE sibler1 = {sibler} OR sibler2 = {sibler}")

    connect.commit()

def get_sibl(sibler): #Получить всех родственников. В том числе и самого юзера. Так что… В коде придется его убирать. Возможно. А может, где-то и не придется.
    cursor.execute(f"SELECT sibler2, sibler1 FROM sibl WHERE sibler1 = {sibler} OR sibler2 = {sibler}")
    sibler = cursor.fetchall()


    return sibler

def check_sibl(sibler1, sibler2): #Проверить являются ли юзеры родственниками. Если да - то выдается True.
    cursor.execute("SELECT * FROM sibl WHERE sibler1 = ? AND sibler2 = ?", (sibler1, sibler2,))
    result1 = cursor.fetchone()
    
    cursor.execute("SELECT * FROM sibl WHERE sibler2 = ? AND sibler1 = ?", (sibler1, sibler2,))
    result2 = cursor.fetchone()

   
    if result1 is None and result2 is None:
        return False
    else:
        return True