import sqlite3
from app import db_file
path = db_file 
import logging


connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS chats(
    chat_id         INTEGER UNIQUE ON CONFLICT IGNORE,
    vermat INTEGER,
    secmat INTEGER,
    roul_mut_mod INTEGER,
    funny_func INTEGER,
    welcome1 TEXT NOT NULL DEFAULT '',
    welcome2 TEXT NOT NULL DEFAULT '',
    matrep INTEGER,
    photo_limit INTEGER,
    text_limit INTEGER,
    video_limit INTEGER,
    anmiation_limit INTEGER,
    sticker_limit INTEGER,
    shield INTEGER,
    chat_info TEXT NOT NULL DEFAULT '',
    m_count INTEGER,
    rules TEXT NOT NULL DEFAULT ''
    )
""")

connect.commit()



def create_chat(chat_id):

    cursor.execute("INSERT INTO chats VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (chat_id, 0, 0, 0, 1, "Привет, ", "! Рады видеть тебя в нашем чате!", 0, 10, 10, 10, 10, 10, 0, "None", 0, "",))
    connect.commit()


def create_chat_with_info(chat_id, chat_info):
       
    cursor.execute("INSERT INTO chats VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (chat_id, 0, 0, 0, 1, "Привет, ", "! Рады видеть тебя в нашем чате!", 0, 10, 10, 10, 10, 10, 0, chat_info, 0, "",))
    connect.commit()


def check_chat(chat_id):
    cursor.execute("SELECT * FROM chats WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    if result is None:
        return True
    else:
        return False


    

def get_chat(id):

    cursor.execute("SELECT * FROM chats WHERE chat_id = ?", (id,))
    chat = cursor.fetchone()
    return chat


def set_chat_info(chat_id, chat_info):
    cursor.execute("UPDATE chats SET chat_info = ? WHERE chat_id = ?", (chat_info, chat_id,)) #Шанс антимата
    connect.commit()
    
def set_rules(chat_id, rules):
    cursor.execute("UPDATE chats SET rules = ? WHERE chat_id = ?", (rules, chat_id,)) #Установить ссылку на правила чата
    connect.commit()


def set_vermat(chat_id, vermat):
    cursor.execute("UPDATE chats SET vermat = ? WHERE chat_id = ?", (vermat, chat_id,)) #Шанс антимата
    connect.commit()

def set_secmat(chat_id, secmat):
    cursor.execute("UPDATE chats SET secmat = ? WHERE chat_id = ?", (secmat, chat_id,)) #Мут антимата
    connect.commit()

def set_matrep(chat_id, matrep):
    cursor.execute("UPDATE chats SET matrep = ? WHERE chat_id = ?", (matrep, chat_id,))  #Падение репутации от мата
    connect.commit()



def set_roul_mut_mod(chat_id, roul_mut_mod):
    cursor.execute("UPDATE chats SET roul_mut_mod = ? WHERE chat_id = ?", (roul_mut_mod, chat_id,)) #Заряд рулетки
    connect.commit()
    


def set_funny_func(chat_id, funny_func):
    cursor.execute("UPDATE chats SET funny_func = ? WHERE chat_id = ?", (funny_func, chat_id,)) #Развлекательные функции. 1 - включены, 0 - выключены.
    connect.commit()

def set_shield(chat_id, shield):
    cursor.execute("UPDATE chats SET shield = ? WHERE chat_id = ?", (shield, chat_id,)) #Шанс антимата
    connect.commit()



    


def set_welcome1(chat_id, welcome1):
    cursor.execute("UPDATE chats SET welcome1 = ? WHERE chat_id = ?", (welcome1, chat_id,))  #Часть приветствия до никнейма.
    connect.commit()
    
def set_welcome2(chat_id, welcome2):
    cursor.execute("UPDATE chats SET welcome2 = ? WHERE chat_id = ?", (welcome2, chat_id,))  #Часть приветствия после никнейма.
    connect.commit()
    



def set_members_count(chat_id, m_count):
    cursor.execute("UPDATE chats SET m_count = ? WHERE chat_id = ?", (m_count, chat_id,))  #Количество юзеров в чате
    connect.commit()





def set_photo_limit(chat_id, photo_limit):
    cursor.execute("UPDATE chats SET photo_limit = ? WHERE chat_id = ?", (photo_limit, chat_id,))  #лимит на фото
    connect.commit()
    
def set_text_limit(chat_id, text_limit):
    cursor.execute("UPDATE chats SET text_limit = ? WHERE chat_id = ?", (text_limit, chat_id,))  #лимит на текст
    connect.commit()

def set_video_limit(chat_id, video_limit):
    cursor.execute("UPDATE chats SET video_limit = ? WHERE chat_id = ?", (video_limit, chat_id,))  #лимит на видео
    connect.commit()
    
def set_anmiation_limit(chat_id, anmiation_limit):
    cursor.execute("UPDATE chats SET anmiation_limit = ? WHERE chat_id = ?", (anmiation_limit, chat_id,))  #лимит на гиф
    connect.commit()
    
def set_sticker_limit(chat_id, sticker_limit):
    cursor.execute("UPDATE chats SET sticker_limit = ? WHERE chat_id = ?", (sticker_limit, chat_id,))  #лимит на стикеры
    connect.commit()




#Отсюда и далее - База Чатов в оперативной памяти.
connect_m = sqlite3.connect(":memory:", timeout=10)
cursor_m = connect_m.cursor()


cursor_m.execute("""CREATE TABLE IF NOT EXISTS m_chats(
    chat_id         INTEGER UNIQUE ON CONFLICT IGNORE,
    hello_count INTEGER,
    hello_string TEXT,
    restricted INTEGER,
    time_up INTEGER,
    msg_id INTEGER
    )
""")

connect_m.commit()

logging.info('Создана таблица для чатов в оперативной памяти!')
print('| Создана таблица для чатов в оперативной памяти!')


def create_chat_m(chat_id):

    cursor_m.execute("INSERT INTO m_chats VALUES(?,?,?,?,?,?)", (chat_id, 0, "", 0, 0, 0,))
    connect_m.commit()

        
def check_chat_m(chat_id):
    cursor_m.execute("SELECT * FROM m_chats WHERE chat_id=?", (chat_id,))
    result = cursor_m.fetchone()
    if result is None:
        return True
    else:
        return False


def get_chat_m(id):

    cursor_m.execute("SELECT * FROM m_chats WHERE chat_id = ?", (id,))
    chat = cursor_m.fetchone()
    return chat


def set_hello_count(chat_id, hello_count):
    cursor_m.execute("UPDATE m_chats SET hello_count = ? WHERE chat_id = ?", (hello_count, chat_id,)) 
    connect_m.commit()
    


def set_hello_string(chat_id, hello_string):
    cursor_m.execute("UPDATE m_chats SET hello_string = ? WHERE chat_id = ?", (hello_string, chat_id,))
    connect_m.commit()
    
def set_time_up(chat_id, time_up):
    cursor_m.execute("UPDATE m_chats SET time_up = ? WHERE chat_id = ?", (time_up, chat_id,)) #переменная счетчика времени отключения стиков и гифок
    connect_m.commit()

def set_msg_id(chat_id, msg_id):
    cursor_m.execute("UPDATE m_chats SET msg_id = ? WHERE chat_id = ?", (msg_id, chat_id,)) #переменная с записью айди сообщения на которое нужно отвечать.
    connect_m.commit()
    
def set_chat_restricted(chat_id, restricted):
    cursor_m.execute("UPDATE m_chats SET restricted = ? WHERE chat_id = ?", (restricted, chat_id,)) #переменная для отключени стиков после постов с канала. Введена, чтобы не выкючать стики, когда они уже и так выключены.
    connect_m.commit()