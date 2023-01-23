import discord
from discord import app_commands
from discord.ext import commands

from Genesis import config


class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pay")
    @app_commands.guilds(discord.Object(id=config.GUILD))
    async def pay(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        await interaction.response.defer()
        curr_bal = await self.bot.pool.fetchval(
            "SELECT balance FROM users WHERE user_id=$1", interaction.user.id
        )
        if curr_bal is None or curr_bal < amount:
            return await interaction.followup.send("You do not have enough money!")


async def setup(bot):
    await bot.add_cog(Pay(bot))
