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
                    bracket varchar(5) NOT NULL CHECK(bracket='se' OR bracket='de' OR bracket='swiss' OR bracket='rr' OR bracket='rr-se'),
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
                    FOREIGN KEY(sid) REFERENCES users(sid)
                    )
                    """)
    res = con.execute("SELECT name FROM sqlite_master WHERE name='matches'")
    if res.fetchone() is None:
        print('Creating matches database...')
        con.execute("""
                    CREATE TABLE matches(
                    matchid INTEGER PRIMARY KEY AUTOINCREMENT,
                    tid int NOT NULL,
                    p1 varchar(30) NOT NULL,
                    p2 varchar(30) NOT NULL,
                    maxrounds int NOT NULL CHECK(maxrounds >= 1 AND maxrounds <= 5),
                    score1 int NOT NULL DEFAULT 0 CHECK(score1 >= -1 AND score1 <= 3),
                    score2 int NOT NULL DEFAULT 0 CHECK(score2 >= -1 AND score2 <= 3),
                    matchdate datetime,
                    FOREIGN KEY(tid) REFERENCES tournaments(tid),
                    FOREIGN KEY(p1) REFERENCES users(name),
                    FOREIGN KEY(p2) REFERENCES users(name)
                    )
                    """)
        
def register(lid:str, name:str, bracket:str, cap:int, pools:int, startdate:datetime, con:Connection):
    if not __exists(name, con):
        try:
            con.execute('PRAGMA foreign_keys = ON')
            con.execute("INSERT INTO tournaments(tid,lid,name,bracket,maxcap,poolsize,startdate) VALUES(NULL,?,?,?,?,?,?)", (lid, name, bracket, cap, pools, startdate))
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
