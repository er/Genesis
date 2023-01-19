import discord
from discord import app_commands
from discord.ext import commands

from Genesis import config
from Genesis.utils import generate_embed


class Farm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="harvest")
    async def harvest(self, interaction: discord.Interaction):
        ...

    @app_commands.command(name="plant")
    @app_commands.guilds(discord.Object(id=config.GUILD))
    async def plant(self, interaction: discord.Interaction, seed: str):
        await interaction.response.defer()
        c = await self.bot.pool.fetchrow(
            "SELECT user_farms.farm_id, user_farms.farm_size, COUNT(farms.farm_id) as count "
            "FROM user_farms "
            "JOIN farms ON user_farms.farm_id = farms.farm_id "
            "WHERE user_farms.user_id=$1 "
            "GROUP BY user_farms.farm_id", interaction.user.id
        )
        if (c is not None and c["count"] < c["farm_size"]) or (c is None):
            # allow plant
            ...
        else:
            return interaction.followup.send("Your farm is full")


async def setup(bot):
    await bot.add_cog(Farm(bot))
