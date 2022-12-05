# discord imports

from distutils.cmd import Command
import discord
from discord.ext import commands, tasks
from discord import app_commands, SelectOption
import discord.ui as ui

# quart imports

import quart
from quart import Quart, jsonify, render_template, redirect, Blueprint
from quart_discord import DiscordOAuth2Session, requires_authorization

# other imports

import requests
from dotenv import load_dotenv
import os
import asyncio
import datetime
import re
from typing import List
import traceback

# local imports

from utilities.data import Application, User, Meta, notificationType
from utilities.database import Database
from helper import Helper
from modals.modals import *

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
    "commands.misc",
    "commands.setup",
]

# discord specific configuration

class StatusChecker(commands.Bot):
    def __init__(self, *, intents: discord.Intents,initial_extensions: List[str]):
        super().__init__(command_prefix=commands.when_mentioned,intents=intents)
        self.initial_extensions = initial_extensions

    async def setup_hook(self):
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}.")
                traceback.print_exc()


intents = discord.Intents.default()
discord.Intents.presences = True
bot = StatusChecker(intents=intents, initial_extensions=cogs)

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
  
    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Bot Started", description=f"Succesful bot startup at {datetime.datetime.now().strftime('%d/%m/%Y at %H:%M')}", color=0x00ff00)
    await log_channel.send(embed=embed)

    # start checking the services

    bot.loop.create_task(app.run_task(host="0.0.0.0",port=1234))
    bot.loop.create_task(check_applications())

    # sync the commands

    bot.tree.copy_global_to(guild=discord.Object(939479619587952640))
    synced = await bot.tree.sync(guild=discord.Object(939479619587952640))

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

    if ctx.guild is None:
        print(error)
        return

    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Error", description=f"An error occured: {error} \n In Guild: {ctx.guild.name} \n Guild Owner: {ctx.guild.owner.mention}", color=0xff0000)
    await log_channel.send(embed=embed)

@bot.event
async def on_presence_update(before,after):

    # checks

    if before.bot == True:
        return
    elif before.id == bot.user.id:
        return
    elif before.status == after.status:
        return
    elif Help.Database.application_is_in_database(before.id) == False:
        return

    # send the notification

    await Help.send_notification(Help.Database.get_application(before.id).notifications,bot)

@bot.event
async def on_presence_update(before,after):

    application = Helper.get_from_database(before.id)
    if application["application_type"] != "bot":
        return # if the bot is not a bot, we will not do anything

    for notification in bot["notifications"]:
        if notification["webhook"]:
            Helper.webhook(notification["webhook"]) 
        elif notification["email"]:
            Helper.email(notification["email"])
        elif notification["sms"]:
            Helper.sms(notification["sms"])
        elif notification["discord"]:

            # send the message

            channel = await bot.get_channel(notification["discord"]["channel"])
            if notification["discord"]["content_type"] == "application/json":
                await channel.send(embed=discord.Embed.from_dict(notification["discord"]["payload"]))
            else:
                await channel.send(notification["discord"]["payload"])
            
            # auto publish
            if notification["discord"]["auto_publish"] == True:
                try:
                    await channel.publish()
                except:
                    pass
            
            # auto lock
            if notification["discord"]["auto_lock"] == True:
                guild = await bot.fetch_guild(notification["discord"]["guild"])
                try:
                    for channel in guild.channels:
                        if channel.id == notification["discord"]["channel"]:
                            await channel.edit(guild.default_role, reason="Auto locked channel", overwrites=discord.PermissionOverwrite(send_messages=False))
                except:
                    pass
        
            pass
        elif notification["dm"]:
            user = await bot.fetch_user(notification["dm"]["user"])
            if notification["dm"]["content_type"] == "application/json":
                await user.send(embed=discord.Embed.from_dict(notification["dm"]["payload"]))
            else:
                await user.send(notification["dm"]["payload"])

            pass


    raise discord.errors.ClientException()

@bot.event
async def on_guild_join(guild):
    # send a message to the channel
    try:
        guild = await bot.get_guild(guild)
        channel = await guild.get_channel()[0]
        embed = discord.Embed(title=f"Hello, {guild.name} I am Status Checker", description="I am a bot that will notify you when your application goes offline. To get started, please run the command `/setup`", color=discord.Color.green())
        await channel.send(embed=embed)
    except:
        pass
    # log the join

    log_channel = bot.get_channel(1042366316897636362)
    embed = discord.Embed(title="I joined a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id}", color=discord.Color.green())


@bot.event
async def on_guild_remove(guild):
    Helper.remove_from_database(guild.id)

    try:
        user = await bot.fetch_user(guild.owner_id)
        embed = discord.Embed(title="Hey there, I am sorry to see you go", description="All references of your guild have been removed from our database", color=discord.Color.red())
        # opportunity for a button
        await user.send(embed=embed)
    except:
        pass

    log_channel = bot.get_channel(1042366316897636362)
    embed = discord.Embed(title="I left a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id}", color=discord.Color.red())

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])