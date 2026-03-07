from sqlite3 import Connection
from modules import leagues

# user commands
REGISTER_USER = 'registeruser'

# league commands
REGISTER_LEAGUE = 'registerleague'
GET_LEAGUES = 'getleagues'
JOIN_LEAGUE = 'joinleague'

# tournament commands
REGISTER_TOURNAMENT = 'registertournament'

def process(user:dict, head:str, body:str, con:Connection):
    if head == GET_LEAGUES:
        return leagues.get_for(user['sid'], con)
    if head == JOIN_LEAGUE:
        lid, sid = __split(body)
        return leagues.join(lid, sid, con)
    
def __split(body:str):
    s = body.split(',')
    return tuple(s)
