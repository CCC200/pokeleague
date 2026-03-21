import sys, sqlite3
from datetime import datetime
from modules import config, request, users, leagues, tournaments
from extensions import challonge_ext, discord_ext

args = sys.argv
args.pop(0)
config.init()
con = sqlite3.connect(config.DB_NAME)
if args[0] == request.REGISTER_USER:
    users.init(con)
    users.register(args[1], con)
elif args[0] == request.REGISTER_LEAGUE:
    leagues.init(con)
    leagues.register(args[1], con)
elif args[0] == request.ADD_MANAGER:
    leagues.init(con)
    leagues.add_manager(args[1], args[2], con)
elif args[0] == request.REGISTER_TOURNAMENT:
    tournaments.init(con)
    tournaments.register(args[1], args[2], args[3], args[4], args[5], args[6], datetime.fromisoformat(args[7]), con)
elif args[0] == request.JOIN_TOURNAMENT:
    tournaments.init(con)
    tournaments.join(args[1], args[2], con)
# challonge extension
elif args[0] == 'challonge':
    challonge_ext.init(con)
    if args[1] == 'createbracket':
        challonge_ext.create_bracket(args[2], con)
# discord extension
elif args[0] == 'discord':
    discord_ext.init(con)
    if args[1] == 'linkaccount':
        discord_ext.link_account(args[2], args[3], con)
con.close()
