import asyncio
import logging.handlers
import os
import sys
from datetime import datetime

import asyncpg
import constants
import discord
from discord.ext import commands

from Genesis import config
from Genesis.config import TOKEN


# noinspection PyArgumentList
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
    ],
)

start_time = datetime.now().strftime("%d/%m/%Y | %H:%M")


class Genesis(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            case_insensitive=True,
            intents=discord.Intents.default(),
        )
        self.logger = logging.getLogger("Genesis")
        self.pool = None

    @staticmethod
    def setup_logging() -> None:
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
            stream=sys.stdout,
        )

    def setup_database(self) -> None:
        """Open a persistent asyncpg pool and create default tables"""
        loop = asyncio.get_event_loop()
        self.pool = loop.run_until_complete(asyncpg.create_pool(config.POSTGRES_STRING))
        self.logger.info("Successfully connected to Postgres")
        loop.run_until_complete(self.pool.execute(constants.CREATE_TABLES))
        self.logger.info("Successfully created default tables")

    def load_extensions(self) -> None:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
                self.logger.info(f"Successfully loaded {filename[:-3]}")

    async def on_ready(self):
        self.remove_command("help")

    async def on_command_error(self, ctx, error):
        ignored = (
            commands.CommandNotFound,
            commands.DisabledCommand,
            commands.NoPrivateMessage,
            commands.CheckFailure,
        )

        if isinstance(error, ignored):
            return

        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)

        raise error


if __name__ == "__main__":
    bot = Genesis()
    bot.setup_logging()
    bot.setup_database()
    bot.load_extensions()
    bot.run(TOKEN)
