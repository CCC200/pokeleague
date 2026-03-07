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
                    name varchar(30) NOT NULL UNIQUE,
                    format varchar(30) NOT NULL,
                    bracket varchar(5) NOT NULL CHECK(bracket='se' OR bracket='de' OR bracket='swiss' OR bracket='rr'),
                    maxcap int NOT NULL,
                    poolsize int NOT NULL,
                    startdate datetime NOT NULL,
                    enddate datetime,
                    FOREIGN KEY(lid) REFERENCES leagues(lid)
                    )
                    """)
    res = con.execute("SELECT name FROM sqlite_master WHERE name='entrants'")
    if res.fetchone() is None:
        print('Creating entrants database...')
        con.execute("""
                    CREATE TABLE entrants(
                    tid int NOT NULL,
                    sid varchar(18) NOT NULL,
                    joindate datetime NOT NULL,
                    FOREIGN KEY(tid) REFERENCES tournaments(tid),
                    FOREIGN KEY(sid) REFERENCES users(sid),
                    PRIMARY KEY(tid, sid)
                    )
                    """)
        
def register(lid:str, name:str, format:str, bracket:str, cap:int, poolsize:int, startdate:datetime, con:Connection):
    if not __exists(name, con):
        try:
            con.execute('PRAGMA foreign_keys = ON')
            con.execute("INSERT INTO tournaments(tid,lid,name,format,bracket,maxcap,poolsize,startdate) VALUES(NULL,?,?,?,?,?,?,?)", (lid, name, format, bracket, cap, poolsize, startdate))
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
    
def join(tid:str, sid:str, con:Connection):
    try:
        con.execute('PRAGMA foreign_keys = ON')
        con.execute(f"INSERT INTO entrants(tid,sid,joindate) VALUES(?,?,?)", (tid, sid, datetime.now()))
        con.commit()
        print(f'User {sid} joined tournament {tid}')
        return True
    except Error as e:
        print(f'Join tournament error: {e}')
        return False

def __exists(name:str, con:Connection):
    res = con.execute(f"SELECT tid FROM tournaments WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True
