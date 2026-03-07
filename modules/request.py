from sqlite3 import Connection
from modules import leagues

# user commands
REGISTER_USER = 'registeruser'

# league commands
REGISTER_LEAGUE = 'registerleague'
GET_LEAGUES = 'getleagues'
ADD_MANAGER = 'addmanager'

# tournament commands
REGISTER_TOURNAMENT = 'registertournament'

def process(user:dict, head:str, body:str, con:Connection):
    if head == GET_LEAGUES:
        return leagues.get_for(user['sid'], con)
    
def __split(body:str):
    s = body.split(',')
    return tuple(s)
