from __future__ import annotations

from decimal import Decimal

import apgorm
from apgorm import types


class DecimalInt(apgorm.Converter[Decimal, int]):
    def to_stored(self, value: int) -> Decimal:
        return Decimal(value)

    def from_stored(self, value: Decimal) -> int:
        return int(value)


class NullDecimalInt(apgorm.Converter["Decimal | None", "int | None"]):
    def to_stored(self, value: int | None) -> Decimal | None:
        if value is None:
            return None
        return Decimal(value)

    def from_stored(self, value: Decimal | None) -> int | None:
        if value is None:
            return None
        return int(value)


class Message(apgorm.Model):
    id = types.Numeric().field().with_converter(DecimalInt)
    channel_id = types.Numeric().field().with_converter(DecimalInt)
    author_id = types.Numeric().field().with_converter(DecimalInt)

    sb_msg_id = types.Numeric().nullablefield().with_converter(NullDecimalInt)

    last_known_star_count = types.Int().field(default=0)

    primary_key = (id,)


class Star(apgorm.Model):
    message_id = types.Numeric().field().with_converter(DecimalInt)
    user_id = types.Numeric().field().with_converter(DecimalInt)

    primary_key = (message_id, user_id,)


class Database(apgorm.Database):
    messages = Message
    stars = Star

    def __init__(self):
        super().__init__("mcoding_bot/database/migrations")

    async def connect(self, **connect_kwargs) -> None:
        await super().connect(**connect_kwargs)

        if self.must_create_migrations():
            self.create_migrations()
        if await self.must_apply_migrations():
            await self.apply_migrations()
