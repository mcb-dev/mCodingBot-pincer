from __future__ import annotations

from typing import TYPE_CHECKING
from enum import Enum

from cachetools import TTLCache
import pincer
from pincer.objects import UserMessage, User, Channel
from pincer.utils import Snowflake

if TYPE_CHECKING:
    from mcoding_bot.bot import Bot


class UNDEF(Enum):
    UNDEF = "UNDEF"


def _s(num: int) -> Snowflake:
    return Snowflake(num)


class Cache:
    def __init__(self, bot: Bot):
        self.bot = bot
        self._messages: TTLCache[int, "UserMessage | None"] = TTLCache(500, 30)
        self._users: TTLCache[int, "User | None"] = TTLCache(500, 30)
        self._channels: TTLCache[int, "Channel | None"] = TTLCache(500, 30)

    async def gof_message(self, msg_id: int, ch_id: int) -> UserMessage | None:
        if (c := self._messages.get(msg_id, UNDEF.UNDEF)) is not UNDEF.UNDEF:
            return c

        try:
            msg = await self.bot.get_message(_s(msg_id), _s(ch_id))
        except pincer.NotFoundError:
            msg = None

        self._messages[msg_id] = msg
        return msg

    async def gof_channel(self, ch_id: int) -> Channel | None:
        if (c := self._channels.get(ch_id, UNDEF.UNDEF)) is not UNDEF.UNDEF:
            return c

        try:
            ch = await self.bot.get_channel(ch_id)
        except pincer.NotFoundError:
            ch = None

        self._channels[ch_id] = ch
        return ch

    async def gof_user(self, user_id: int) -> User | None:
        if (c := self._users.get(user_id, UNDEF.UNDEF)) is not UNDEF.UNDEF:
            return c

        try:
            usr = await self.bot.get_user(user_id)
        except pincer.NotFoundError:
            usr = None

        self._users[user_id] = usr
        return usr
