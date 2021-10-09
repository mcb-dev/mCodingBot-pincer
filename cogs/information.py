from __future__ import annotations
from os import listdir
from typing import TYPE_CHECKING, Dict

import inspect
from pincer.commands import command
from pincer.objects import Embed

if TYPE_CHECKING:
    from bot import Bot


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

    @command(name="code", description="Provide the code info")
    async def get_code(self) -> Embed:
        embed = self.client.embed(
            title="Code structure",
            description=f"The whole code structure of {self.client.bot}!"
        )

        for file_name, file in self.files.items():
            embed.add_field(
                name=f"> {file_name}",
                value=inspect.cleandoc(
                    f"""
                    - `{len(file):,}` characters
                    - `{len(file.splitlines()):,}` lines
                    """
                ),
                inline=True
            )

        return embed


setup = Information
