import os, json

# default settings (overriden by settings.json)
DB_NAME = '_db/pokeleague.db'
address = '0.0.0.0'
port = 6500
buffer = 1024
max_login = 600

def init():
    if os.path.exists('_config/settings.json'):
        with open('_config/settings.json', 'r') as file:
            data = json.loads(file.read())
        if 'address' in data:
            global address
            address = data['address']
        if 'port' in data:
            global port
            port = data['port']
    else:
        print('Creating settings.json...')
        settings = {
            'address': address,
            'port': port,
        }
        with open('_config/settings.json', 'w') as file:
            file.write(json.dumps(settings, indent=4))
