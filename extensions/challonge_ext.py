import requests, re
from sqlite3 import Connection
from modules import config, tournaments

BASE_URL = 'https://api.challonge.com/v2.1'

def verify_key():
    print(f'Challonge API login: {__get_req('/me.json')}')

def create_bracket(tid:int, con:Connection):
    tourn = tournaments.get(tid, con)
    body = {
        'data': {
            'attributes': {
                'name': tourn[2],
                'url': f'pokeleague_{__flatten_name(tourn[2])}',
                'game_name': 'Pokémon Showdown',
                'tournament_type': __convert_bracket_type(tourn[4]),
                'starts_at': tourn[7],
                'registration_options': {
                    'signup_cap': tourn[5]
                }
            }
        }
    }
    res = __post_req('/tournaments.json', body)
    if res.status_code == 201:
        json = res.json()
        print(f'Tournament created at: {json['data']['attributes']['full_challonge_url']}')
        entrants = tournaments.get_entrants(tid, con)
        if len(entrants) == 0:
            return
        body = {
            'data': {
                'attributes': {
                    'participants': []
                }
            }
        }
        for tup in entrants:
            body['data']['attributes']['participants'].append({
                'name': tup[1],
                'misc': tup[0]
            })
        res = __post_req(f'/tournaments/{json['data']['id']}/participants/bulk_add.json', body)
        if res.status_code == 200:
            print(f'Added {len(res.json()['data'])} players to tournament')
        else:
            print(f'Error:\n{res.json()}')
    else:
        print(f'Error:\n{res.json()}')

def __get_req(route:str, params:dict = None):
    req = requests.get(BASE_URL + route, headers=__base_headers(), json=params)
    return req

def __post_req(route:str, params:dict):
    req = requests.post(BASE_URL + route, headers=__base_headers(), json=params)
    return req

def __base_headers():
    return {
        'User-Agent': 'Chrome',
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/json',
        'Authorization-Type': 'v1',
        'Authorization': config.challonge_key
    }

def __convert_bracket_type(t:str):
    if t == 'se':
        return 'single elimination'
    elif t == 'de':
        return 'double elimination'
    elif t == 'rr':
        return 'round robin'
    else:
        return t
    
def __flatten_name(n:str):
    n = n.replace(' ', '')
    return re.sub(r'[^a-zA-Z0-9]', '', n)
