import os, sys, sqlite3
from modules import users, config, server, leagues, tournaments

# boot script
if '-clean' in sys.argv:
    print('This will wipe all data, including leagues and settings. Continue? (Y/N)')
    res = input('> ')
    if res.strip().lower() == 'y':
        if os.path.exists(config.DB_NAME):
            os.remove(config.DB_NAME)
        if os.path.exists('settings.json'):
            os.remove('settings.json')
# load modules
config.init()
con = sqlite3.connect(config.DB_NAME)
users.init(con)
leagues.init(con)
tournaments.init(con)
con.close()
server.init()
