from __future__ import annotations

from typing import TYPE_CHECKING

import dotenv
import os
import pincer

dotenv.load_dotenv()

MCODING = int(os.getenv("MCODING_SERVER"))

if TYPE_CHECKING:
    from mcoding_bot.bot import Bot


class Misc:
    def __init__(self, client: Bot):
        self.client = client

    @pincer.command(name="s", description="Seriously", guild=MCODING)
    async def seriously(self, ctx: pincer.objects.MessageContext):
        return f"{ctx.author} is serious btw"


setup = Misc  # noqa  # type: ignore
