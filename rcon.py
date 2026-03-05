import sys
from modules import users

cmd = sys.argv[1]
body = sys.argv[2]
if cmd == '-register':
    users.init()
    users.register(body)
