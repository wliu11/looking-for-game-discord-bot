import discord

def welcome_embed():
    embed = discord.Embed(
        title="🎮 Choose Your Role",
        description=(
            "React to choose your role:\n\n"
            "🩺 **Healer**\n"
            "🛡️ **Tank**\n"
            "⚔️ **DPS**"
        ),
        color=discord.Color.blurple()
    )
    embed.set_footer(text="You can change roles anytime by reacting again.")
    return embed