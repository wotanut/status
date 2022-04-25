import os
import discord
from discord import app_commands
from datetime import time
from pymongo import MongoClient
from dotenv import load_dotenv

# import cogs
from cogs.bots import Bot
from cogs.misc import misc
from cogs.mc import Minecraft
from cogs.web import Web

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

bot = discord.Client(intents=intents)

tree = app_commands.CommandTree(bot)

# fires when the bot is ready
cogs = ["cogs.events"]

@bot.event 
async def on_ready():  # When the bot is ready
    tree.add_command(Bot())
    tree.add_command(misc())
    tree.add_command(Minecraft())
    tree.add_command(Web())

    for cog in cogs:
      try:
        await bot.load_extension(cog)
      except Exception as e:
        print(f"Could not laod cog {cog}: {str(e)}")    

    await tree.sync()  # Syncs the command tree

    print("I'm in")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over your bots!"))
    print(bot.user)  # Prints the bot's username and identifier

    startTime = time.time()
 
# runs the bot
bot.run(os.environ.get("DISCORD_BOT_SECRET"))