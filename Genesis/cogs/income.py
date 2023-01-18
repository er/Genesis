import random
import time

import discord
from discord.ext import commands

from Genesis.constants import JOBS
from Genesis.utils import generate_embed
from Genesis.utils import is_claimable


class Income(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(
            1, 900, commands.BucketType.user
        )
        self.bounds = {
            "daily": {
                "lower": 200,
                "upper": 300,
            },
            "weekly": {"lower": 1000, "upper": 1200},
            "monthly": {"lower": 3500, "upper": 3800},
        }

    async def generate_job(self, user_id: int) -> discord.Embed:
        job = random.choice(JOBS)
        amount = random.randint(5, 20)
        await self.bot.pool.execute(
            f"UPDATE users SET balance=balance + $1 WHERE discord_id=$2",
            amount,
            user_id,
        )
        return await generate_embed(job.replace("%amt%", f"${amount}"))

    async def get_cooldown(self, ctx) -> float:
        """Returns the cooldown left"""
        bucket = self._cd.get_bucket(ctx.message)
        return bucket.update_rate_limit()

    @commands.command(aliases=["w"])
    async def work(self, ctx) -> discord.Message:
        if (cooldown := await self.get_cooldown(ctx)) is not None:
            if isinstance(cooldown, float) or isinstance(cooldown, int):
                return await ctx.send(
                    embed=await generate_embed(
                        f"You can work again <t:{int(time.time() + cooldown)}:R>"
                    )
                )
        return await ctx.reply(embed=await self.generate_job(ctx.author.id))

    @commands.command(aliases=["daily", "weekly", "monthly"])
    async def _interval_rewards(self, ctx) -> discord.Message:
        interval = ctx.invoked_with.lower()
        last_claimed = await self.bot.pool.fetchval(
            f"SELECT {interval}_claimed_at FROM users WHERE discord_id=$1",
            ctx.author.id,
        )
        if (time_until := await is_claimable(interval, last_claimed)) > 0:
            return await ctx.send(
                embed=await generate_embed(
                    f"You can claim your {interval} rewards "
                    f"<t:{int(time.time()) + time_until}:R>!"
                )
            )
        amount = random.randint(
            self.bounds[interval]["lower"], self.bounds[interval]["upper"]
        )
        await self.bot.pool.execute(
            f"UPDATE users SET balance=balance + $1, {interval}_claimed_at=$2 "
            f"WHERE discord_id=$3",
            amount,
            int(time.time()),
            ctx.author.id,
        )
        return await ctx.send(
            embed=await generate_embed(
                f"You claimed your daily rewards and got ${amount}!"
            )
        )


async def setup(bot):
    await bot.add_cog(Income(bot))
