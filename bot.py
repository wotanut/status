import os
from keep_alive import keep_alive
import diskord
from diskord import Embed
from diskord.ext import commands,tasks
from asyncio import sleep
import asyncio
import re
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# still to do

# on guild remove delete everything from the db
# view guild config
# remove bots from databases at guild owners request
# ensure that command permissions are working fine
# stats command

cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]


intents = diskord.Intents.all()  
intents.members = True  

bot = commands.Bot(
	command_prefix="s!",  # Change to desired prefix
	case_insensitive=True,# Commands aren't case-sensitive
  intents=intents,  #enables intents
)

bot.author_id = 705798778472366131  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    await bot.change_presence(activity=diskord.Activity(type=diskord.ActivityType.watching, name="over your bots!"))
    print(bot.user)  # Prints the bot's username and identifier

@bot.slash_command(guild_ids=[842044695269736498],description="Check the status of a bot")
@diskord.application.option('user', description='The user to check the status of')
async def status(ctx,user:diskord.User):
  if not user.bot:
    await ctx.respond("For privacy reasons, you can only check the status of a bot.")
    return
  for i in ctx.guild.members:
    if i.id == user.id:
      if str(i.status) == 'online':
          await ctx.respond(f"<:online:844536822972284948>  {user.mention} is online")
      elif str(i.status) == 'idle':
        await ctx.respond(f"<:idle:852891603264602172> {user.mention} is on idle")
      elif str(i.status) == 'dnd':
        await ctx.respond(f"<:dnd:852891721771515934> {user.mention} is on do not disturb")
      else:
        await ctx.respond(f"<:offline:844536738512896020> {user.mention} is offline")



@bot.slash_command(guild_ids=[842044695269736498],description="Check the latency of a bot")
async def ping(ctx):
  await ctx.respond(f':ping_pong: Pong!\n **Bot**: {round(bot.latency * 1000)} ms')  

@bot.slash_command(guild_ids=[842044695269736498],description="Adds a bot to watch for status changes")
@diskord.application.option('channel', description='The Channel to send down messages to')
@diskord.application.option('user', description='The user to watch the status of')
@diskord.application.option('down_message', description='The down message to send to the channel')
@diskord.application.option('auto_publish', description='Whether the bot should publish the down message')
@commands.has_permissions(manage_channels=True)
async def add(ctx, channel: diskord.abc.GuildChannel, user: diskord.User, down_message: str, auto_publish: bool = False):

  # get the channel and ensure that the bot has the correct access permisions 
  
  try:
    channel = bot.get_channel(int(channel.id))
  except Exception as e:
    await ctx.respond(f"Failed to get channel, this is usually becuase I do not have access or the channel does not exist. \n Error: || {e} ||")

  if type(channel) != diskord.channel.TextChannel:
    await ctx.respond("That doesn't look like a text channel to me")
    return
  if auto_publish == True and channel.is_news() == False:
    auto_publish = False
    
    
  # get the bot

  if not user.bot:
    await ctx.send("For privacy reasons I can only track bots")
    return

  try:
    message = await channel.send(f"<a:loading:844891826934251551> Loading Status Checker information")
  except:
    await ctx.respond("I do not have permissions to send messages in that channel")
    return

  try:
    collection.insert_one({"_id": user.id, f"{ctx.guild.id}": [channel.id,message.id,down_message,auto_publish]})
  except:
    collection.update_one({"_id": user.id}, {"$set" : {f"{ctx.guild.id}": [channel.id,message.id,down_message,auto_publish]}})

  await ctx.respond(f"Watching {user.mention} I will alert you if their status changes")

@bot.slash_command(guild_ids=[842044695269736498],description="Get a link to invite the bot")
async def invite(ctx):
  user = bot.get_user(ctx.author.id)
  await user.send("https://dsc.gg/status-checker")
  await ctx.respond("<:success:844896295054213171>")

@bot.event
async def on_member_update(before,after):
  if not before.bot:
    return

  if before.status == after.status:
    return

    
  user = bot.get_user(before.id)
  try:
    results = collection.find()
    for result in results:

      if str(result["_id"]) != str(user.id):
        # pass do literally nothing
        pass
      else:
        for query in result:
          if str(query) == "_id":
            pass
          else:
            server = result[query]
            channel = bot.get_channel(server[0])
            msg = await channel.fetch_message(server[1])
            down_message = server[2]
            auto_publish = server[3]      
            if str(after.status) == 'online':
                await msg.edit(content=f"<:online:844536822972284948>  {user.mention} is online")
            elif str(after.status) == 'idle':
              await msg.edit(content=f"<:idle:852891603264602172> {user.mention} is on idle")
            elif str(after.status) == 'dnd':
              await msg.edit(content=f"<:dnd:852891721771515934> {user.mention} is on do not disturb")
            else:
              await msg.edit(content=f"<:offline:844536738512896020> {user.mention} is offline")
              
              down_msg = await channel.send(down_message)
              if auto_publish == True:
                print("publishing down message")
                await down_msg.publish()
            
  except Exception as e:
    print(e)
    return

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot
