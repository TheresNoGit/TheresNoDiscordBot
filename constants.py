"""Keys, URLs, and other constants."""
import os
import typing

import dotenv

dotenv.load_dotenv()

# Set to True to prevent log messages sending to Discord
DEV = False

# Version
VERSION = "1.6.0"
VERSION_NAME = "spicy"

# Bot config
DISCORD_KEY = typing.cast(str, os.getenv('DISCORD_BOT'))  # type: ignore
BOT_ID = int(os.getenv('BOT_ID'))  # type: ignore
GUILD = int(os.getenv('GUILD'))  # type: ignore

# Roles
MOD_PLUS_PLUS = int(os.getenv('MOD_PLUS_PLUS'))  # type: ignore
MOD = int(os.getenv('MOD'))  # type: ignore
HALF_MOD = int(os.getenv('HALF_MOD'))  # type: ignore
TRUSTED = int(os.getenv('TRUSTED'))  # type: ignore

# Channels
MOD_CHANNEL = int(os.getenv('MOD_CHANNEL'))  # type: ignore
ALL_MOD_CHANNEL = int(os.getenv('ALL_MOD_CHANNEL'))  # type: ignore
BOT_SPAM_CHANNEL = int(os.getenv('BOT_SPAM_CHANNEL'))  # type: ignore
COMMANDS_CHANNEL = int(os.getenv('COMMANDS_CHANNEL'))  # type: ignore

# Misc
BOT_ACTIVITY = typing.cast(str, os.getenv('BOT_ACTIVITY'))  # type: ignore
ERROR_COL = 0xff0000  # type: ignore
WARN_COL = 0xfcb603  # type: ignore
DEBUG_COL = 0x03fcf4  # type: ignore
