import os
from keep_alive import keep_alive
import diskord
from diskord.ext import commands
import asyncio
import requests
import aiohttp
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# view guild config

cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]


intents = diskord.Intents.all()  
intents.members = True  

bot = commands.Bot(
	command_prefix="s!",  # Change to desired prefix
	case_insensitive=True,# Commands aren't case-sensitive
  	intents=intents,      #enables intents
)

bot.author_id = 705798778472366131  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    await bot.change_presence(activity=diskord.Activity(type=diskord.ActivityType.watching, name="over your bots!"))
    print(bot.user)  # Prints the bot's username and identifier

@bot.slash_command(description="Get some help about the bot")
async def help(ctx):
  embed=diskord.Embed(title="FAQ", url="https://github.com/wotanut", color=0x258d58)
  embed.set_author(name="Made by Sambot#7421", url="https://github.com/wotanut")
  embed.add_field(name="What is this bot?", value="Status checker is a bot that was made to instantly inform you and your users of when your bot goes offline.", inline=False)
  embed.add_field(name="Why did you make this bot?", value="In the early horus of March 12th 2021 OVH burned down. Mine and many other discord bots were down for hours. I decided to try and find a bot that could do what Status Checker did but found none.", inline=False)
  embed.add_field(name="Can I track my members with this?", value="No, this bot tracks **other bots only**", inline=False)
  embed.add_field(name="Can I self host this bot?", value="Yes but I don't recommend it. If you want to find the source code please have a dig around my GitHub profile. I will not link directly to it to discourage you from trying to self host it.", inline=False)
  embed.add_field(name="I have a bug to report", value="Please do so in our [support server ](https://discord.gg/uNKfBdQHUx)", inline=True)
  embed.add_field(name="How do I get started?", value="/add", inline=True)
  await ctx.respond(embed=embed)

@bot.slash_command(description="Give some information about the bot")
async def stats(ctx):
  members = 0
  for guild in bot.guilds:
    members += guild.member_count - 1

  
  embed=diskord.Embed(title="Bot Stats")
  embed.set_author(name="Made by SamBot#7421", url="https://github.com/wotanut")
  embed.add_field(name="Guilds", value=f"```{len(bot.guilds)}```", inline=True) 
  embed.add_field(name="Users", value=f"```{members}```", inline=True)
  embed.set_footer(text="Thank you for supporting status checker")
  await ctx.respond(embed=embed)

@bot.slash_command(description="Check the status of a bot")
@diskord.application.option("user", description="The user to check the status of")
async def status(ctx,user:diskord.User):
  if not user.bot:
    await ctx.respond("For privacy reasons, you can only check the status of a bot.")
    return
  for i in ctx.guild.members:
    if i.id == user.id:
      if str(i.status) == "online":
          await ctx.respond(f"<:online:844536822972284948> {user.mention} is online")
      elif str(i.status) == "idle":
        await ctx.respond(f"<:idle:852891603264602172> {user.mention} is on idle")
      elif str(i.status) == "dnd":
        await ctx.respond(f"<:dnd:852891721771515934> {user.mention} is on do not disturb")
      else:
        await ctx.respond(f"<:offline:844536738512896020> {user.mention} is offline.")

@bot.slash_command(description="Clears every mention of your guild from the database")
@diskord.application.option("user", description="The bot to remove from the database")
@commands.has_permissions(manage_channels=True)
async def remove(ctx, user:diskord.User = None):
  if user != None:
    if not user.bot:
      await ctx.respond("You can only remove a bot from the database")
      return
    try:
    	if user == None:
    	  collection.update_many( { }, { "$unset": { str(ctx.guild.id): "" } } )
    	  await ctx.respond(f"Removed all mentions of {ctx.guild.name} from the database")
    	else:
    	  collection.update_one({"_id": user.id}, {"$unset" : {f"{ctx.guild.id}": ""}})
    	  await ctx.respond(f"Removed {user.mention} from the database")
    except Exception as e:
  	  await ctx.respond(e)

 
@bot.event
async def on_guild_join(guild):
  channel = client.get_channel(947126649378447400)
  embed=diskord.Embed(title="I joined a guild", description=f"{guild.name}", color=0x5bfa05)
  embed.timestamp = datetime.datetime.utcnow()
  await channel.send(embed=embed)

  async with aiohttp.ClientSession() as session:
    top = 'https://top.gg/api/bots/845943691386290198/stats'
    dsl = 'https://api.discordlist.space/v2/bots/845943691386290198'
    async with session.post(top,headers={"Authorization": os.getenv("top")},json={"server_count": int(len(bot.guilds))}) as resp:
        response = await resp.json()
        pass
    async with session.post(dsl,headers={"Authorization": os.getenv("dsl")},json={"serverCount": int(len(bot.guilds))}) as resp:
        response = await resp.json()
        pass
    

@bot.event
async def on_guild_remove(guild):
    channel = client.get_channel(947126649378447400)
    embed=diskord.Embed(title="I Left a guild", description=f"{guild.name}", color=0xfa0505)
    embed.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=embed)
    collection.update_many( { }, { "$unset": { str(guild.id): "" } } )

@bot.event
async def on_command_error(self, ctx, error):
  if isinstance(error, commands.CommandNotFound):
      return

  if isinstance(error, commands.BotMissingPermissions):
      await ctx.respond("I am missing required permissions to run this command")
      return

  if isinstance(error, commands.MissingPermissions):
      await ctx.respond("You are missing required permissions to run this command")
      return

  await ctx.respond("A fatal error occured, please join the support server for more information")

  channel = bot.get_channel(947126385254740028)

  embed = discord.Embed(title="Error", description="An error was produced", color= int("0x36393f", 16)) # Initializing an Embed
  embed.add_field(name=f"{ctx.author}", value=f"{error}")
  await channel.send(embed=embed)

@bot.slash_command(description="Check the latency of a bot")
async def ping(ctx):
  await ctx.respond(f":ping_pong: Pong!\n **Bot**: {round(bot.latency * 1000)} ms")  

@bot.slash_command(description="Get a link to invite the bot")
async def invite(ctx):
  await ctx.respond("https://dsc.gg/status-checker")

@bot.slash_command(description="View the bots privacy policy")
async def privacy(ctx):
  await ctx.respond("https://bit.ly/SC-Privacy-Policy")

@bot.slash_command(description="View the bots Terms Of Service")
async def terms(ctx):
  await ctx.respond("https://bit.ly/SC-TOS")

@bot.slash_command(description="Adds a bot to watch for status changes")
@diskord.application.option("user", description="The user to watch the status of")
@diskord.application.option("channel", description="The Channel to send down messages to")
@diskord.application.option("down_message", description="The down message to send to the channel")
@diskord.application.option("auto_publish", description="Whether the bot should publish the down message")
@diskord.application.option("dm", description="Whether the bot should Direct Message you")
@commands.has_permissions(manage_channels=True)
async def add(ctx, user: diskord.User,channel: diskord.abc.GuildChannel, down_message: str, auto_publish: bool = False, dm:bool = False):
  
  if dm == False:
    owner = 0
  elif dm == True:
    owner = ctx.author.id
  
  try:
    channel = bot.get_channel(int(channel.id))
    if type(channel) != diskord.channel.TextChannel:
      await ctx.respond("That doesn't look like a text channel to me")
      return
    if auto_publish == True and channel.is_news() == False:
      auto_publish = False
  except Exception as e:
    await ctx.respond(f"Failed to get channel, this is usually becuase I do not have access or the channel does not exist. \n Error: || {e} ||")
    return
  
  if user == bot.user.id:
    await ctx.respond("You cannot add me for status checks\nYou can only add other bots")
    return
    
  # get the bot
  if not user.bot:
    await ctx.send("For privacy reasons I can only track bots")
    return

  # Instead of try/catch, just check for permissions
  permissionsInChannel = channel.permissions_for(channel.guild.me)
  if not permissionsInChannel.send_messages: 
    await ctx.respond("I cannot send messages in that channel")
    return
  if not permissionsInChannel.manage_messages: # Needed to be able to publish messages in an announcements channel
    await ctx.respond("I cannot manage messages in that channel")
    return
  
  # If bot has all needed permissions, send a message in that channel (and catch the error if it fails somehow)
  try:
    message = await channel.send("<a:loading:844891826934251551> Loading Status Checker information")
  except:
    await ctx.respond("I do not have permissions to send messages in that channel")
    return

  try:
    collection.insert_one({"_id": user.id, f"{ctx.guild.id}": [channel.id,message.id,down_message,auto_publish,owner]})
  except:
    collection.update_one({"_id": user.id}, {"$set" : {f"{ctx.guild.id}": [channel.id,message.id,down_message,auto_publish,owner]}})

  await message.edit(content=f"Status Checker information loaded\nWatching {user.mention}")
  await ctx.respond(f"Watching {user.mention} I will alert you if their status changes")

updated = []
  
@bot.event
async def on_presence_update(before,after):
  if not before.bot:
    return

  if before.status == after.status:
    return

  if before.id in updated:
    return
    
  updated.append(before.id)

  try:
    await asyncio.sleep(10)
  
    double_check = bot.get_user(before.id)
  
    if before.status != double_check.status:
      return
  except:
    pass
    
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

            if str(after.status) == "online":
                await msg.edit(content=f"<:online:844536822972284948> {user.mention} is online")
            elif str(after.status) == "idle":
              await msg.edit(content=f"<:idle:852891603264602172> {user.mention} is on idle")
            elif str(after.status) == "dnd":
              await msg.edit(content=f"<:dnd:852891721771515934> {user.mention} is on do not disturb")
            else:
              await msg.edit(content=f"<:offline:844536738512896020> {user.mention} is offline")

              down_msg = await channel.send(down_message)
              if auto_publish == True:
                try:
                  await down_msg.publish()
                except:
                  pass

            try:
              user = bot.get_user(server[4])
              await user.send(down_message)
            except:
              pass
            
  except Exception as e:
    print(e)
    pass
  await asyncio.sleep(10)
  updated.remove(before.id)



keep_alive()  # Starts a webserver to be pinged
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot