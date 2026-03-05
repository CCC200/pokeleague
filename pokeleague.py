import os, sys, shutil
from modules import users

# boot script
if '-clean' in sys.argv:
    shutil.rmtree('_db')
if not os.path.isdir('_db'):
    os.mkdir('_db')
users.init()
users.register('TestGuy')
