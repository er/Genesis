from discord.ext import commands


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def bot_check(self, ctx):
        if ctx.author.id != await self.bot.pool.fetchval(
            "SELECT discord_id FROM users WHERE discord_id=$1", ctx.author.id
        ):
            await self.bot.pool.execute(
                "INSERT INTO users VALUES(Default, $1)", ctx.author.id
            )
        return True


async def setup(bot):
    await bot.add_cog(Core(bot))
