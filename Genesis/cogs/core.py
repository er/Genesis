import discord
from discord.ext import commands

from Genesis import config


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def bot_check(self, ctx):
        if not await self.bot.db.user_exists(ctx.author):
            await self.bot.db.create_user(ctx.author)
        return True

    @commands.command()
    async def test(self, ctx):
        player = await self.bot.db.get_user(ctx.author)
        print(dict(player))
        print(player.balance, player.farm_id)

    @commands.command()
    async def sync(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            return
        await self.bot.tree.sync(guild=discord.Object(id=config.GUILD))
        await ctx.send("Done")


async def setup(bot):
    await bot.add_cog(Core(bot))
