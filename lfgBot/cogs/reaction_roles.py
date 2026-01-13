import discord
from discord.ext import commands

from config import (
    WELCOME_CHANNEL_ID,
    REACTION_ROLES
)
from utils.embed_factory import welcome_embed


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None  # Track the welcome message

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            print("Welcome channel not found.")
            return

        # Send welcome message
        message = await channel.send(embed=welcome_embed())
        self.message_id = message.id

        # Add reactions
        for emoji in REACTION_ROLES.keys():
            await message.add_reaction(emoji)

        print("Reaction role message ready.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.message_id:
            return

        if payload.emoji.name not in REACTION_ROLES:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member is None or member.bot:
            return

        role_id = REACTION_ROLES[payload.emoji.name]
        role = guild.get_role(role_id)

        if role:
            await member.add_roles(role)
            print(f"Added {role.name} to {member.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.message_id:
            return

        if payload.emoji.name not in REACTION_ROLES:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member is None:
            return

        role_id = REACTION_ROLES[payload.emoji.name]
        role = guild.get_role(role_id)

        if role:
            await member.remove_roles(role)
            print(f"Removed {role.name} from {member.name}")


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
