import asyncio

import discord
from discord.ext import commands
from humanfriendly import format_number


class ShopPages(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=120)
        self.embed = embeds["default"]


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop = {}
        self.shop_embeds = {
            "default": {
                "embed": discord.Embed(
                    title="Shop",
                    description="1 - Seeds\n2 - Island Upgrades",
                    colour=0x000000,
                ),
                "button": "Home",
            },
            "seeds": {"embed": None, "button": "seeds"},
        }

    async def load_shop(self):
        shop_items = await self.bot.pool.fetch(
            "SELECT * FROM item_info WHERE buy_price IS NOT NULL"
        )
        for item in shop_items:
            clean_name = item["item_name"].replace("_", " ").title()
            if item["item_type"] not in self.shop:
                self.shop[item["item_type"]] = {}
            if item["item_type"] not in self.shop_embeds:
                self.shop_embeds[item["item_type"]] = {
                    "embed": None,
                    "button": item["item_type"],
                }
            self.shop[item["item_type"]][clean_name] = item["buy_price"]
        for category in self.shop.keys():
            embed = discord.Embed(
                title=category.title(), description="", colour=0x000000
            )
            for item, price in self.shop[category].items():
                embed.description += f"{item} - ${format_number(price)}\n"
            self.shop_embeds[category]["embed"] = embed

    @commands.command()
    async def shop(self, ctx):
        for cat, data in self.shop_embeds.items():
            await ctx.send(embed=data["embed"])


async def setup(bot):
    await bot.add_cog(Shop(bot))
