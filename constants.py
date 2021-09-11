"""Keys, URLs, and other constants."""
import os
import typing

import dotenv

dotenv.load_dotenv()

VERSION = "1.0.0"
DISCORD_KEY = typing.cast(str, os.getenv('DISCORD_BOT'))
ENWIKI_URL = "https://en.wikipedia.org/wiki/"
