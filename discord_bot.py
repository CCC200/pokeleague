import discord, sqlite3
from modules import config, users, tournaments
from extensions import discord_ext

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'{bot.user} connected')

tournament = bot.create_group('tournament', 'Tournament commands')

@tournament.command(name='register', description='Register for an active tournament')
async def register(ctx:discord.ApplicationContext):
    con = sqlite3.connect(config.DB_NAME)
    tid = discord_ext.get_channel_tid(ctx.channel_id, con)
    if tid is None:
        await ctx.respond('There is no tournament with registration available.', ephemeral=True)
        con.close()
        return
    sid = discord_ext.get_account(ctx.author.id, con)
    if sid is None:
        await ctx.send_modal(discord_ext.SignupModal(title="League Registration"))
    else:
        if tournaments.join(tid, sid, con):
            await discord_ext.member_nickname(ctx.author, sid, con)
            await ctx.respond(embed=discord_ext.embed_response('Register', f'{ctx.author.display_name} has joined the tournament!'))
        else:
            await ctx.respond('Something went wrong joining the tournament.', ephemeral=True)
    con.close()

manager = bot.create_group('manager', 'Manager commands')

@manager.command(name='open-tournament', description='Assigns tournament registration to this channel')
@discord.option('tourid', type=discord.SlashCommandOptionType.integer)
async def open_tournament(ctx:discord.ApplicationContext, tourid:int):
    con = sqlite3.connect(config.DB_NAME)
    res = discord_ext.link_channel(ctx.channel_id, ctx.author.id, tourid, con)
    await ctx.respond(res, ephemeral=True)
    con.close()

@manager.command(name='close-tournament', description='Removes tournament registration from this channel.')
async def close_tournament(ctx:discord.ApplicationContext):
    con = sqlite3.connect(config.DB_NAME)
    res = discord_ext.close_channel(ctx.channel_id, ctx.author.id, con)
    await ctx.respond(res, ephemeral=True)
    con.close()

config.init()
con = sqlite3.connect(config.DB_NAME)
discord_ext.init(con)
users.init(con)
tournaments.init(con)
con.close()
if config.discord_token is not None:
    bot.run(config.discord_token)
    print('\nBot closed')
else:
    print('ERROR: discord_token not found in config')

