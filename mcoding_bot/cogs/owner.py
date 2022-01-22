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
    async def gitpull(self, ctx: pincer.objects.MessageContext):
        if ctx.author.id not in self.bot.config.owner_ids:
            return "You don't have permission to do this."
        await ctx.interaction.ack()
        os.system("git pull")
        await ctx.reply("Pulled from github, restarting bot...")
        self.bot.close()


setup = Owner
