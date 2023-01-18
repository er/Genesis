import os

import asyncpg
import config
import discord
from discord.ext import commands

from Genesis import constants


class Genesis(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            case_insensitive=True,
            intents=discord.Intents.all(),
        )
        self.ready = False
        self.pool = None

    async def load_cogs(self, directory="./cogs") -> None:
        for file in os.listdir(directory):
            if file.endswith(".py") and not file.startswith("_"):
                await self.load_extension(
                    f"{directory[2:].replace('/', '.')}.{file[:-3]}"
                )
            elif not (
                file in ["__pycache__"] or file.endswith(("pyc", "txt"))
            ) and not file.startswith("_"):
                await self.load_cogs(f"{directory}/{file}")

    async def on_ready(self):
        if not self.ready:
            self.pool = await asyncpg.create_pool(
                config.POSTGRES_STRING,
            )
            for table in constants.CREATE_TABLES:
                await self.pool.execute(table)
            await self.load_cogs()
            self.ready = True


if __name__ == "__main__":
    bot = Genesis()
    bot.remove_command("help")
    bot.run(config.TOKEN)
