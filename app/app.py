# discord imports

from distutils.cmd import Command
import discord
from discord.ext import commands
from discord import app_commands

# quart imports

import quart
from quart import Quart, jsonify, render_template, redirect
from quart_discord import DiscordOAuth2Session, requires_authorization

# other imports

import requests
from dotenv import load_dotenv
import os
import asyncio
import datetime

# local imports

from utilities.data import Application, User
from utilities.database import Database
from helper import Helper

# general configuration

load_dotenv()
Help = Helper()

# discord specific configuration

intents = discord.Intents.default()
discord.Intents.presences = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

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

    # sync commands
    await tree.sync(guild=discord.Object(id=939479619587952640))

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

@tree.command(name="ping",descrirption="Checks the latency between our servers and discords")
async def ping(interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@tree.command(name="invite",description="Sends the invite link for the bot")
async def invite(interaction):
    try:
        await interaction.author.send(f"Hey there {interaction.author.mention}. Here is the invite link you asked for: https://discord.com/api/oauth2/authorize?client_id=845943691386290198&permissions=380105055296&scope=bot%20applications.commands")
    except:
        await interaction.author.send(f"Hi {interaction.author.mention}, I am sorry but I cannot send you a DM. Please enable DMs from server members to use this command")

@tree.comand(name="info",description="Sends information about the bot")
async def info(interaction):
    embed = discord.Embed(title="Status Checker", description="A bot that will notify you when your application goes offline", color=discord.Color.green())
    embed.set_author(name="Concept by Sambot", url="https://github.com/wotanut", icon_url="https://cdn.discordapp.com/avatars/705798778472366131/3dd73a994932174dadc65ff22b1ceb60.webp?size=2048")
    embed.add_field(name="What is this?", description="Status Checker is an open source bot that notifies you when your application goes offline or becomes unresponsive.")
    embed.add_field(name="How do I use it?", description="Each user has an \"account\" on the bot. For each user they can subscribe to an application and can send notifications to themselves or to a discord guild if they have manage server permissions in that guild. To subscribe to an application run `/subscribe` and to unsubscribe run `/unsubscribe`")
    embed.add_field(name="Sounds cool, you mentioned open source, how can I contribute?", description="First of all, thanks for your interest in contributing to this project. You can check out the source code on (GitHub)[https://github.com/wotanut] where there is a more detailed contributing guide :)")
    embed.add_field(name="HELPPP", description="If you need help you can join the [Support Server](https://discord.gg/2w5KSXjhGe)")
    embed.add_field(name="WhErE iS yOuR pRiVaCy pOlIcY", description="We're a discord bot, I can't belive we need a privacy policy....but that's [here](http://bit.ly/SC-Privacy-Policy) and our TOS is [here](http://bit.ly/SC-TOS)")
    embed.add_field(name="I have a suggestion / bug to report", description="You can join the [Support Server](https://discord.gg/2w5KSXjhGe) and report it there")
    embed.add_field(name="How can I support this project?", description="Thanks for your interest in supporting this project. You can support this project by tipping me on [Ko-Fi](https://ko-fi.com/wotanut) or by starring the [GitHub repository](https://github.com/wotanut). Furthermore, joining the [Discord Server](https://discord.gg/2w5KSXjhGe) is a great way to support the project as well as getting help with the bot")
    embed.set_footer(text="Made with ❤️ by Sambot")

    await interaction.response.send_message(embed=embed)

@tree.command(name="status",description="Check the status of a service")
async def status(interaction, service:str = None, bot:discord.Member = None):
    if service == None and bot == None:
        await interaction.response.send_message("Please provide a service or a bot to check the status of.")
        return
    elif service != None:
        try:
            r = requests.get(service)
            await interaction.response.send_message(f"Service {service} responded with status code {r.status_code}")
        except Exception as e:
            await interaction.response.send_message(f"Unable to get service {service}, are you sure it is a valid URL? \n \n Error: || {e} || ")

# other commands
# help, config, subscribe,unsubscribe, uptime<service>, status<service>, dashboard

# contributor commands
# 

# administrator commands
# ban_guild
# unban_guild
# ban_user
# unban_user
# ban_service
# unban_service


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