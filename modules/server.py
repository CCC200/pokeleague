import socket, asyncio
from modules import config, users

def init():
    asyncio.run(__start())
    print('Server escaped task')

async def __start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config.address, config.port))
    server.listen()
    server.setblocking(False)
    print(f'Bound to {config.address}:{config.port}')
    events = asyncio.get_event_loop()
    while True:
        client, ip = await events.sock_accept(server)
        print(f'Connected: {ip}')
        events.create_task(__login_thread(client, ip))

async def __login_thread(client:socket.socket, ip):
    events = asyncio.get_event_loop()
    try:
        user = await asyncio.wait_for(__handle_login(client), config.max_login)
        print(f'Login: {user}')
    except asyncio.TimeoutError:
        print(f'Login timeout: {ip}')
        await events.sock_sendall(client, __buffer('error', 'timeout'))
        client.close()

async def __handle_login(client:socket.socket):
    events = asyncio.get_event_loop()
    await events.sock_sendall(client, __buffer('login', 'wait'))
    while True:
        req = await events.sock_recv(client, config.buffer)
        cmd, body = __decode(req)
        if cmd == 'login':
            user = users.get(body)
            if user is None:
                await events.sock_sendall(client, __buffer('error', 'badSID'))
            else:
                await events.sock_sendall(client, __buffer('login', f'{user['name']},{user['joindate']}'))
                return user
        else:
            await events.sock_sendall(client, __buffer('error', 'nologin'))

def __buffer(cmd:str, body:str):
    buf = f'{cmd}|{body}'
    return buf.encode()

def __decode(req:bytes):
    d = req.decode().strip()
    s = d.split('|')
    return tuple(s)
