import discord

def build_character_embed(data, score):

    embed = discord.Embed(
        title=f'{data["name"]} — {data["class"]}',
        color=discord.Color.purple()
    )

    embed.add_field(name="Realm", value=data["realm"], inline=True)
    embed.add_field(name="Region", value=data["region"].upper(), inline=True)

    embed.add_field(
        name="Mythic+ Score",
        value=score if score else "No runs yet",
        inline=False
    )

    return embed