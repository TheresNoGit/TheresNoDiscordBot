"""Keys, URLs, and other constants."""
import os
import typing

import dotenv

dotenv.load_dotenv()

VERSION = "1.5.5"

DISCORD_KEY = typing.cast(str, os.getenv('DISCORD_BOT'))
GUILD = int(os.getenv('GUILD'))  # type: ignore
MOD_CHANNEL = int(os.getenv('MOD_CHANNEL'))  # type: ignore
ALL_MOD_CHANNEL = int(os.getenv('ALL_MOD_CHANNEL'))  # type: ignore
MOD_PLUS_PLUS = int(os.getenv('MOD_PLUS_PLUS'))  # type: ignore
MOD = int(os.getenv('MOD'))  # type: ignore
HALF_MOD = int(os.getenv('HALF_MOD'))  # type: ignore
TRUSTED = int(os.getenv('TRUSTED'))  # type: ignore
BOT_ID = int(os.getenv('BOT_ID'))  # type: ignore
