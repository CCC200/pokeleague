from uuid import uuid4
from sqlite3 import Connection
from datetime import datetime
from modules import config

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='users'")
    if res.fetchone() is None:
        print('Creating users database...')
        con.execute("""
                    CREATE TABLE users(
                    sid varchar(18) PRIMARY KEY,
                    name varchar(30) NOT NULL,
                    joindate datetime NOT NULL
                    )
                    """)

def register(name:str, con:Connection):
    if __exists(name, con):
        print(f'User {name} already exists, aborting register')
        return
    gen = True
    while(gen):
        sid = __secret()
        res = con.execute(f"SELECT sid FROM users WHERE sid='{sid}'")
        if res.fetchone() is None:
            con.execute(f"INSERT INTO users VALUES(?,?,?)", (sid, name, datetime.now()))
            con.commit()
            res = con.execute(f"SELECT * FROM users WHERE sid='{sid}'")
            print(f'Created user {res.fetchone()}')
            gen = False
    con.close()

def get(sid:str, con:Connection):
    res = con.execute(f"SELECT * FROM users WHERE sid='{sid}'")
    data = res.fetchone()
    if data is None:
        print(f"User matching '{sid}' does not exist")
        return
    u = {
        'sid': data[0],
        'name': data[1],
        'joindate': data[2]
    }
    return u

def __exists(name:str, con:Connection):
    res = con.execute(f"SELECT sid FROM users WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True

def __secret():
    return str(uuid4()).replace('-', '')[:18]
