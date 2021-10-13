from __future__ import annotations

import time
from math import log

import aiohttp

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

BASE_URL = "https://www.googleapis.com/youtube/v3/channels"
_last_stats = {"subs": 0., "views": 0.}


async def get_stats(bot):
    link = (
        f"{BASE_URL}?part=statistics&id={bot.config.mcoding_yt_id}"
        f"&key={bot.config.yt_api_key}"
    )

    async with aiohttp.ClientSession().get(link) as res:
        response = await res.json()

    print(response)

    if not response:
        return _last_stats

    items = response.get("items")
    if not items:
        return _last_stats

    channel = items[0]
    if channel.get("id") != bot.config.mcoding_yt_id:
        return _last_stats

    statistics = channel.get("statistics")
    if not statistics:
        return _last_stats

    subs = float(statistics.get("subscriberCount", 0))
    views = float(statistics.get("viewCount", 0))

    if not subs or not views:
        return _last_stats

    print("Youtube statistics fetched!")
    _last_stats['subs'] = subs
    _last_stats['views'] = views
    return _last_stats


def display_stats(stat):
    int_stat = stat

    if int_stat < 10 ** 6:
        pretty_stat = int_stat / 10 ** 3
        unit = "K"
    else:
        pretty_stat = int_stat / 10 ** 6
        unit = "M"

    pretty_stat = round(pretty_stat, 2)

    exp_stat = round(log(int_stat, 2), 3)
    # ^ this might not be as accurate as the member count thing when
    # someone picky actually calculates it, but I suppose it's not
    # gonna be such a problem if it's gonna be shown as e.g. "44.3K"

    if exp_stat % 1 == 0:
        exp_stat = int(exp_stat)

    if pretty_stat % 1 == 0:
        pretty_stat = int(pretty_stat)

    return f"2**{exp_stat} ({pretty_stat}{unit})"


async def update_channels(self: Bot):
    stats = await get_stats(self)
    print(stats)

    print(display_stats(stats['subs']))
    print(display_stats(stats['views']))
    # TODO: update channels
    # Waiting for pincer 0.9.2 release in order to use `channel.edit`
