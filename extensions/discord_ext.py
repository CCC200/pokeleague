import discord, sqlite3
from sqlite3 import Connection, Error
from modules import users, config, tournaments

ERROR_NOT_MANAGER = 'Command failed: You are not a manager for this league.'

class SignupModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Username",max_length=30,placeholder='CoolGuy15'))

    async def callback(self, interaction:discord.Interaction):
        con = sqlite3.connect(config.DB_NAME)
        username = self.children[0].value
        sid = users.register(username, con)
        if sid is not None:
            if link_account(interaction.user.id, sid, con):
                tid = get_channel_tid(interaction.channel_id, con)
                if tournaments.join(tid, sid, con):
                    await member_nickname(interaction.user, sid, con)
                    await interaction.response.send_message(embeds=[embed_response('Register', f'{username} has joined the tournament!')])
                else:
                    await interaction.response.send_message('Something went wrong joining the tournament.', ephemeral=True)
            else:
                await interaction.response.send_message('Something went wrong linking your account.', ephemeral=True)
        else:
            await interaction.response.send_message('Something went wrong during registration.', ephemeral=True)

def init(con:Connection):
    res = con.execute("SELECT name FROM sqlite_master WHERE name='discord_auth'")
    if res.fetchone() is None:
        print('Creating discord_auth database...')
        con.execute("""
                    CREATE TABLE discord_auth(
                    discord_id varchar(20) PRIMARY KEY,
                    sid varchar(18) NOT NULL,
                    FOREIGN KEY(sid) REFERENCES users(sid)
                    )
                    """)
    res = con.execute("SELECT name FROM sqlite_master WHERE name='discord_channel'")
    if res.fetchone() is None:
        print('Creating discord_channel database...')
        con.execute("""
                    CREATE TABLE discord_channel(
                    discord_id varchar(20) NOT NULL,
                    tid int NOT NULL,
                    active boolean NOT NULL DEFAULT true,
                    role_id varchar(20),
                    FOREIGN KEY(tid) REFERENCES tournaments(tid),
                    PRIMARY KEY(discord_id, tid)
                    )
                    """)
        
def get_account(userid:int, con:Connection):
    """Checks if a discount account has an associated pokeleague account and returns their secretID if so"""
    res = con.execute(f"SELECT sid FROM discord_auth WHERE discord_id='{userid}'")
    sid = res.fetchone()
    if sid:
        return sid[0]
    else:
        return None

def link_account(userid:int, sid:str, con:Connection):
    """Associate a discord account with a pokeleague account"""
    try:
        con.execute("INSERT INTO discord_auth(discord_id, sid) VALUES(?,?)", (userid, sid))
        con.commit()
        print(f'User {sid} linked with discord {userid}')
        return True
    except Error as e:
        print(f'Register discord failed: {e}')
        return False

def link_channel(channelid:int, userid:int, tid:int, con:Connection, roleid:str = None):
    """Associate a discord channel with a tournament (opens signups)"""
    if __check_manager(userid, tid, con):
        try:
            if roleid:
                con.execute("INSERT INTO discord_channel(discord_id, tid, role_id) VALUES(?,?,?)", (channelid, tid, roleid))
            else:
                con.execute("INSERT INTO discord_channel(discord_id, tid) VALUES(?,?)", (channelid, tid))
            con.commit()
            return 'Tournament linked to channel.'
        except Error as e:
            print(f'Link channel error: {e}')
            return 'Failed to link channel.'
    else:
        return ERROR_NOT_MANAGER
    
def close_channel(channelid:int, userid:int, con:Connection):
    """Closes connection to a tournament channel"""
    tid = get_channel_tid(channelid, con)
    if tid is not None:
        if __check_manager(userid, tid, con):
            try:
                con.execute(f"UPDATE discord_channel SET active=false WHERE discord_id='{channelid}'")
                con.commit()
                return 'Tournament registration closed.'
            except Error as e:
                print(f'Unlink channel error: {e}')
                return 'Failed to unlink channel.'
        else:
            return ERROR_NOT_MANAGER
        
def get_channel_tid(channelid:int, con:Connection):
    res = con.execute(f"SELECT tid FROM discord_channel WHERE discord_id='{channelid}' AND active=true")
    tid = res.fetchone()
    if tid:
        return tid[0]
    else:
        return None
    
def get_channel_role(channelid:int, con:Connection):
    res = con.execute(f"SELECT role_id FROM discord_channel WHERE discord_id='{channelid}'")
    roleid = res.fetchone()
    if roleid:
        return roleid[0]
    else:
        return None

def embed_response(title, body):
    embed = discord.Embed(title='Tournament')
    embed.add_field(name=title, value=body)
    return embed

async def member_nickname(member:discord.Member, sid:str, con:Connection):
    user = users.get(sid, con)
    if member.nick != user['name']:
        try:
            await member.edit(nick=user['name'])
        except:
            print(f'ERROR: Cannot edit "{member.display_name}" discord nickname; perm issue?')
    return user['name']

def __check_manager(userid:int, tid:int, con:Connection):
    res = con.execute(f"SELECT d.discord_id FROM discord_auth d LEFT JOIN managers m ON d.sid = m.sid LEFT JOIN tournaments t ON m.lid = t.lid WHERE t.tid='{tid}'")
    mgs = res.fetchall()
    for tup in mgs:
        if int(tup[0]) == userid:
            return True
    return False
