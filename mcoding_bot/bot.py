import asyncio
from glob import glob
from typing import Optional

import aiohttp
import pincer
from pincer import Client
from pincer.objects import Embed

from mcoding_bot.config import Config
from mcoding_bot.database import Database
from mcoding_bot.cache import Cache


class Bot(Client):
    def __init__(self, config: Config):
        self.theme = 0x0B7CD3
        self.load_cogs()
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        super().__init__(self.config.token, intents=pincer.Intents.all())

        self.database = Database()
        self.cache = Cache(self)

        self.loop: asyncio.AbstractEventLoop
        self.stop_future: asyncio.Event

    def run(self):
        loop = asyncio.get_event_loop()
        self.loop = loop
        loop.run_until_complete(self._run())
        loop.run_until_complete(self._cleanup())

    async def _run(self):
        await self.database.connect(
            host="localhost",
            database=self.config.db_name,
            user=self.config.db_user,
            password=self.config.db_password,
        )
        self.stop_future = asyncio.Event(loop=self.loop)
        await self.start_shard(0, 1)
        await self.stop_future.wait()

    async def _cleanup(self):
        if self.session and not self.session.closed:
            await self.session.close()
        await self.database.cleanup()

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

    def close(self):
        self.stop_future.set()
