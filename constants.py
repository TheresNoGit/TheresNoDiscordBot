"""Keys, URLs, and other constants."""
import os
import typing

import dotenv

dotenv.load_dotenv()

VERSION = "1.4.0"
DISCORD_KEY = typing.cast(str, os.getenv('DISCORD_BOT'))
GUILD = int(os.getenv('GUILD'))  # type: ignore
MOD_CHANNEL = int(os.getenv('MOD_CHANNEL'))  # type: ignore
BASED_MOD = int(os.getenv('BASED_MOD'))  # type: ignore
HELPFUL_MOD = int(os.getenv('HELPFUL_MOD'))  # type: ignore
TRUSTED = int(os.getenv('TRUSTED'))  # type: ignore

EMAIL_API_URL = typing.cast(str, os.getenv('EMAIL_API_URL'))
EMAIL_API_KEY = typing.cast(str, os.getenv('EMAIL_API_KEY'))

EMAIL_FROM = typing.cast(str, os.getenv('EMAIL_FROM'))
EMAIL_TO = typing.cast(str, os.getenv('EMAIL_TO'))
