import discord
from discord.ext import commands

from config import WELCOME_CHANNEL_ID, REACTION_ROLES
from utils.database import get_connection
from utils.embed_factory import welcome_embed

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_ids = {}  # guild_id -> message_id

    def get_saved_message(self, guild_id):
        with get_connection() as conn:
            cur = conn.execute(
                "SELECT channel_id, message_id FROM welcome_message WHERE guild_id = ?",
                (guild_id,)
            )
            return cur.fetchone()

    def save_message(self, guild_id, channel_id, message_id):
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO welcome_message (guild_id, channel_id, message_id)
                VALUES (?, ?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET
                    channel_id = excluded.channel_id,
                    message_id = excluded.message_id
            """, (guild_id, channel_id, message_id))

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        channel = guild.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            return

        saved = self.get_saved_message(guild.id)

        if saved:
            channel_id, message_id = saved
            try:
                message = await channel.fetch_message(message_id)
                self.message_ids[guild.id] = message.id
                print(f"Using existing welcome message in {guild.name}")
                return
            except discord.NotFound:
                print(f"Welcome message missing in {guild.name}, recreating")

        message = await channel.send(embed=welcome_embed())
        self.message_ids[guild.id] = message.id
        self.save_message(guild.id, channel.id, message.id)

        for emoji in REACTION_ROLES:
            await message.add_reaction(emoji)

        print(f"Posted welcome message in {guild.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id not in self.message_ids:
            return
        if payload.message_id != self.message_ids[payload.guild_id]:
            return
        if payload.emoji.name not in REACTION_ROLES:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member is None or member.bot:
            return

        role = guild.get_role(REACTION_ROLES[payload.emoji.name])
        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id not in self.message_ids:
            return
        if payload.message_id != self.message_ids[payload.guild_id]:
            return
        if payload.emoji.name not in REACTION_ROLES:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member is None:
            return

        role = guild.get_role(REACTION_ROLES[payload.emoji.name])
        if role:
            await member.remove_roles(role)


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
