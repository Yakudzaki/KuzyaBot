import sqlite3
import html
from app import db_file
path = db_file 

connect = sqlite3.connect(path, timeout=10)
cursor = connect.cursor()

print(f"sqlite version - {sqlite3.sqlite_version}")
cursor.execute("pragma foreign_keys=on;")

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id    INTEGER UNIQUE ON CONFLICT IGNORE,
    username   TEXT    UNIQUE ON CONFLICT IGNORE,
    nick       TEXT,
    bio        TEXT,
    gender     INTEGER,
    reputation INTEGER,
    age        INTEGER DEFAULT (20),
    specie     TEXT,
    moniker    TEXT    NOT NULL DEFAULT '',
    ban        INTEGER DEFAULT (0),
    clan_id    INTEGER REFERENCES clans (id) ON DELETE SET NULL,
    balance    INTEGER DEFAULT (5000),
    marry_id   INTEGER REFERENCES users (user_id) ON DELETE SET NULL,
    FOREIGN KEY (
        clan_id
    )
    REFERENCES clans (id),
    FOREIGN KEY (
        marry_id
    )
    REFERENCES users (user_id) ON DELETE SET NULL,
    FOREIGN KEY (
        clan_id
    )
    REFERENCES clans (id) ON DELETE SET NULL,
    PRIMARY KEY (
        user_id
    )
    ON CONFLICT IGNORE
    )
""")

connect.commit()


def get_user(id):

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (id,))
    user = cursor.fetchone()
    return user


def check_nick(nick):

    cursor.execute("SELECT * FROM users WHERE nick=?", (nick,))
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True


def create_user(user_id, username, nick):
    user = get_user(user_id)
    if user != None:
        return user
    else:
        user = create_user_main(user_id, username, nick)
        return user


def create_user_main(user_id, username, nick):
    
    if username == None:
        username = str(user_id)

    if check_username(username):
        create_user_simpe(user_id, username, nick)
        user = [user_id, username, nick, "Нет", 0, 0, 20, "Человек", "", 0, None, 5000, None]
        return user
    
    else:
        user = get_username(username)
        if user[0] != user_id:
            set_username_simple(user[0], str(user[0]))
            create_user_simpe(user_id, username, nick)
            user = [user_id, username, nick, "Нет", 0, 0, 20, "Человек", "", 0, None, 5000, None]
            return user
        else:
            return user

def create_user_simpe(user_id, username, nick):
    cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (user_id, username, nick, "Нет", 0, 0, 20, "Человек", "", 0, None, 5000, None, ))
    print(f"Создан юзер {user_id} {username} {nick}")
    connect.commit()

def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    connect.commit()
    print(f"Удалён юзер {user_id}")

def check_user(user_id):

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result is None:
        return True
    else:
        return False



def check_username(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    if result is None:
        return True
    else:
        return False



def get_username(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    return user



def set_nick(user_id, nick):
    cursor.execute("UPDATE users SET nick = ? WHERE user_id = ?", (nick, user_id,))
    connect.commit()



def set_bio(user_id, bio):
    cursor.execute("UPDATE users SET bio = ? WHERE user_id = ?", (bio, user_id,))
    connect.commit()


def set_gender(user_id, gender):
    cursor.execute("UPDATE users SET gender = ? WHERE user_id = ?", (gender, user_id,))
    connect.commit()

def set_specie(user_id, specie):
    cursor.execute("UPDATE users SET specie = ? WHERE user_id = ?", (specie, user_id,))
    connect.commit()

def set_username_simple(user_id, username):
    cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id,))
    connect.commit()


def set_username(user_id, username):
    
    if check_username(username):
        set_username_simple(user_id, username)
        return
    
    else:
        user = get_username(username)
        if user[0] != user_id:
            set_username_simple(user[0], str(user[0]))
            set_username_simple(user_id, username)
            return
        else:
            return

def set_moniker(user_id, moniker):
    cursor.execute("UPDATE users SET moniker = ? WHERE user_id = ?", (moniker, user_id,))
    connect.commit()

def set_ban(user_id, ban):
    cursor.execute("UPDATE users SET ban = ? WHERE user_id = ?", (ban, user_id,))
    connect.commit()

def set_age(user_id, age):
    cursor.execute("UPDATE users SET age = ? WHERE user_id = ?", (age, user_id,))
    connect.commit()


def add_rep(user_id):
    cursor.execute("UPDATE users SET reputation = reputation + 1 WHERE user_id = ?", (user_id,))
    connect.commit()



def take_rep(user_id):
    cursor.execute("UPDATE users SET reputation = reputation - 1 WHERE user_id = ?", (user_id,))
    connect.commit()

def get_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return users



