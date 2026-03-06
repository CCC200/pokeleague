import sys
from modules import users, leagues

args = sys.argv
args.pop(0)
if args[0] == '-registeruser':
    users.init()
    users.register(args[1])
elif args[0] == '-registerleague':
    leagues.init()
    leagues.register(args[1], args[2])
elif args[0] == '-joinleague':
    leagues.init()
    leagues.join(args[1], args[2])
