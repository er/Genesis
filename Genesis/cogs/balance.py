import discord
from discord.ext import commands
from discord.ext.commands import UserNotFound
from humanfriendly import format_number

from Genesis.utils import generate_embed


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, user: discord.User = None) -> discord.Embed:
        if user is None:
            user = ctx.author
        balance = await self.bot.pool.fetchval(
            "SELECT balance FROM users WHERE discord_id=$1", user.id
        )
        return await ctx.send(
            embed=await generate_embed(
                f"{user} has ${format_number(balance)}"
                if balance is not None
                else f"{user} has not created a Genesis profile yet!"
            )
        )

    @balance.error
    async def on_error(self, ctx, error):
        if isinstance(error, UserNotFound):
            await ctx.send(embed=await generate_embed("Please specify a valid user!"))


async def setup(bot):
    await bot.add_cog(Balance(bot))
