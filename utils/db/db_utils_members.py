import sqlite3
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS members (
    chat_id   INTEGER REFERENCES chats (chat_id) ON DELETE CASCADE,
    member_id INTEGER REFERENCES users (user_id) ON DELETE CASCADE,
    status_m TEXT,
    FOREIGN KEY (
        chat_id
    )
    REFERENCES chats (chat_id),
    FOREIGN KEY (
        member_id
    )
    REFERENCES users (user_id) 
    )
""")



connect.commit()

def create_member(chat_id, member_id, status_m): #Регистрация члена чата в базе
    if check_member(chat_id, member_id) == False:

        cursor.execute("INSERT INTO members VALUES(?,?,?)", (chat_id, member_id, status_m,))
        print(f"Создан {status_m} {member_id} в чате: {chat_id}")
        connect.commit()

    else:
        print(f"Не был дуплицирован {status_m} {member_id} в чате: {chat_id}, ибо уже есть там.")


def check_member(chat_id, member_id): #проверить, является ли юзер участником чата в базе кузи
    cursor.execute("SELECT * FROM members WHERE chat_id = ? AND member_id = ?", (chat_id, member_id,))
    result = cursor.fetchone()

    if result is None:
        return False
    else:
        return True

def get_member(chat_id, member_id): #проверить, является ли юзер участником чата в базе кузи
    cursor.execute("SELECT * FROM members WHERE chat_id = ? AND member_id = ?", (chat_id, member_id,))
    result = cursor.fetchone()
    return result

def delete_member(chat_id, member_id): #удалить участника чата из чата, в базе кузи
    cursor.execute("DELETE FROM members WHERE chat_id = ? AND member_id = ?", (chat_id, member_id,))
    connect.commit()


def get_members(chat_id): #получить список людей, которые являются участниками чата согласно базе кузи (ВСЕХ ЛЮДЕЙ)
    cursor.execute(f"SELECT * FROM members WHERE chat_id = {chat_id}")
    members = cursor.fetchall()

    return members

def get_from_status(chat_id, status_m): #получить список людей, которые являются участниками чата согласно базе кузи (ВСЕХ ЛЮДЕЙ)
    cursor.execute(f"SELECT member_id FROM members WHERE chat_id = ? AND status_m = ?", (chat_id, status_m,))
    members = cursor.fetchall()

    return members


def set_status(chat_id, member_id, status_m): #Обновить статус юзера в чате
    cursor.execute("UPDATE members SET status_m = ? WHERE member_id = ? and chat_id = ?", (status_m, member_id, chat_id,))
    connect.commit()
