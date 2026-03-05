import sqlite3, uuid
from datetime import datetime

__DB_NAME = '_db/users.db'

def init():
    con = sqlite3.connect(__DB_NAME)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE name='users'")
    if res.fetchone() is None:
        print('Creating users database...')
        cur.execute("""
                    CREATE TABLE users(
                    sid varchar(18) PRIMARY KEY,
                    name varchar(30) NOT NULL,
                    joindate date NOT NULL
                    )
                    """)
    con.close()

def register(name:str):
    con = sqlite3.connect(__DB_NAME)
    cur = con.cursor()
    if __exists__(cur, name):
        print(f'User {name} already exists, aborting register')
        return
    gen = True
    while(gen):
        sid = __secret__()
        res = cur.execute(f"SELECT sid FROM users WHERE sid='{sid}'")
        if res.fetchone() is None:
            res = cur.execute(f"INSERT INTO users VALUES(?,?,?)", (sid, name, datetime.now()))
            con.commit()
            res = cur.execute(f"SELECT * FROM users WHERE sid='{sid}'")
            print(f'Created user {res.fetchone()}')
            gen = False
    con.close()

def get(sid:str):
    con = sqlite3.connect(__DB_NAME)
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM users WHERE sid='{sid}'")
    data = res.fetchone()
    if data is None:
        print(f'User matching {sid} does not exist')
        return
    u = {
        'sid': data[0],
        'name': data[1],
        'joindate': data[2]
    }
    return u

def __exists__(cur:sqlite3.Cursor, name:str):
    res = cur.execute(f"SELECT sid FROM users WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True

def __secret__():
    return str(uuid.uuid4()).replace('-', '')[:18]
