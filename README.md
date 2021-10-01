# TheresNoDiscordBot

[![Mypy](https://github.com/TheresNoGit/TheresNoDiscordBot/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/TheresNoGit/TheresNoDiscordBot/actions/workflows/pylint.yml)
[![CodeQL](https://github.com/TheresNoGit/TheresNoDiscordBot/actions/workflows/codeql-analysis.yml/badge.svg?branch=master)](https://github.com/TheresNoGit/TheresNoDiscordBot/actions/workflows/codeql-analysis.yml)
[![Discord](https://img.shields.io/discord/865055891345506334?logo=discord&logoColor=white)](https://discord.gg/HDkHHRRs)

TheresNoDiscordBot is a Discord bot (funny that..) - its heavily geared towards [my Discord server](https://discord.gg/HDkHHRRs).

## Developing
To hack around with this bot, you'll need:
 - Python 3.9
 - `venv`
 - A completed `.env` file (bot tokens, role/channel IDs etc...)

### Clone the repo
```
$ git clone https://github.com/TheresNoGit/TheresNoDiscordBot.git
$ cd TheresNoDiscordBot
```

### Create & activate a virtual environment
```
$ python -m venv venv
```
You'll then need to [activate your virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) depending on your OS

### Install the requirements
```
$ pip install -r requirements.txt
```

### Set up your `.env` file
You'll need to contact us for relevant tokens/IDs.

### Run it!
```
$ python bot.py

2021-10-01 20:35:54
------------------
Logged in as
TheresNoBot
{token}
v1.6.0 (spicy)
------------------
```