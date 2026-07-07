import os, json

DB_NAME = 'pokeleague.db'

# optional settings (only in settings.json)
discord_token:str = None
challonge_key:str = None

def init():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as file:
            data = json.loads(file.read())
        if 'discord_token' in data:
            global discord_token
            discord_token = data['discord_token']
        if 'challonge_key' in data:
            global challonge_key
            challonge_key = data['challonge_key']
    else:
        print('Creating settings.json...')
        settings = {}
        with open('settings.json', 'w') as file:
            file.write(json.dumps(settings, indent=4))
