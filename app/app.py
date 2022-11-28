# discord imports

from distutils.cmd import Command
import discord
from discord.ext import commands
from discord import app_commands, SelectOption
import discord.ui as ui

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
import re

# local imports

from utilities.data import Application, User, Meta
from utilities.database import Database
from utilities.dropdown_views import *
from helper import Helper

# general configuration

load_dotenv()
Help = Helper()
meta = Meta()

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
    embed = discord.Embed(title="Bot Started", description=f"Succesful bot startup at {datetime.datetime.now().strftime('%d/%m/%Y at %H:%M')}", color=0x00ff00)
    await log_channel.send(embed=embed)

    # start checking the services

    bot.loop.create_task(app.run_task(host="0.0.0.0",port=1234))
    bot.loop.create_task(check_applications())

    # sync commands
    # await tree.sync(guild=discord.Object(id=939479619587952640))
    await tree.sync()

    # start the web server

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

@tree.command(name="ping",description="Checks the latency between our servers and discords")
async def ping(interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@tree.command(name="invite",description="Sends the invite link for the bot")
async def invite(interaction : discord.Interaction):
    try:
        await interaction.user.send(f"Hey there {interaction.user.mention}. Here is the invite link you asked for: https://discord.com/api/oauth2/authorize?client_id=845943691386290198&permissions=380105055296&scope=bot%20applications.commands")
        await interaction.response.send_message("I have sent you a DM with the invite link", ephemeral=True)
    except:
        await interaction.user.send(f"Hi {interaction.user.mention}, I am sorry but I cannot send you a DM. Please enable DMs from server members to use this command")

@tree.command(name="info",description="Sends information about the bot")
async def info(interaction):
    embed = discord.Embed(title="Status Checker", description="A bot that will notify you when your application goes offline", color=discord.Color.green())
    embed.set_author(name="Concept by Sambot", url="https://github.com/wotanut", icon_url="https://cdn.discordapp.com/avatars/705798778472366131/3dd73a994932174dadc65ff22b1ceb60.webp?size=2048")
    embed.add_field(name="What is this?", value="Status Checker is an open source bot that notifies you when your application goes offline or becomes unresponsive.")
    embed.add_field(name="How do I use it?", value="Each user has an \"account\" on the bot. For each user they can subscribe to an application and can send notifications to themselves or to a discord guild if they have manage server permissions in that guild. To subscribe to an application run `/subscribe` and to unsubscribe run `/unsubscribe`")
    embed.add_field(name="Sounds cool, you mentioned open source, how can I contribute?", value="First of all, thanks for your interest in contributing to this project. You can check out the source code on [GitHub](https://github.com/wotanut) where there is a more detailed contributing guide :)")
    embed.add_field(name="HELPPP", value="If you need help you can join the [Support Server](https://discord.gg/2w5KSXjhGe)")
    embed.add_field(name="WhErE iS yOuR pRiVaCy pOlIcY", value="We're a discord bot, I can't belive we need a privacy policy....but that's [here](http://bit.ly/SC-Privacy-Policy) and our TOS is [here](http://bit.ly/SC-TOS)")
    embed.add_field(name="I have a suggestion / bug to report", value="You can join the [Support Server](https://discord.gg/2w5KSXjhGe) and report it there or on the issues tab on [GitHub](https://github.com/wotanut/status)")
    embed.add_field(name="How can I support this project?", value="Thanks for your interest in supporting this project. You can support this project by tipping me on [Ko-Fi](https://ko-fi.com/wotanut) or by starring the [GitHub repository](https://github.com/wotanut). Furthermore, joining the [Discord Server](https://discord.gg/2w5KSXjhGe) is a great way to support the project as well as getting help with the bot")
    embed.set_footer(text="Made with ❤️ by Sambot")

    await interaction.response.send_message(embed=embed)

@tree.command(name="status",description="Check the status of a service")
async def status(interaction : discord.Interaction, service:str = None, bt:discord.Member = None):
    #BUG: shows up as bt in discord when it should show up as bot
    if service == None and bt == None:
        await interaction.response.send_message("Please provide a service or a bot to check the status of.")
        return
    if service != None:
        try:
            r = requests.get(service)
            await interaction.response.send_message(f"Service {service} responded with status code {r.status_code}")
        except Exception as e:
            await interaction.response.send_message(f"Unable to get service {service}, are you sure it is a valid URL? \n \n Error: || {e} || ")
    if bt != None:
        if bt.bot == False:
            await interaction.response.send_message("For privacy reasons, you can only check the status of bots.")
            return
        try:
            await interaction.response.send_message(f"Bot {bt.name} is {bt.status}") # BUG: Shows up as offline
        except Exception as e:
            await interaction.response.send_message(f"Unable to get bot {bt.name}, are you sure it is a valid bot? \n \n Error: || {e} || ")

@tree.command(name="subscribe",description="Subscribe to a service")
async def subscribe(interaction : discord.Interaction):

    class Setup(ui.Modal,title="Setup"):
        # ServiceType = ui.Select(placeholder="Select a service type",min_values=1,max_values=1, options=[
        #     discord.SelectOption(label="Web Server", value="website",emoji="<:website:1046716159682166815>"),
        #     discord.SelectOption(label="Bot", value="bot",emoji="<:bot_dev:945077689394536528>"),
        #     discord.SelectOption(label="Minecraft Server", value="mc",emoji="<:MC:1044914771612405760>"),
        # ])
        # TODO: As soon as discord supports select menus in modals, uncomment this

        ServiceType = ui.TextInput(label="Service Type (website,bot,mc)",placeholder="website",required=True)
        ServiceURL = ui.TextInput(label="Service URL (websites and mc only)",placeholder="https://sblue.tech/uptime",required=False)
        Bot = ui.TextInput(label="Bot (bots only) (bot_name)#(discriminator)",placeholder="Status Checker#2469",required=False)


        # TODO: Actually sending the damn notification

        async def on_submit(self, interaction: discord.Interaction):
            if self.ServiceType.value.lower() == "website":
                if self.ServiceURL.value == None:
                    await interaction.response.send_message("Your service type is website but you did not provide a service URL. Please try again.")
                    return
                regex = re.search(r"(http|https)://[a-zA-Z0-9./]+", self.ServiceURL.value)
                if regex == None:
                    await interaction.response.send_message("Your service URL is invalid. Please try again.")
                    return
                
                Database.add_website(interaction.user.id, self.ServiceURL.value,{})

                

                await interaction.response.send_message("Subscribed to website " + self.ServiceURL.value)

            elif self.ServiceType.value.lower() == "mc":
                if self.ServiceURL.value == None:
                    await interaction.response.send_message("Your service type is minecraft but you did not provide a service URL. Please try again.")
                    return
                regex = re.search(r"(http|https)://[a-zA-Z0-9./]+", self.ServiceURL.value)
                if regex == None:
                    await interaction.response.send_message("Your service URL is invalid. Please try again.")
                    return
                
                Database.add_minecraft(interaction.user.id, self.ServiceURL.value,{})


                await interaction.response.send_message("Subscribed to minecraft server " + self.ServiceURL.value)
            
            elif self.ServiceType.value.lower() == "bot":
                if self.Bot.value == None:
                    await interaction.response.send_message("Your service type is bot but you did not provide a bot. Please try again.")
                    return
                regex = re.search(r"[a-zA-Z0-9]+#[0-9]{4}", self.Bot.value)
                if regex == None:
                    await interaction.response.send_message("Your bot is not. Please try again.")
                    return
                
                Database.add_bot(interaction.user.id, self.Bot.value,{})

                await interaction.response.send_message("Subscribed to bot " + self.Bot.value)
    
    await interaction.response.send_modal(Setup())

# other commands
# help, config, subscribe,unsubscribe

# contributor commands

@tree.command(name="github", description="Sends the github link for the bot")
async def github(interaction):
    await interaction.response.send_message("https://github.com/wotanut/status")

@tree.command(name="debug", description="Sends debug information for the bot")
async def debug(interaction):
    embed = discord.Embed(title="Debug Information", description="Debug information for the bot", color=discord.Color.blue())
    embed.add_field(name="Bot Latency", value=f"{round(bot.latency * 1000)}ms")
    embed.add_field(name="Bot Uptime", value=f"{datetime.datetime.now() - meta.start_time}")
    embed.add_field(name="Bot Version", value=f"{meta.version} - {meta.version_name}")

    await interaction.response.send_message(embed=embed)    

# administrator commands

@tree.command(name="ban_guild", description="Bans a guild from using the bot",guild=discord.Object(id=939479619587952640))
@app_commands.checks.has_role(939481851939135548)
async def ban_guild(interaction, guild:int, reason:str = None):
    try:
        guild = await bot.get_guild(guild)
    except Exception as e:
        await interaction.response.send_message(f"Failed to get guild, are you sure i'm in that guild? \n \n Error: || {e} ||")
    
    try:
        await guild.owner.send(f"Your guild {guild.name} has been banned from using the bot with reason {reason}. If you believe this is a mistake please contact an administrator in our discord server. https://discord.gg/2w5KSXjhGe")
    except:
        pass

    await guild.leave()

    # post it

    r = requests.post("https://api.sblue.tech/bans/guild", data={"guild_id":guild.id, "reason":reason, "token":os.getenv("SBLUE_TECH_API_KEY")})

    await interaction.response.send_message(f"Successfully banned guild {guild.name} with reason {reason}")

@tree.command(name="unban_guild", description="Unbans a guild from using the bot",guild=discord.Object(id=939479619587952640))
@app_commands.checks.has_role(939481851939135548)
async def unban_guild(interaction, guild:int):
    # post it
    r = requests.post("https://api.sblue.tech/bans/guild/delete", data={"guild_id":guild.id, "token":os.getenv("SBLUE_TECH_API_KEY")})

    await interaction.response.send_message(f"Successfully unbanned guild {guild.name}")

@tree.command(name="ban_user", description="Bans a user from using the bot",guild=discord.Object(id=939479619587952640))
@app_commands.checks.has_role(939481851939135548)
async def ban_user(interaction, user:int, reason:str = None):
    try:
        user = await bot.fetch_user(user)
    except Exception as e:
        await interaction.response.send_message(f"Failed to get user. \n \n Error: || {e} ||")
    
    try:
        await user.send(f"You have been banned from using the bot with reason {reason}. If you believe this is a mistake please contact an administrator in our discord server. https://discord.gg/2w5KSXjhGe")
    except:
        pass

    # post it

    r = requests.post("https://api.sblue.tech/bans/user", data={"user_id":user.id, "reason":reason, "token":os.getenv("SBLUE_TECH_API_KEY")})

    await interaction.response.send_message(f"Banned user {user.name}#{user.discriminator} from using the bot with reason {reason}")

@tree.command(name="unban_user", description="Unbans a user from using the bot",guild=discord.Object(id=939479619587952640))
@app_commands.checks.has_role(939481851939135548)
async def unban_user(interaction, user:int):
    # post it
    r = requests.post("https://api.sblue.tech/bans/user/delete", data={"user_id":user.id, "token":os.getenv("SBLUE_TECH_API_KEY")})
    await interaction.response.send_message(f"Sucesfully unbanned user {user.name}#{user.discriminator}")

@tree.command(name="ban_service", description="Bans a service from using the bot",guild=discord.Object(id=939479619587952640))
@app_commands.checks.has_role(939481851939135548)
async def ban_service(interaction, service:str, reason:str = None):
    # post it

    r = requests.post("https://api.sblue.tech/bans/service", data={"service_id":service, "reason":reason, "token":os.getenv("SBLUE_TECH_API_KEY")})

    await interaction.response.send_message(f"Successfully banned service {service} with reason {reason}")

@tree.command(name="unban_service", description="Unbans a service from using the bot",guild=discord.Object(id=939479619587952640))
@app_commands.checks.has_role(939481851939135548)
async def unban_service(interaction, service:str):
    # post it
    r = requests.post("https://api.sblue.tech/bans/service/delete", data={"service_id":service, "token":os.getenv("SBLUE_TECH_API_KEY")})

    await interaction.response.send_message(f"Successfully unbanned service {service}")

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
async def discord_server():
    return redirect("https://discord.gg/2w5KSXjhGe")

@app.route("/youtube")
async def youtube():
    return redirect("https://www.youtube.com/channel/UCIVkp1F5JSyE0IKALyPW5sg")

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
