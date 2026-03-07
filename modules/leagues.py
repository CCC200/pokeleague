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
    res = con.execute("SELECT name FROM sqlite_master WHERE name='managers'")
    if res.fetchone() is None:
        print('Creating managers database...')
        con.execute("""
                    CREATE TABLE managers(
                    lid int NOT NULL,
                    sid varchar(18) NOT NULL,
                    FOREIGN KEY(lid) REFERENCES leagues(lid),
                    FOREIGN KEY(sid) REFERENCES users(sid)
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

def get_for(sid:str, con:Connection):
    res = con.execute(f"SELECT l.lid,l.name FROM leagues l LEFT JOIN managers m ON m.lid=l.lid WHERE m.sid ='{sid}'")
    return res.fetchall()

def add_manager(lid:str, sid:str, con:Connection):
    try:
        con.execute("INSERT INTO managers(lid, sid) VALUES(?,?)", (lid, sid))
        con.commit()
        print(f'Added manager {sid} to {lid}')
        return True
    except Error as e:
        print(f'Add manager failed: {e}')
        return False

def __exists(name:str, con:Connection):
    res = con.execute(f"SELECT lid FROM leagues WHERE name='{name}'")
    if res.fetchone() is None:
        return False
    return True
