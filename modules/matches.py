from sqlite3 import Connection, Error

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='matches'")
    if res.fetchone() is None:
        print('Creating matches database...')
        con.execute("""
                    CREATE TABLE matches(
                    matchid INTEGER PRIMARY KEY AUTOINCREMENT,
                    tid int NOT NULL,
                    p1_sid varchar(18),
                    p2_sid varchar(18),
                    maxgames int NOT NULL CHECK(maxgames >= 1 AND maxgames <= 5),
                    score1 int NOT NULL DEFAULT 0 CHECK(score1 >= -1 AND score1 <= 3),
                    score2 int NOT NULL DEFAULT 0 CHECK(score2 >= -1 AND score2 <= 3),
                    matchdate datetime,
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
                    matchid int NOT NULL,
                    url text NOT NULL,
                    replaytime datetime NOT NULL,
                    FOREIGN KEY(matchid) REFERENCES matches(matchid)
                    )
                    """)
