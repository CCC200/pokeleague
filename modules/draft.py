from sqlite3 import Connection

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='draft_list'")
    if res.fetchone() is None:
        print('Creating draft list database...')
        con.execute("""
                    CREATE TABLE draft_list(
                    mid INTEGER PRIMARY KEY AUTOINCREMENT,
                    tid int NOT NULL,
                    mon varchar(15) NOT NULL,
                    price int NOT NULL,
                    FOREIGN KEY(tid) REFERENCES tournaments(tid)
                    )
                    """)
    res = con.execute("SELECT name FROM sqlite_master WHERE name='draft_picks'")
    if res.fetchone() is None:
        print('Creating draft pick database...')
        con.execute("""
                    CREATE TABLE draft_picks(
                    did INTEGER PRIMARY KEY AUTOINCREMENT,
                    sid varchar(18) NOT NULL,
                    mid_pickup int NOT NULL,
                    mid_drop int,
                    picktype varchar(5) CHECK(picktype='draft' OR picktype='trade' OR picktype='fa'),
                    FOREIGN KEY(sid) REFERENCES users(sid),
                    FOREIGN KEY(mid_pickup) REFERENCES draft_list(mid),
                    FOREIGN KEY(mid_drop) REFERENCES draft_list(mid)
                    )
                    """)
