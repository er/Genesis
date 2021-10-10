import random
import time

import discord
from discord.ext import commands

from Genesis.constants import JOBS
from Genesis.utils import generate_embed


class Income(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.seconds_in_a_day = 86400

    async def generate_job(self, user_id: int) -> discord.Embed:
        job = random.choice(JOBS)
        amount = random.randint(25, 60)
        multiplier = await self.bot.pool.fetchval("SELECT multiplier FROM users WHERE discord_id=$1", user_id)
        return await generate_embed(job.replace("%amt%", f"${amount * multiplier}"))

    @commands.command(aliases=["w"])
    async def work(self, ctx) -> discord.Embed:
        return await ctx.reply(embed=await self.generate_job(ctx.author.id))

    @commands.command()
    async def daily(self, ctx) -> discord.Embed:
        last_claimed = await self.bot.pool.fetchval("SELECT daily_claimed_at FROM users WHERE discord_id=$1", ctx.author.id)
        if last_claimed + self.seconds_in_a_day > time.time():
            return await ctx.send(embed=await generate_embed(f"You can claim your daily rewards in "
                                                             f"<t:{last_claimed + self.seconds_in_a_day}:R>!"))




def setup(bot):
    bot.add_cog(Income(bot))
