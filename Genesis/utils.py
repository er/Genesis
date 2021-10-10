import time

import discord


async def generate_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, colour=0x000000)


async def is_claimable(interval: str, last_claimed: int) -> int:
    delay = {"daily": 86400, "weekly": 604800, "monthly": 2419200}
    print((last_claimed + delay[interval]) - int(time.time()))
    return (last_claimed + delay[interval]) - int(time.time())
