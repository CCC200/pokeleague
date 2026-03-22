# PokeLeague
### A tool for hosting & participating in competitive Pokemon tournaments.

**Server** | Client (coming soon)

<p align="center">
    <img src="icon.png">
</p>

> [!WARNING]
> This project is still very WIP. New features are being added and things may break at any time.

## What is PokeLeague?
PokeLeague is a Python + SQLite backend for running competitive Pokemon leagues. It is highly modular, meaning you can get a full experience or a simple integration with your existing setup!

### Features
- Register leagues and add managers with hosting permissions
- Create tournaments of any size or format
- Simple user registration with connections to existing services like Discord
- & more!

# Components
This project is made up of several components, some of which are optional if the setup does not warrant them.

## Server
The core server listens for socket connections, handles user login and can parse/reply to "requests" made by users. Ideally interacts with a frontend client the host provides.

### Setup

```
pip install requests
python3 pokeleague.py
```

Close the connection with **Ctrl+C**.

### Configuration
After the initial launch, several settings can be configured in `settings.json`:
- `address`: default `0.0.0.0` (this probably should not be changed)
- `port`: default `6500`
- `max_login_time`: default `600` (10 minutes)
- `max_idle_time`: default `1800` (30 minutes)

## Discord Bot
A discord bot can be deployed in league servers. This allows hosts to tie tournament registration to channels, with single-command onboarding for participants.

### Setup

```
python3 -m pip install -U py-cord
python3 discord_bot.py
```

Add the bot token to `settings.json` as follows:

```
"discord_token": "your_token_here"
```

## RCON
A simple CLI app to directly interact with the database. Useful for admins or minimal setups that might not need the [Server](#server) component.

### Setup

```
pip install requests
python3 rcon.py [command] [options]
```

Accepted commands and their arguments can be found in [`rcon.py`](rcon.py)

# Extensions
Extensions can connect to external services for additional functionality, and add relevant info to the database.

- [`discord_ext`](extensions/discord_ext.py): Used by the [Discord bot](#discord-bot) to link leagues, tournaments and users to Discord servers
- [`challonge_ext`](extensions/challonge_ext.py): Tournament brackets can be generated for league tournaments via the Challonge platform
