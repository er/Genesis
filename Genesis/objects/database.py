import asyncpg
import discord
from asyncpg import Record

from Genesis import config
from Genesis.objects.player import Player


class DB:
    def __init__(self, bot):
        self.bot = bot
        self._pool = None

    async def connect(self):
        self._pool = await asyncpg.create_pool(
                config.POSTGRES_STRING,
            )

    async def create_user(self, member: discord.Member):
        async with self._pool.acquire() as con:
            await con.execute("INSERT INTO users VALUES($1, 100)", member.id)  # Change this to return the user after

    async def get_user(self, member: discord.Member) -> Player:
        async with self._pool.acquire() as con:
            data = await con.fetchrow(
                "SELECT users.balance, user_farms.farm_size, user_farms.farm_id, farms.*, count_query.count "
                "FROM users "
                "JOIN user_farms ON users.user_id = user_farms.user_id "
                "LEFT JOIN farms on user_farms.farm_id = farms.farm_id "
                "LEFT JOIN (SELECT farm_id, COUNT(farm_id) as count FROM farms GROUP BY farm_id) as count_query "
                "ON user_farms.farm_id = count_query.farm_id "
                "WHERE users.user_id=$1", member.id
            )
        if data is None:
            data = await self.create_user(member)
        data = dict(data)
        data["user_id"] = member.id
        print(data)
        return Player.parse_obj(dict(data))

    async def user_exists(self, member: discord.Member) -> bool:
        async with self._pool.acquire() as con:
            data = await con.fetchval("SELECT user_id FROM users WHERE user_id=$1", member.id)
        return data is not None
