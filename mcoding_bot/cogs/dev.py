from __future__ import annotations

from typing import TYPE_CHECKING

import psutil
from pincer import command

if TYPE_CHECKING:
    from pincer.objects import Embed
    from mcoding_bot.bot import Bot


class Dev:
    """Admin & Test features"""

    def __init__(self, client: Bot):
        self.client = client

    @command(name="panel", description="Some data about the panel")
    async def panel_command(self) -> Embed:
        """Panel status command."""
        cols: tuple = ("blue", "green", "yellow", "orange", "red")

        mb: int = 1024 ** 2

        vm = psutil.virtual_memory()
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent()
        disk = psutil.disk_usage("")

        stats = {
            "ram": (100 * (vm.used / vm.total), f"{(vm.total / mb) / 1000:,.3f}", "Gb"),
            "cpu": (
                cpu_percent,
                f"{cpu_freq.current / 1000:.1f}`/`{cpu_freq.max / 1000:.1f}",
                "Ghz",
            ),
            "disk": (100 * (disk.used / disk.total), f"{disk.total / mb:,.0f}", "Mb"),
        }

        return self.client.embed(
            title="Panel Stats", description="The bot is hosted on a private vps."
        ).add_fields(
            stats.items(),
            map_title=lambda name: (
                f":{cols[int(stats[name][0] // 20)]}_square: __{name.upper()}__"
            ),
            map_values=lambda percent, info, unit: (
                f"> `{percent:.3f}` **%**\n- `{info}` **{unit}**"
            ),
        )


setup = Dev
