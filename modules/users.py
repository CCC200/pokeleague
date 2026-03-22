from uuid import uuid4
from sqlite3 import Connection, Error
from datetime import datetime

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='users'")
    if res.fetchone() is None:
        print('Creating users database...')
        con.execute("""
                    CREATE TABLE users(
                    sid varchar(18) PRIMARY KEY,
                    name varchar(30) NOT NULL UNIQUE,
                    pass varchar(15) NOT NULL,
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
            try:
                con.execute(f"INSERT INTO users VALUES(?,?,?,?)", (sid, name, __secret(15), datetime.now()))
                con.commit()
                res = con.execute(f"SELECT * FROM users WHERE sid='{sid}'")
                user = res.fetchone()
                print(f'Created user {user}')
                return user[0]
            except Error as e:
                print(f'User creation error: {e}')
            gen = False

def get(sid:str, con:Connection):
    res = con.execute(f"SELECT * FROM users WHERE sid='{sid}'")
    data = res.fetchone()
    if data:
        return {
            'sid': data[0],
            'name': data[1],
            'pass': data[2],
            'joindate': data[3]
        }

def get_credential(name:str, pwd:str, con:Connection):
    res = con.execute(f"SELECT * FROM users WHERE name='{name}' AND pass='{pwd}'")
    data = res.fetchone()
    if data:
        return {
            'sid': data[0],
            'name': data[1],
            'pass': data[2],
            'joindate': data[3]
        }

def __exists(name:str, con:Connection):
    res = con.execute(f"SELECT sid FROM users WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True

def __secret(len:int = 18):
    return str(uuid4()).replace('-', '')[:len]
