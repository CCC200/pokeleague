from sqlite3 import Connection
from modules import leagues, users

# user commands
LOGIN = 'login'
REGISTER_USER = 'registeruser'

# league commands
REGISTER_LEAGUE = 'registerleague'
GET_LEAGUES = 'getleagues'
ADD_MANAGER = 'addmanager'

# tournament commands
REGISTER_TOURNAMENT = 'registertournament'
JOIN_TOURNAMENT = 'jointournament'

def process(user:dict, head:str, body:str, con:Connection):
    if head == GET_LEAGUES:
        return leagues.get_for(user['sid'], con)
    
def process_login(head:str, body:str, con:Connection):
    if head == LOGIN:
        name, pwd = __split(body)
        return users.get_credential(name, pwd, con)
    
def __split(body:str):
    s = body.split(',')
    return tuple(s)
