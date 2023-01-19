import discord
from discord.ext import commands

from Genesis import config


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def bot_check(self, ctx):
        if ctx.author.id != await self.bot.pool.fetchval(
            "SELECT user_id FROM users WHERE user_id=$1", ctx.author.id
        ):
            await self.bot.pool.execute(
                "INSERT INTO users VALUES($1, 100)", ctx.author.id
            )
        return True

    @commands.command()
    async def sync(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return
        await self.bot.tree.sync(guild=discord.Object(id=config.GUILD))
        await ctx.send("Done")


async def setup(bot):
    await bot.add_cog(Core(bot))
