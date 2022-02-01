from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar
import asyncpg

from pincer import Client
import pincer
from pincer.objects import (
    MessageReactionAddEvent, MessageReactionRemoveEvent, UserMessage, Embed
)
from pincer.utils.types import MissingType, APINullable

from mcoding_bot.database import Star, Message

if TYPE_CHECKING:
    from mcoding_bot.bot import Bot


_T = TypeVar("_T")


def _obj_or_none(obj: APINullable[_T]) -> _T | None:
    if isinstance(obj, MissingType):
        return None
    return obj


async def _orig_message(msg_id: int) -> Message | None:
    if (message := await Message.exists(sb_msg_id=msg_id)):
        return message
    return await Message.exists(id=msg_id)


def embed_message(
    msg: UserMessage, points: int, bot: Bot
) -> tuple[str, Embed]:
    embed = Embed(
        description=_obj_or_none(msg.content) or "",
        color=bot.theme,
    ).set_author(
        icon_url=msg.author.get_avatar_url(),  # type: ignore
        name=msg.author.username,  # type: ignore
        url="https://pincermademe.dothis",
    ).add_field(
        "​",
        f"[Go to Message](https://discord.com/channels/"
        f"{bot.config.mcoding_server}/{msg.channel_id}/{msg.id})"
    )
    if (attachments := _obj_or_none(msg.attachments)) is not None and len(attachments) > 0:
        embed.set_image(attachments[0].url)
        embed.description = embed.description or f"*{attachments[0].filename}*"
    elif not embed.description:
        embed.description = "*nothing*"

    return f"⭐ **{points} |** <#{msg.channel_id}>", embed


async def _refresh_message(bot: Bot, message: Message):
    # get starcount
    points = await Star.fetch_query().where(message_id=message.id).count()
    message.last_known_star_count = points

    # get action
    action: bool | None = None
    if points >= bot.config.required_stars:
        action = True
    elif points == 0:
        action = False

    # get the starboard message
    orig = await bot.cache.gof_message(message.id, message.channel_id)
    if not orig:
        return

    sbmsg = None
    if message.sb_msg_id is not None:
        sbmsg = await bot.cache.gof_message(
            message.sb_msg_id, bot.config.starboard_id
        )
        if not sbmsg:
            message.sb_msg_id = None

    # update
    if sbmsg is None and action is True:
        starboard = await bot.cache.gof_channel(bot.config.starboard_id)
        if not starboard:
            return

        content, embed = embed_message(orig, points, bot)
        sbmsg = await starboard.send(
            pincer.objects.Message(
                content=content,
                embeds=[embed],
            )
        )
        assert sbmsg
        await sbmsg.react("⭐")
        message.sb_msg_id = sbmsg.id

    elif sbmsg is not None:
        if action is False:
            await sbmsg.delete()
            message.sb_msg_id = None

        else:
            content, embed = embed_message(orig, points, bot)
            await sbmsg.edit(
                content=content,
                embeds=[embed],
            )

    await message.save()


class Starboard:
    def __init__(self, client: Bot):
        self.client = client
        self.refreshing: set[int] = set()

    async def refresh_message(self, message: Message):
        if message.id in self.refreshing:
            return
        self.refreshing.add(message.id)
        try:
            await _refresh_message(self.client, message)
        finally:
            self.refreshing.remove(message.id)

    @Client.event
    async def on_message_reaction_add(self, event: MessageReactionAddEvent):
        if (member := _obj_or_none(event.member)) is None:
            return
        if (user := _obj_or_none(member.user)) is None:
            user = await self.client.cache.gof_user(event.user_id)
            if not user:
                return
        if bool(user.bot):
            return

        if event.emoji.name != "⭐":
            return

        orig = await _orig_message(event.message_id)
        if not orig:
            obj = await self.client.cache.gof_message(
                event.message_id, event.channel_id
            )
            if not obj:
                return
            if (author := _obj_or_none(obj.author)) is None:
                return
            orig = await Message(
                id=event.message_id,
                channel_id=event.channel_id,
                author_id=author.id,
            ).create()

        assert self.client.bot is not None
        if (
            orig.author_id == self.client.bot.id
            and orig.channel_id == self.client.config.starboard_id
        ):
            # prevents old starboard messages from reposting
            return

        if orig.author_id == event.user_id:
            # no self stars
            return

        try:
            await Star(message_id=orig.id, user_id=event.user_id).create()
        except asyncpg.UniqueViolationError:
            # forgiveness, not permission
            # besides, Star.exists() is async so it might fail anyways
            pass

        await self.refresh_message(orig)

    @Client.event
    async def on_message_reaction_remove(
        self, event: MessageReactionRemoveEvent
    ):
        orig = await _orig_message(event.message_id)
        if not orig:
            return
        await Star.delete_query().where(
            message_id=orig.id, user_id=event.user_id
        ).execute()

        await self.refresh_message(orig)


setup = Starboard
