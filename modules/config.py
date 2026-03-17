import os, json

DB_NAME = 'pokeleague.db'
BUFFER_SIZE = 1024

# default settings (overriden by settings.json)
address = '0.0.0.0'
port = 6500
max_login_time = 600
max_idle_time = 1800

# optional settings (only in settings.json)
discord_token:str = None

def init():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as file:
            data = json.loads(file.read())
        if 'address' in data:
            global address
            address = data['address']
        if 'port' in data:
            global port
            port = data['port']
        if 'max_login_time' in data:
            global max_login_time
            max_login_time = data['max_login_time']
        if 'max_idle_time' in data:
            global max_idle_time
            max_idle_time = data['max_idle_time']
        if 'discord_token' in data:
            global discord_token
            discord_token = data['discord_token']
    else:
        print('Creating settings.json...')
        settings = {
            'address': address,
            'port': port,
            'max_login_time': max_login_time,
            'max_idle_time': max_idle_time,
        }
        with open('settings.json', 'w') as file:
            file.write(json.dumps(settings, indent=4))
