from __future__ import annotations

from typing import TYPE_CHECKING

from pincer.utils import TaskScheduler

from tasks.update_channels import update_channels

if TYPE_CHECKING:
    from bot import Bot


class YtStatistics:
    def __init__(self, client: Bot):
        self.client = client

        task = TaskScheduler(self.client)
        self.update_channels = task.loop(minutes=10)(update_channels)
        self.update_channels.start()


setup = YtStatistics
