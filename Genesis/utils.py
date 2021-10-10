import discord


async def generate_embed(description: str) -> discord.Embed:
    return discord.Embed(description=description, colour=0x000000)