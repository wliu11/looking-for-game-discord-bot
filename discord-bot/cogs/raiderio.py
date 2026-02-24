import discord
from discord.ext import commands

from discord import app_commands
from utils.raiderio_parser import parse_raiderio_character_url
from utils.raiderio_api import fetch_character_profile
from utils.raiderio_validator import is_valid_raiderio_character

class RaiderIO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="raider", description="Fetch Raider.IO character info")
    @app_commands.describe(
        url="Raider.IO character profile URL",
        season="Select Mythic+ season"
    )
    @app_commands.choices(season=[
        app_commands.Choice(name="The War Within Season 1", value="season-tww-1"),
        app_commands.Choice(name="The War Within Season 2", value="season-tww-2"),
        app_commands.Choice(name="The War Within Season 3", value="season-tww-3"),
    ])
    async def raider(
        self,
        interaction: discord.Interaction,
        url: str,
        season: app_commands.Choice[str]
    ):
        await interaction.response.defer()

        if not is_valid_raiderio_character(url):
            await interaction.followup.send("❌ Invalid Raider.IO character URL.")
            return

        parsed = parse_raiderio_character_url(url)

        try:
            data = fetch_character_profile(
                parsed["region"],
                parsed["realm"],
                parsed["name"]
            )

            # Find selected season score
            selected_score = "Not Found"

            for s in data.get("mythic_plus_scores_by_season", []):
                if s["season"] == season.value:
                    selected_score = s["scores"]["all"]
                    break

            embed = discord.Embed(
                title=f'{data["name"]} — {data["class"]}',
                color=discord.Color.purple()
            )

            embed.add_field(name="Realm", value=data["realm"], inline=True)
            embed.add_field(name="Region", value=data["region"].upper(), inline=True)
            embed.add_field(name="Mythic+ Score", value=selected_score, inline=False)

            embed.set_footer(text=f"Season: {season.name}")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Error:\n```{e}```")


async def setup(bot):
    cog = RaiderIO(bot)

    await bot.add_cog(cog)
    bot.tree.add_command(cog.raider, guild=discord.Object(id=1444517104136224800))
    print("RaiderIO cog added")

