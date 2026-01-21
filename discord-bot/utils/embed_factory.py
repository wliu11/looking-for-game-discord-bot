import discord
from config import ROLE_CHOICES
from config import REACTION_ROLES

def welcome_embed():
    lines = [
        f"{emoji} **{data['name']}**"
        for emoji, data in ROLE_CHOICES.items()
    ]

    embed = discord.Embed(
        title="🎮 Choose Your Role",
        description="React to choose your role:\n\n" + "\n".join(lines),
        color=discord.Color.blurple(),
    )

    embed.set_footer(text="You can change roles anytime.")
    return embed