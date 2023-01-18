import discord
from discord.ext import commands

from Genesis.utils import generate_embed


class Farm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Farm(bot))
