import os, sys, shutil, asyncio
from modules import users, config, server

# boot script
if '-clean' in sys.argv:
    print('This will wipe all data, including leagues and settings. Continue? (Y/N)')
    res = input('> ')
    if res.lower() == 'y':
        shutil.rmtree('_db')
        shutil.rmtree('_config')
if not os.path.isdir('_db'):
    os.mkdir('_db')
if not os.path.isdir('_config'):
    os.mkdir('_config')
# load modules
config.init()
users.init()
# start server threads
asyncio.run(server.start())
