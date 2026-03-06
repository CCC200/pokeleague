import os, sys
from modules import users, config, server, leagues

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
users.init()
leagues.init()
server.init()
