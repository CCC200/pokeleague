import requests
from modules import config

BASE_URL = 'https://api.challonge.com/v2.1'

def verify_key():
    print(f'Challonge API login: {__get_req('/me.json')}')

def __get_req(route:str, params:dict = None):
    req = requests.get(BASE_URL + route, headers=__base_headers(), params=params)
    return req

def __base_headers():
    return {
        'User-Agent': 'Chrome',
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/json',
        'Authorization-Type': 'v1',
        'Authorization': config.challonge_key
    }
