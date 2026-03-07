from sqlite3 import Connection, Error
from datetime import datetime

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='tournaments'")
    if res.fetchone() is None:
        print('Creating tournaments database...')
        con.execute("""
                    CREATE TABLE tournaments(
                    tid INTEGER PRIMARY KEY AUTOINCREMENT,
                    lid int NOT NULL,
                    name varchar(30) NOT NULL,
                    maxcap int NOT NULL,
                    startdate datetime NOT NULL,
                    enddate datetime,
                    FOREIGN KEY(lid) REFERENCES leagues(lid)
                    )
                    """)
    res = con.execute("SELECT name FROM sqlite_master WHERE name='draft'")
    if res.fetchone() is None:
        print('Creating draft database...')
        con.execute("""
                    CREATE TABLE draft(
                    tid INTEGER PRIMARY KEY,
                    mon varchar(15) NOT NULL,
                    price int NOT NULL,
                    FOREIGN KEY(tid) REFERENCES tournaments(tid)
                    )
                    """)
        
def register(lid:str, name:str, cap:int, startdate:datetime, con:Connection):
    if not __exists(name, con):
        try:
            con.execute('PRAGMA foreign_keys = ON')
            con.execute("INSERT INTO tournaments(tid,lid,name,maxcap,startdate) VALUES(NULL,?,?,?,?)", (lid, name, cap, startdate))
            con.commit()
            res = con.execute(f"SELECT * FROM tournaments WHERE name='{name}'")
            print(f'Created tournament {res.fetchone()}')
            return True
        except Error as e:
            print(f'Register tournament error: {e}')
            return False
    else:
        print(f'Tournament {name} already exists, aborting')
        return False

def __exists(name:str, con:Connection):
    res = con.execute(f"SELECT tid FROM tournaments WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True
