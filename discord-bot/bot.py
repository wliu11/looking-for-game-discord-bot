import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from utils.database import init_db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def setup_extensions():
    await bot.load_extension("cogs.reaction_roles")
    await bot.load_extension("cogs.raiderio")


@bot.event
async def setup_hook():
    init_db()
    await setup_extensions()

bot.run(TOKEN)
