import discord
from discord.ext import commands

from utils.raiderio_parser import parse_raiderio_character_url
from utils.raiderio_api import fetch_character_basic
from utils.raiderio_validator import is_valid_raiderio_character

class RaiderIO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def raider(self, ctx, url: str):
        if not is_valid_raiderio_character(url):
            await ctx.send(
                "❌ Please provide a valid Raider.IO character URL.\n"
                "Example:\n"
                "`https://raider.io/characters/us/illidan/Thrallslayer`"
            )
            return

        try:
            parsed = parse_raiderio_character_url(url)
            data = fetch_character_basic(
                parsed["region"],
                parsed["realm"],
                parsed["name"]
            )

            embed = discord.Embed(
                title=f'{data["name"]} — {data["class"]}',
                color=discord.Color.purple()
            )

            embed.add_field(name="Realm", value=data["realm"], inline=True)
            embed.add_field(name="Region", value=data["region"].upper(), inline=True)
            embed.add_field(name="Faction", value=data.get("faction", "Unknown").title(), inline=True)

            embed.set_footer(text="Data from Raider.IO")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Error fetching character:\n```{e}```")

async def setup(bot):
    await bot.add_cog(RaiderIO(bot))
