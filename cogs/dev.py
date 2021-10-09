from typing import TYPE_CHECKING

import psutil
from pincer import command

if TYPE_CHECKING:
    from bot import Bot


class Dev:
    """Admin & Test features"""

    def __init__(self, bot: "Bot"):
        self.bot = bot

    @command(name="panel", description="Some data about the panel", cooldown=2)
    async def panel_stats(self, ctx):
        cols: tuple = ("blue", "green", "yellow", "orange", "red")
        mb: int = 1024 ** 2

        vm = psutil.virtual_memory()
        percent: int = 100 * (vm.used / vm.total)
        cpu_freq, cpu_percent = psutil.cpu_freq(), psutil.cpu_percent()
        disk = psutil.disk_usage(".")
        percent: int = 100 * (disk.used / disk.total)

        await ctx.send(
            embed=self.bot.embed(title="Bot Stats").add_field(
                name=f":{cols[int(percent // 20)]}_square: __RAM__",
                value="\n".join(
                    (
                        f"> `{percent:.3f}` **%**",
                        f" - `{vm.total / mb:,.3f}` **Mb**",
                    )
                ),
            ).add_field(
                name=f":{cols[int(cpu_percent // 20)]}_square: __CPU__",
                value=(
                    f"> `{cpu_percent:.3f}`**%**\n"
                    f"- `{cpu_freq.current / 1000:.1f}`/"
                    f"`{cpu_freq.max / 1000:.1f}` **Ghz**"
                ),
            ).add_field(
                name=f":{cols[int(percent // 20)]}_square: __DISK__",
                value="\n".join(
                    (
                        f"> `{percent:.3f}` **%**",
                        f"- `{disk.total / mb:,.3f}` **Mb**",
                    )
                )
            )
        )


setup = Dev
