# code imports

import os
import discord
from discord import app_commands
import asyncio
import requests
import datetime
from datetime import time
import aiohttp
from pymongo import MongoClient
from dotenv import load_dotenv
import sys

# local imports


from cogs.bot_watch import bot_watch
from cogs.events import events
from cogs.misc import misc
from cogs.mc import MC
from cogs.web import web

load_dotenv()

# database connection

cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]


# enabling intents

intents = discord.Intents.all()  
intents.members = True  

# defining the bot, the application commands and the start time

startTime = 0

bot = discord.Client(
  	intents=intents
)

tree = app_commands.CommandTree(bot)

# fires when the bot is ready

cogs = ["cogs.events"]

@bot.event 
async def on_ready():  # When the bot is ready

    tree.add_command(bot_watch())
    tree.add_command(events())
    tree.add_command(misc())
    tree.add_command(MC())
    tree.add_command(web())

    for cog in cogs:
      try:
        await bot.load_extension(cog)
      except Exception as e:
        print(f'Could not laod cog {cog}: {str(e)}')    

    await tree.sync()  # Syncs the command tree

    print("I'm in")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over your bots!"))
    print(bot.user)  # Prints the bot's username and identifier

    startTime = time.time()
 
# runs the bot

bot.run(os.environ.get("DISCORD_BOT_SECRET"))