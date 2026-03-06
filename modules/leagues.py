import sqlite3
from datetime import datetime
from modules import config

def init():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master WHERE name='leagues'")
    if res.fetchone() is None:
        print('Creating leagues database...')
        cur.execute("""
                    CREATE TABLE leagues(
                    lid INTEGER PRIMARY KEY AUTOINCREMENT,
                    name varchar(30) NOT NULL,
                    maxcap int NOT NULL DEFAULT 16,
                    createdate datetime NOT NULL
                    )
                    """)
    res = cur.execute("SELECT name FROM sqlite_master WHERE name='members'")
    if res.fetchone() is None:
        print('Creating members database...')
        cur.execute("""
                    CREATE TABLE members(
                    lid int NOT NULL,
                    sid varchar(18) NOT NULL,
                    manager boolean NOT NULL DEFAULT FALSE,
                    regdate datetime NOT NULL,
                    FOREIGN KEY(sid) REFERENCES users(sid),
                    FOREIGN KEY(lid) REFERENCES leagues(lid)
                    )
                    """)
    con.close()

def register(name:str, cap:int=16):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    if not __exists(cur, name):
        cur.execute("INSERT INTO leagues(lid,name,maxcap,createdate) VALUES(NULL,?,?,?)", (name, cap, datetime.now()))
        con.commit()
        res = cur.execute(f"SELECT * FROM leagues WHERE name='{name}'")
        print(f'Created league {res.fetchone()}')
    else:
        print(f'League {name} already exists, aborting')
    con.close()

def join(lid:str, sid:str):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    res = cur.execute(f"SELECT rowid FROM members WHERE lid='{lid}' AND sid='{sid}'")
    if res.fetchone() is None:
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute('INSERT INTO members(lid,sid,regdate) VALUES(?,?,?)', (lid, sid, datetime.now()))
        con.commit()
        print(f'User {sid} joined league {lid}')
    else:
        print(f'User {sid} already joined league {lid}, aborting')
    con.close()

def __exists(cur:sqlite3.Cursor, name:str):
    res = cur.execute(f"SELECT lid FROM leagues WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True
