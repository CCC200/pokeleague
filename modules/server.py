import socket, asyncio
from modules import config

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

# doesn't work rn
async def start_rcon():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config.address, config.rcon_port))
    server.listen()
    server.setblocking(False)
    print(f'RCON bound to {config.address}:{config.port}')
    events = asyncio.get_event_loop()
    while True:
        client, ip = await events.sock_accept(server)
        print(f'RCON connected: {ip}')
        events.create_task(__rcon_login__(client, ip))

async def __rcon_login__(client:socket.socket, ip):
    events = asyncio.get_event_loop()
    await events.sock_sendall(client, __buffer__('RCON connected, enter commands:'))
    try:
        while True:
            await asyncio.wait_for(__rcon_cmd__, 180)
    except asyncio.TimeoutError:
        await events.sock_sendall(client, __buffer__('Timeout disconnect'))
        client.close()

async def __rcon_cmd__(client:socket.socket, ip):
    events = asyncio.get_event_loop()
    req = (await events.sock_recv(client, config.buffer)).decode().strip()
    if len(req) == 0:
        return
    print(req)

def __buffer__(msg:str, end='\n'):
    buf = f'{msg}{end}'
    return buf.encode()
