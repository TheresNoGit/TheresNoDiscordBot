"""Keys, URLs, and other constants."""
import os
import typing

import dotenv

dotenv.load_dotenv()

VERSION = "1.1.0"
DISCORD_KEY = typing.cast(str, os.getenv('DISCORD_BOT'))
MOD_CHANNEL = typing.cast(int, os.getenv('MOD_CHANNEL'))
BASED_MOD = typing.cast(int, os.getenv('BASED_MOD'))
HELPFUL_MOD = typing.cast(int, os.getenv('HELPFUL_MOD'))

EMAIL_API_URL = typing.cast(str, os.getenv('EMAIL_API_URL'))
EMAIL_API_KEY = typing.cast(str, os.getenv('EMAIL_API_KEY'))

EMAIL_FROM = typing.cast(str, os.getenv('EMAIL_FROM'))
EMAIL_TO = typing.cast(str, os.getenv('EMAIL_TO'))