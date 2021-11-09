import logging

import dotenv

from mcoding_bot.bot import Bot
from mcoding_bot.config import Config

logging.basicConfig(level=logging.DEBUG)
dotenv_values = dotenv.dotenv_values(".env")
config = Config.from_dict(dotenv_values)
bot = Bot(config)
bot.run()
