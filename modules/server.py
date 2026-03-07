import socket, asyncio, sqlite3
from modules import config, users, request

def init():
    asyncio.run(__start())
    print('\nServer closed')

async def __start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config.address, config.port))
    server.listen()
    server.setblocking(False)
    print(f'Bound to {config.address}:{config.port}')
    events = asyncio.get_event_loop()
    while True:
        try:
            client, ip = await events.sock_accept(server)
            print(f'Connected: {ip}')
            events.create_task(__login_thread(client, ip))
        except asyncio.CancelledError:
            server.close()
            break

async def __login_thread(client:socket.socket, ip):
    events = asyncio.get_event_loop()
    con = sqlite3.connect(config.DB_NAME)
    try:
        user = await asyncio.wait_for(__handle_login(client, con), config.max_login_time)
        print(f'Login: {user}')
        events.create_task(__request_thread(client, user, con))
    except asyncio.TimeoutError:
        print(f'Login timeout: {ip}')
        await events.sock_sendall(client, __encode('error', 'timeout'))
        client.close()
        con.close()
    except BrokenPipeError:
        print(f'Disconnect during login: {ip}')
        client.close()
        con.close()

async def __handle_login(client:socket.socket, con:sqlite3.Connection):
    events = asyncio.get_event_loop()
    await events.sock_sendall(client, __encode('login', 'wait'))
    while True:
        req = await events.sock_recv(client, config.BUFFER_SIZE)
        head, body = __decode(req)
        if head == 'login':
            user = users.get(body, con)
            if user is not None:
                await events.sock_sendall(client, __encode('login', f'{user['name']},{user['joindate']}'))
                return user
            else:
                await events.sock_sendall(client, __encode('error', 'badSID'))
        else:
            await events.sock_sendall(client, __encode('error', 'nologin'))

async def __request_thread(client:socket.socket, user:dict, con:sqlite3.Connection):
    events = asyncio.get_event_loop()
    while True:
        try:
            req = await asyncio.wait_for(events.sock_recv(client, config.BUFFER_SIZE), config.max_idle_time)
            if len(req) == 0:
                print(f'User {user['sid']} disconnected')
                break
            head, body = __decode(req)
            res = request.process(user, head, body, con)
            if res is not None:
                await events.sock_sendall(client, __encode(head, res))
        except asyncio.TimeoutError:
            print(f'User timeout: {user['sid']}')
            await events.sock_sendall(client, __encode('error', 'timeout'))
            break
        except ValueError:
            print(f'Bad request {req.decode()} from {user['sid']}')
            await events.sock_sendall(client, __encode('error', 'badrequest'))
    con.close()
    client.close()

def __encode(head:str, body:str = ''):
    buf = f'{head}|{body}'
    return buf.encode()

def __decode(req:bytes):
    d = req.decode().strip()
    s = d.split('|')
    if len(s) == 1:
        s.append('')
    return tuple(s)
