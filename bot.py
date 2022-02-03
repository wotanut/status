import os
from keep_alive import keep_alive
import discord
from discord import Embed
from discord.ext import commands,tasks
from asyncio import sleep
import asyncio
from discord_slash import SlashCommand, SlashContext
import re
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]


intents = discord.Intents.all()  
intents.members = True  

bot = commands.Bot(
	command_prefix="s!",  # Change to desired prefix
	case_insensitive=True,# Commands aren't case-sensitive
  intents=intents,  #enables intents
)

bot.author_id = 705798778472366131  # Change to your discord id!!!

class MyHelp(commands.HelpCommand):
  def get_command_signature(self, command):
    return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)
  async def send_bot_help(self, mapping):
      embed = discord.Embed(title="Help")
      for cog, commands in mapping.items():
          filtered = await self.filter_commands(commands, sort=True)
          command_signatures = [self.get_command_signature(c) for c in filtered]
          if command_signatures:
              cog_name = getattr(cog, "qualified_name", "No Category")
              embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
      channel = self.get_destination()
      await channel.send(embed=embed)

  async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()



@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over your bots!"))
    print(bot.user)  # Prints the bot's username and identifier

@bot.command(help="Checks the status of a bot")
async def status(ctx,user:discord.User):
  if not user.bot:
    await ctx.send("For privacy reasons, you can only check the status of a bot.")
    return
  for i in ctx.guild.members:
    if i.id == user.id:
      if str(i.status) == 'online':
          await ctx.send(f"<:online:844536822972284948>  {user.mention} is online")
      elif str(i.status) == 'idle':
        await ctx.send(f"<:idle:852891603264602172> {user.mention} is on idle")
      elif str(i.status) == 'dnd':
        await ctx.send(f"<:dnd:852891721771515934> {user.mention} is on do not disturb")
      else:
        await ctx.send(f"<:offline:844536738512896020> {user.mention} is offline")



@bot.command(help="Checks the bots latency", aliases=["latency","lag"])
async def ping(ctx):
  await ctx.send(f':ping_pong: Pong!\n **Bot**: {round(bot.latency * 1000)} ms')  

@commands.has_permissions(manage_guild=True)
@bot.command(help="Adds a bot to watch for status changes")
async def add_bot(ctx):
  await ctx.message.delete()

  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel


  embed = discord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
  embed.add_field(name = f"Channel:",value = f"None yet! tag one to select", inline = True)
  bed = await ctx.send(embed=embed)

  # get the channel


  try:
        msg = await bot.wait_for("message",check=check, timeout=30)
        await msg.delete()
        try:
          channel = msg.content.replace("<","")
          channel = channel.replace("#","")
          channel = channel.replace(">","")
          try:
            channel = bot.get_channel(int(channel))
          except Exception as e:
            await ctx.send(f"Failed to get channel, this is usually becuase I do not have access or the channel does not exist. \n Error: || {e} ||")
          if type(channel) != discord.channel.TextChannel:
            await ctx.send("That doesn't look like a text channel")
            await bed.delete()
            return
        except:
          await ctx.send("That doesn't look like a channel to me")
          await bed.delete()
          return
        embed = discord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"None yet! tag one to select", inline = True)
        await bed.edit(embed=embed)
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")



  # get the bot

  try:
        input = await bot.wait_for("message",check=check, timeout=30)
        await input.delete()
        try:
          user = input.content.replace("<","")
          user = user.replace("@","")
          user = user.replace(">","")
          user = user.replace("!","")
          user = bot.get_user(int(user))
          if not user.bot:
            await ctx.send("For privacy reasons I can only track bots")
            await bed.delete()
            return
          #await ctx.send(f"User's ID is {user.id} \n User Name \n {user.name} \n Mention {user.mention}")
        except:
          await ctx.send("That doesn't look like a bot to me")
          await bed.delete()
          return
        embed = discord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{user.mention}", inline = True)
        embed.add_field(name = f"Down Message:",value = f"Choose a message to be sent when the bot changes status", inline = True)
        await bed.edit(embed=embed)
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")


  # get the down message


  try:
        down_message = await bot.wait_for("message",check=check, timeout=30)
        await down_message.delete()
        embed = discord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{user.mention}", inline = True)
        embed.add_field(name = f"Down Message:",value = f"{down_message.content}", inline = True)
        if channel.is_news():
          embed.add_field(name = f"Auto Publish",value = f"I have detected that the channel you selected ({channel.mention}) is an announcement catagory, would you like me to automatically publish the down message?", inline = True)
        await bed.edit(embed=embed)
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")


  # get the state of auto publish (depending on type of channel)

  auto_publish = False
  if channel.is_news():
    try:
        publish = await bot.wait_for("message",check=check, timeout=30)
        await publish.delete()

        yes = ["y", "yes", "afirm","afirmitave", "positive","true"]
        no = ["n", "no", "negative","false"]


        if publish.content.lower() in yes:
          auto_publish = True
        elif publish.content.lower() in no:
          auto_publish = False
          await bed.delete()
          return
        else:
          await ctx.send(f"I couldn't tell what that meant, you must pick from one of the following options {yes}{no}")

        embed = discord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{user.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{down_message.content}", inline = True)
        embed.add_field(name = f"Auto Publish",value = f"{publish.content}", inline = True)
        await bed.edit(embed=embed)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        await bed.delete()
        return
  message = await channel.send(f"<a:loading:844891826934251551> Loading Status Checker information")

  try:
    collection.insert_one({"_id": user.id, f"{ctx.guild.id}": [channel.id,message.id,down_message.content,auto_publish]})
  except Exception as e:
    collection.update_one({"_id": user.id}, {"$set" : {f"{ctx.guild.id}": [channel.id,message.id,down_message.content,auto_publish]}})

  await ctx.send(f"Watching {user.mention} I will alert you if their status changes")

@bot.command(help="Invie the bot")
async def invite(ctx):
  user = bot.get_user(ctx.author.id)
  await user.send("https://dsc.gg/status-checker")
  await ctx.message.add_reaction("<:success:844896295054213171>")

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


extensions = ['cogs.loops']

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot
