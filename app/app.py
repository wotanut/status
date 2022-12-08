# discord imports

import discord
from discord.ext import commands

# quart imports

from quart import Quart
from quart_discord import DiscordOAuth2Session

# other imports

from dotenv import load_dotenv
import os
import asyncio
import datetime
import traceback

# local imports

from utilities.data import Meta
from helper import Helper

# from blueprints.api import api
from blueprints.redirects import redirects
from blueprints.routing import routing

# general configuration

load_dotenv()
Help = Helper()
meta = Meta()

cogs = [
    "commands.admin",
    "commands.events",
    "commands.help",
    "commands.misc",
    "commands.setup",
]

# discord specific configuration

intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned,intents=intents)

# quart specific  configuration

app = Quart(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['DISCORD_CLIENT_ID'] = os.getenv('DISCORD_CLIENT_ID')
app.config['DISCORD_CLIENT_SECRET'] = os.getenv('DISCORD_CLIENT_SECRET')
app.config['DISCORD_REDIRECT_URI'] = "os.getenv('DISCORD_REDIRECT_URI')"
oauth = DiscordOAuth2Session(app)

# app.register_blueprint(api)
app.register_blueprint(redirects)
app.register_blueprint(routing)


# bot stuff

@bot.event
async def on_ready():
    # on ready we will start the web server, set the bot's status and log the uptime as well as a few other admin things
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching, name="over your bots"))

    # load the cogs
    for cog in cogs:
        try:
            await bot.load_extension(cog)
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")
            traceback.print_exc()

    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Bot Started", description=f"Succesful bot startup at {datetime.datetime.now().strftime('%d/%m/%Y at %H:%M')}", color=0x00ff00)
    await log_channel.send(embed=embed)

    # start checking the services

    bot.loop.create_task(app.run_task(host="0.0.0.0",port=1234))
    bot.loop.create_task(check_applications())

    # sync the commands

    bot.tree.copy_global_to(guild=discord.Object(939479619587952640))
    await bot.tree.sync(guild=discord.Object(939479619587952640))

    print(f"Sucesfully logged in as {bot.user.name}#{bot.user.discriminator} with loaded cogs {cogs}")

async def check_applications():
    """ Checks the applications every 5 minutes """

    while True:
        await asyncio.sleep(300)
        await Help.check_applications(bot)

@bot.event
async def on_command_error(ctx,error):
    await ctx.send(f"An error occured: {error}")

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingPermissions or commands.MissingRole):
        await ctx.send("You don't have the permissions to do that!")
        return

    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have the permissions to do that!")
        return

    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Error", description=f"An error occured: {error} \n In Guild: {ctx.guild.name} \n Guild Owner: {ctx.guild.owner.mention}", color=0xff0000)
    await log_channel.send(embed=embed)

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
