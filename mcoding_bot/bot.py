from glob import glob
from typing import Optional

import aiohttp
import pincer
from pincer import Client
from pincer.objects import Embed

from mcoding_bot.config import Config


class Bot(Client):
    def __init__(self, config: Config):
        self.theme = 0x0B7CD3
        self.load_cogs()
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        super().__init__(self.config.token, intents=pincer.Intents.all())

    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session

    def load_cogs(self):
        """Load all cogs from the `cogs` directory."""
        for cog in glob("mcoding_bot/cogs/*.py"):
            if "__init__" in cog:
                continue

            self.load_cog(cog.replace("/", ".").replace("\\", ".")[:-3])
            print("Loaded cogs from", cog)

    @Client.event
    async def on_ready(self):
        print(
            "       _____       _ _            _____     _",
            " _____|     |___ _| |_|___ ___   | __  |___| |_",
            "|     |   --| . | . | |   | . |  | __ -| . |  _|",
            "|_|_|_|_____|___|___|_|_|_|_  |  |_____|___|_|",
            "                          |___|" "",
            sep="\n",
        )

    def embed(self, **kwargs) -> Embed:
        return Embed(**kwargs, color=self.theme).set_footer(
            text=f"{self.bot.username} - /help for more information",
        )

    async def close(self):
        await self.session.close()
        return await super().close()
