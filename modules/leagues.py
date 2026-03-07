from sqlite3 import Connection, Error
from datetime import datetime

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='leagues'")
    if res.fetchone() is None:
        print('Creating leagues database...')
        con.execute("""
                    CREATE TABLE leagues(
                    lid INTEGER PRIMARY KEY AUTOINCREMENT,
                    name varchar(30) NOT NULL UNIQUE,
                    createdate datetime NOT NULL
                    )
                    """)
    res = con.execute("SELECT name FROM sqlite_master WHERE name='members'")
    if res.fetchone() is None:
        print('Creating members database...')
        con.execute("""
                    CREATE TABLE members(
                    lid int PRIMARY KEY NOT NULL,
                    sid varchar(18) NOT NULL,
                    manager boolean NOT NULL DEFAULT FALSE,
                    regdate datetime NOT NULL,
                    FOREIGN KEY(sid) REFERENCES users(sid),
                    FOREIGN KEY(lid) REFERENCES leagues(lid)
                    )
                    """)

def register(name:str, con:Connection):
    if not __exists(name, con):
        try:
            con.execute("INSERT INTO leagues(lid,name,createdate) VALUES(NULL,?,?)", (name, datetime.now()))
            con.commit()
            res = con.execute(f"SELECT * FROM leagues WHERE name='{name}'")
            print(f'Created league {res.fetchone()}')
        except Error as e:
            print(f'Register league failed: {e}')
    else:
        print(f'League {name} already exists, aborting')

def join(lid:str, sid:str, con:Connection):
    res = con.execute(f"SELECT rowid FROM members WHERE lid='{lid}' AND sid='{sid}'")
    if res.fetchone() is None:
        try:
            con.execute('PRAGMA foreign_keys = ON')
            con.execute('INSERT INTO members(lid,sid,regdate) VALUES(?,?,?)', (lid, sid, datetime.now()))
            con.commit()
            print(f'User {sid} joined league {lid}')
            return True
        except Error as e:
            print(f'Join league error: {e}')
            return False
    else:
        print(f'User {sid} already joined league {lid}, aborting')
        return False

def get_for(sid:str, con:Connection):
    res = con.execute(f"SELECT l.lid,l.name FROM leagues l LEFT JOIN members m ON m.lid=l.lid WHERE m.sid ='{sid}'")
    return res.fetchall()

def __exists(name:str, con:Connection):
    res = con.execute(f"SELECT lid FROM leagues WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True
