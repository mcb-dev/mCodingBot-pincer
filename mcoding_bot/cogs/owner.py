from __future__ import annotations

import os
from typing import TYPE_CHECKING

import dotenv
import pincer

dotenv.load_dotenv()

MCODING = int(os.getenv("MCODING_SERVER"))

if TYPE_CHECKING:
    from mcoding_bot.bot import Bot


class Owner:
    def __init__(self, bot: Bot):
        self.bot = bot

    @pincer.command(name="gitpull", guild=MCODING)
    async def gitpull(self):
        os.system("git pull")
        self.bot.close()


setup = Owner
