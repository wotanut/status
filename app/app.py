# discord imports

from distutils.cmd import Command
import discord
from discord.ext import commands
import datetime
from helper import Helper
from dotenv import load_dotenv
import os
import asyncio

# quart imports

import quart
from quart import Quart, jsonify, render_template, redirect
from quart_discord import DiscordOAuth2Session, requires_authorization

# other imports

# local imports

from utilities.data import Application, User
from utilities.database import Database

# general configuration

load_dotenv()
Help = Helper()

# discord specific configuration

intents = discord.Intents.default()
discord.Intents.presences = True
bot = discord.Client(intents=intents)

# quart specific  configuration

app = Quart(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['DISCORD_CLIENT_ID'] = os.getenv('DISCORD_CLIENT_ID')
app.config['DISCORD_CLIENT_SECRET'] = os.getenv('DISCORD_CLIENT_SECRET')
app.config['DISCORD_REDIRECT_URI'] = "os.getenv('DISCORD_REDIRECT_URI')"
oauth = DiscordOAuth2Session(app)

# bot stuff

@bot.event
async def on_ready():
    # on ready we will start the web server, set the bot's status and log the uptime as well as a few other admin things
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching, name="over your bots"))
  
    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Bot Started", description=f"Succesful bot startup at {datetime.datetime.now()}", color=0x00ff00)
    await log_channel.send(embed=embed)

    # start checking the services

    bot.loop.create_task(app.run(host="0.0.0.0",port=1234))
    bot.loop.create_task(check_applications())

async def check_applications():
    """ Checks the applications every 5 minutes """
    
    while True:
        await asyncio.sleep(300)
        await Help.check_applications(bot)

@bot.event
async def on_command_error(ctx,error):
    await ctx.send(f"An error occured: {error}")

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

@bot.command
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command
async def invite(ctx):
    try:
        await ctx.author.send(f"Hey there {ctx.author.mention}. Here is the invite link you asked for: https://discord.com/api/oauth2/authorize?client_id=845943691386290198&permissions=380105055296&scope=bot%20applications.commands")
    except:
        await ctx.send(f"Hi {ctx.author.mention}, I am sorry but I cannot send you a DM. Please enable DMs from server members to use this command")

# other commands
# ping, help, config, subscribe,unsubscribe, info, uptime<service>, status<service>,invite, dashboard,privacy

# contributor commands
# 

# administrator commands
# remove_Serivce


# aside from this we need to add commands to watch other bots stop watching other bots and view the configuration of the guild
# furthermore commands for contributors and administrators should be added too.
# web dashboard too :P

# quartz stuff


app = Quart(__name__)

# routing
 
@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/docs")
async def docs():
    return await render_template("docs.html")

@app.route("/about")
async def about():
    return await render_template("about.html")

@app.route("/dashboard")
async def dashboard():
    return await render_template("dashboard.html")

@app.route("/privacy")
async def privacy():
    return await render_template("privacy.html")

# api

@app.route("/api")
async def api():
    return await jsonify({"status": "ok"})

@app.route("/api/get_from_db/<id>")
async def get_from_db(id):
    """ Get's an application from the database and returns a json object of the stats"""
    return await jsonify({"status": "ok"})

@app.route("/api/add_to_db/<id>")
async def add_to_db(id):
    """ Adds an application to the database """
    return await jsonify({"status": "ok"})

@app.route("/api/remove_from_db/<id>")
async def remove_from_db(id):
    """ Removes an application from the database """
    return await jsonify({"status": "ok"})

# redirects

@app.route("/discord")
async def discord():
    return redirect("https://discord.gg/2w5KSXjhGe")

@app.route("/youtube")
async def youtube():
    return redirect("https://www.youtube.com/channel/UCIVkp1F5JSyE0IKALyPW5sg")