import os, json

# default settings (overriden by settings.json)
league_name = 'My League'
address = '0.0.0.0'
port = 6500
rcon_port = 6501
buffer = 1024

def init():
    if os.path.exists('_config/settings.json'):
        with open('_config/settings.json', 'r') as file:
            data = json.loads(file.read())
        if 'league_name' in data:
            global league_name
            league_name = data['league_name']
        if 'address' in data:
            global address
            address = data['address']
        if 'port' in data:
            global port
            port = data['port']
        if 'rcon_port' in data:
            global rcon_port
            rcon_port = data['rcon_port']
    else:
        print('Creating settings.json...')
        settings = {
            'league_name': league_name,
            'address': address,
            'port': port,
            'rcon_port': rcon_port
        }
        with open('_config/settings.json', 'w') as file:
            file.write(json.dumps(settings, indent=4))
