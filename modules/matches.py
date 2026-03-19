from sqlite3 import Connection, Error

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='matches'")
    if res.fetchone() is None:
        print('Creating matches database...')
        con.execute("""
                    CREATE TABLE matches(
                    matchid text PRIMARY KEY,
                    tid int NOT NULL,
                    p1_sid varchar(18),
                    p2_sid varchar(18),
                    FOREIGN KEY(tid) REFERENCES tournaments(tid),
                    FOREIGN KEY(p1_sid) REFERENCES users(sid),
                    FOREIGN KEY(p2_sid) REFERENCES users(sid)
                    )
                    """)
    res = con.execute("SELECT name FROM sqlite_master WHERE name='replays'")
    if res.fetchone() is None:
        print('Creating replays database...')
        con.execute("""
                    CREATE TABLE replays(
                    replayid INTEGER PRIMARY KEY AUTOINCREMENT,
                    matchid text NOT NULL,
                    url text NOT NULL,
                    replaytime datetime NOT NULL,
                    FOREIGN KEY(matchid) REFERENCES matches(matchid)
                    )
                    """)
