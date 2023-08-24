import sqlite3
from app import db_file
from utils.db.db_utils_users import get_user

path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS warning (
    chat_id   INTEGER REFERENCES chats (chat_id) ON DELETE CASCADE,
    warner_id INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    warns INTEGER,
    matex_status INTEGER,
    kuzya_ban INTEGER,
    FOREIGN KEY (
        chat_id
    )
    REFERENCES chats (chat_id),
    FOREIGN KEY (
        warner_id
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()

def create_warner(chat_id, warner_id): #Регистрация члена чата в базе
    if check_warner(chat_id, warner_id) == False:

        cursor.execute("INSERT INTO warning VALUES(?,?,?,?,?)", (chat_id, warner_id, 0, 0, 0,))
        connect.commit()

    else:
        return


def check_warner(chat_id, warner_id): #проверить, является ли юзер участником чата в базе кузи
    cursor.execute("SELECT * FROM warning WHERE chat_id = ? AND warner_id = ?", (chat_id, warner_id,))
    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True

def get_warner(chat_id, warner_id): #получить данные участника чата
    cursor.execute("SELECT * FROM warning WHERE chat_id = ? AND warner_id = ?", (chat_id, warner_id,))
    result = cursor.fetchone()
    
    if result is None:
        result = [chat_id, warner_id, 0, 0, 0]

    user = get_user(warner_id)
    
    if user != None:
        if user[9] == 2:
            return [chat_id, warner_id, result[2], result[3], 0]
        elif user[9] == 3:
            return [chat_id, warner_id, result[2], result[3], 1]
        else:
            return result
    
    else:
        return result

def add_warning(chat_id, warner_id):
    cursor.execute("UPDATE warning SET warns = warns + 1 WHERE chat_id = ? AND warner_id = ?", (chat_id, warner_id,))
    connect.commit()



def take_warning(chat_id, warner_id):
    cursor.execute("UPDATE warning SET warns = warns - 1 WHERE chat_id = ? AND warner_id = ?", (chat_id, warner_id,))
    connect.commit()


def set_matex_status(chat_id, warner_id, matex_status): #Обновить статус юзера в чате
    cursor.execute("UPDATE warning SET matex_status = ? WHERE warner_id = ? and chat_id = ?", (matex_status, warner_id, chat_id,))
    connect.commit()
    
def set_kuzya_ban(chat_id, warner_id, kuzya_ban): #Обновить кузябан юзера в чате
    cursor.execute("UPDATE warning SET kuzya_ban = ? WHERE warner_id = ? and chat_id = ?", (kuzya_ban, warner_id, chat_id,))
    connect.commit()