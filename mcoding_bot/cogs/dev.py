from __future__ import annotations

from typing import TYPE_CHECKING

import psutil
from pincer import command

if TYPE_CHECKING:
    from pincer.objects import Embed
    from mcoding_bot.bot import Bot


def _percent_info_unit_ram(used, total):
    mb: int = 1024 ** 2
    return (
        100 * (used / total),
        f"{(total / mb) / 1000:,.3f}",
        "Gb",
    )


def _percent_info_unit_cpu(cpu_percent, current_freq, max_freq):
    return (
        cpu_percent,
        f"{current_freq / 1000:.1f}`/`{max_freq / 1000:.1f}",
        "Ghz",
    )


def _percent_info_unit_disk(used, total):
    mb: int = 1024 ** 2
    return (
        100 * (used / total),
        f"{total / mb:,.0f}",
        "Mb",
    )


def _format_percent_info_unit_for_embed(percent, info, unit):
    return f"> `{percent:.3f}` **%**\n- `{info}` **{unit}**"


class Dev:
    """Admin & Test features"""

    def __init__(self, client: Bot):
        self.client = client

    @command(name="panel", description="Some data about the panel")
    async def panel_command(self) -> Embed:
        """Panel status command."""
        cols: tuple = ("blue", "green", "yellow", "orange", "red")
        vm = psutil.virtual_memory()
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent()
        disk = psutil.disk_usage("")

        stats = {
            "ram": _percent_info_unit_ram(vm.used, vm.total),
            "cpu": _percent_info_unit_cpu(cpu_percent, cpu_freq.current, cpu_freq.max),
            "disk": _percent_info_unit_disk(disk.used, disk.total),
        }

        title = "Panel Stats"
        description = "The bot is hosted on a private vps."
        embed = self.client.embed(title=title, description=description)

        def _format_name(name):
            col = cols[int(stats[name][0] // 20)]
            return f":{col}_square: __{name.upper()}__"

        embed = embed.add_fields(
            stats.items(),
            map_title=_format_name,
            map_values=_format_percent_info_unit_for_embed,
        )
        return embed


setup = Dev
