import sys, sqlite3
from modules import config, users, leagues

args = sys.argv
args.pop(0)
con = sqlite3.connect(config.DB_NAME)
if args[0] == '-registeruser':
    users.init(con)
    users.register(args[1], con)
elif args[0] == '-registerleague':
    leagues.init(con)
    leagues.register(args[1], args[2], con)
elif args[0] == '-joinleague':
    leagues.init(con)
    leagues.join(args[1], args[2], con)
con.close()
