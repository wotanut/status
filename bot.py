import os
from keep_alive import keep_alive
import discord
from discord import Embed
from discord.ext import commands,tasks
from asyncio import sleep
import asyncio
from discord_slash import SlashCommand, SlashContext
import re


intents = discord.Intents.all()  
intents.members = True  

bot = commands.Bot(
	command_prefix="s!",  # Change to desired prefix
	case_insensitive=True,# Commands aren't case-sensitive
  intents=intents,  #enables intents
)

bot.author_id = 705798778472366131  # Change to your discord id!!!

slash = SlashCommand(bot,sync_commands=True)

@slash.slash(name="test")
async def test(ctx: SlashContext):
    embed = Embed(title="Embed Test")
    await ctx.send(embed=embed)

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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name = f"with your bots!"))
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

@bot.event
async def on_message(message):  
  if message.author.id == bot.user.id :
        return
  
  if message.content.startswith(f"<@!{bot.user.id}>") and len(message.content) == len(f"<@!{bot.user.id}>"):
    await message.channel.send(f"Hi, my name is status checker, my prefix is s! and you can do s!help for help!")
  await bot.process_commands(message)

@commands.has_permissions(manage_guild=True)
@bot.command()
async def config(ctx):
  await ctx.message.delete()

  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel


  embed = discord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
  embed.add_field(name = f"Channel:",value = f"None yet! tag one to select", inline = True)
  bed = await ctx.send(embed=embed)
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
            await ctx.send(f"Failed to get channel, this is usually becuase I do not have access or the channel does not exist Error: || {e} ||")
          await ctx.send(channel.type)
          if type(channel) != discord.channel.TextChannel:
            await ctx.send("That doesn't look like a text channel")
            await bed.delete()
            return
          #elif discord.channel.TextChannel.is_news():
           # await ctx.send("Anouncment catagory")
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
  try:
        input = await bot.wait_for("message",check=check, timeout=30)
        await input.delete()
        try:
          user = input.content.replace("<","")
          user = user.replace("@","")
          user = user.replace(">","")
          user = user.replace("!","")
          user = bot.get_user(int(user))
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
  try:
        down_message = await bot.wait_for("message",check=check, timeout=30)
        await down_message.delete()
        embed = discord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{user.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{down_message.content}", inline = True)
        await bed.edit(embed=embed)
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")
  message = await ctx.send(f"Watching {user.mention} I will aleart you if their status changes")
  #bot.loop.create_task(checks(ctx,user, message))
  

async def checks(ctx,user, message):
  while True:
    for i in ctx.guild.members:
      if i.id == user.id:
        if str(i.status) == 'online':
            await message.edit(content=f"<:online:844536822972284948>  {user.mention} is online")
        elif str(i.status) == 'idle':
          await message.edit(content=f"<:idle:852891603264602172> {user.mention} is on idle")
        elif str(i.status) == 'dnd':
          await message.edit(content=f"<:dnd:852891721771515934> {user.mention} is on do not disturb")
        else:
          await message.edit(content=f"<:offline:844536738512896020> {user.mention} is offline")
    await sleep(10)

@bot.command()
async def invite(ctx):
  user = bot.get_user(ctx.author.id)
  await user.send("https://dsc.gg/status-checker")
  await ctx.message.add_reaction("<:success:844896295054213171>")


extensions = ['cogs.loops']

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot
