import discord
from discord.ext import commands


class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pay(self, ctx, user: discord.User = None) -> discord.Embed:
        if user is None:
            return await ctx.reply(
                embed=discord.Embed(
                    description="You must specify a member to send money to!",
                    colour=000000,
                )
            )


async def setup(bot):
    await bot.add_cog(Pay(bot))
