import discord
from discord.ext import commands
import datetime
from helper import Helper

intents = discord.Intents.default()
discord.Intents.presences = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    # on ready we will start the web server, set the bot's status and log the uptime as well as a few other admin things
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching, name="over your bots"))
  
    log_channel = bot.get_channel(949388038260273193)
    embed = discord.Embed(title="Bot Started", description=f"Succesful bot startup at {datetime.datetime.now()}", color=0x00ff00)
    await log_channel.send(embed=embed)

@bot.event
async def on_command_error(ctx,error):
    print(error) # will be expanded on later

@bot.event
async def on_presence_update(before,after):
    if before.bot == True:
        return
    elif before.id == bot.user.id:
        return
    elif before.status == after.status:
        return
    elif Helper.check_database(before.id) == False:
        return

    NotificationType = Helper.get_notification_type(before.id)


    if NotificationType == Helper.webhook:
        Helper.webhook()
    elif NotificationType == Helper.email:
        Helper.email()
    elif NotificationType == Helper.sms:
        Helper.sms()
    elif NotificationType == Helper.dm:
        # due to limitattions of classes we can't do a helper class for this, therefore we will have to do it here
        pass
    elif NotificationType == Helper.discord:
        # due to limitattions of classes we can't do a helper class for this, therefore we will have to do it here
        pass

    raise discord.errors.ClientException()

@bot.event
async def on_guild_join(guild):
    print(guild) # again, again, will be expanded on later

@bot.event
async def on_guild_remove(guild):
    print(guild) # again,again,again will be expanded on later

# aside from this we need to add commands to watch other bots stop watching other bots and view the configuration of the guild
# furthermore commands for contributors and administrators should be added too.
# web dashboard too :P

token = "OTQ1MjY5MDcxODc0NzY0ODAw.G_n0Xy.-1HzoOk_w4RhOgh1mA9fmkRuh78qzlNSOakNuU" # this is insecure but I will edit this out

bot.run(token=token)