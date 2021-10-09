from __future__ import annotations
from os import listdir
from typing import TYPE_CHECKING, Dict

import inspect
from pincer.commands import command

if TYPE_CHECKING:
    from bot import Bot
    from pincer.objects import Embed


class Information:
    def __init__(self, client: Bot) -> None:
        self.client = client

        self.files: Dict[str, str] = {}
        folders = (".", "cogs")

        for path in folders:
            files = (file for file in listdir(path) if file.endswith(".py"))

            for file in files:
                with open(f"{path}/{file}", encoding="utf-8") as f:
                    self.files[file] = f.read()

        self.files["Total"] = "\n".join(self.files.values())

    @command(name="about", description="Provide the code info")
    async def get_code(self) -> Embed:
        return self.client.embed(
            title="Code structure",
            description=f"The whole code structure of {self.client.bot}!"
        ).add_fields(
            self.files,
            map_title=lambda name: f"> {name}",
            map_values=lambda f: inspect.cleandoc(
                    f"""
                    - `{len(f):,}` characters
                    - `{len(f.splitlines()):,}` lines
                    """
                ),
            inline=True
        )


setup = Information
