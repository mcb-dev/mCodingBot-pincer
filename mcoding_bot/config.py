from __future__ import annotations

import dataclasses
import typing
from typing import Dict, Optional

from pincer.utils.snowflake import Snowflake


@dataclasses.dataclass
class Config:
    db_name: str
    db_user: str
    db_password: str
    starboard_id: int
    required_stars: int
    _owner_ids: str
    mcoding_server: Snowflake
    mcoding_yt_id: str
    member_count_channel: Snowflake
    sub_count_channel: Snowflake
    token: str
    view_count_channel: Snowflake
    yt_api_key: str

    @property
    def owner_ids(self) -> list[int]:
        return [int(id.strip()) for id in self._owner_ids.split(",")]

    @classmethod
    def from_dict(cls, d: Dict[str, Optional[str]]):
        d = {key.lower(): value for key, value in d.items()}
        _type = typing.get_type_hints(cls)

        if missing := _type.keys() - d.keys():
            raise ValueError(f"Missing keys: {missing}")

        if extra := d.keys() - _type.keys():
            raise ValueError(f"Extra keys: {extra}")

        if null_keys := {key for key, value in d.items() if not value}:
            raise ValueError(f"Missing required values for: {null_keys}")

        return cls(**{key: _type[key](value) for key, value in d.items()})
