from sqlite3 import Connection
from modules import leagues

def process(user:dict, head:str, body:str, con:Connection):
    if head == 'getleagues':
        return leagues.get_for(user['sid'], con)
    if head == 'joinleague':
        lid, sid = __split(body)
        return leagues.join(lid, sid, con)
    
def __split(body:str):
    s = body.split(',')
    return tuple(s)
