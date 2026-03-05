import socket, asyncio
from modules import config, users

async def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config.address, config.port))
    server.listen()
    server.setblocking(False)
    print(f'Bound to {config.address}:{config.port}')
    events = asyncio.get_event_loop()
    while True:
        client, ip = await events.sock_accept(server)
        print(f'Connected: {ip}')
        events.create_task(login_thread(client, ip))

async def login_thread(client:socket.socket, ip):
    events = asyncio.get_event_loop()
    try:
        user = await asyncio.wait_for(handle_login(client), config.max_login)
        print(f'Login: {user}')
    except asyncio.TimeoutError:
        print(f'Login timeout: {ip}')
        await events.sock_sendall(client, __buffer__('error', 'timeout'))
        client.close()

async def handle_login(client:socket.socket):
    events = asyncio.get_event_loop()
    await events.sock_sendall(client, __buffer__('login', 'wait'))
    while True:
        req = await events.sock_recv(client, config.buffer)
        cmd, body = __decode__(req)
        if cmd == 'login':
            user = users.get(body)
            if user is None:
                await events.sock_sendall(client, __buffer__('error', 'badSID'))
            else:
                await events.sock_sendall(client, __buffer__('login', f'{user['name']},{user['joindate']}'))
                return user
        else:
            await events.sock_sendall(client, __buffer__('error', 'nologin'))

def __buffer__(cmd:str, body:str):
    buf = f'{cmd}|{body}'
    return buf.encode()

def __decode__(req:bytes):
    d = req.decode().strip()
    s = d.split('|')
    return s[0], s[1]
