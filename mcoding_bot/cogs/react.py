from __future__ import annotations

from typing import TYPE_CHECKING
import re

from pincer import Client
from pincer.client import Bot
from pincer.objects.message import MessageType

if TYPE_CHECKING:
    from pincer.objects import UserMessage


class React:

    def __init__(self, client: Bot) -> None:
        self.client = client
        self.rust_search = re.compile("\\brust\\b") 

    @Client.event
    async def on_message(self, message: UserMessage):
        if message.type == MessageType.GUILD_MEMBER_JOIN:
            await message.react("👋")
        else:
            if self.rust_search.findall(message.content.lower()):
                await message.react("🚀")


setup = React
