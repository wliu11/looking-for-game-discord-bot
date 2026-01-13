import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='../discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as lfgBot")

async def setup_extensions():
    await bot.load_extension("cogs.reaction_roles")

@bot.event
async def setup_hook():
    await setup_extensions()

bot.run(TOKEN)
