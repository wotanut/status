import discord
from discord import app_commands
from pymongo import MongoClient
import os

# database connection
cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]

class Bot(app_commands.Group):
    """Watch over bots"""

    @app_commands.command(description="Check the status of a bot")
    @app_commands.describe(user = "The user to check the status of")
    async def status(self, interaction: discord.Interaction,user:discord.User):
        """Check the status of a bot"""
        if not user.bot:
            await interaction.response.send_message("For privacy reasons, you can only check the status of a bot.")
            return
        for i in interaction.guild.members:
            if i.id == user.id:
                if str(i.status) == "online":
                    await interaction.response.send_message(f"<:online:949589635061915648> {user.mention} is online")
                elif str(i.status) == "idle":
                    await interaction.response.send_message(f"<:idle:949589635087081503> {user.mention} is on idle")
                elif str(i.status) == "dnd":
                    await interaction.response.send_message(f"<:dnd:949589635091284019> {user.mention} is on do not disturb")
                else:
                    await interaction.response.send_message(f"<:offline:949589634898350101> {user.mention} is offline.")
    
    @app_commands.command(description="Clears every mention of your guild from the database")
    @app_commands.describe(user="The bot to remove from the database")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def remove(self,interaction: discord.Interaction, user:discord.User = None):
        """Clears every mention of your bot from the database"""
        if user != None:
            if not user.bot:
                await interaction.response.send_message("You can only remove a bot from the database")
                return
            try:
                if user == None:
                    collection.update_many( { }, { "$unset": { str(interaction.guild.id): "" } } )
                    await interaction.response.send_message(f"Removed all mentions of {interaction.guild.name} from the database")
                else:
                    collection.update_one({"_id": user.id}, {"$unset" : {f"{interaction.guild.id}": ""}})
                    await interaction.response.send_message(f"Removed {user.mention} from the database")
            except Exception as e:
                await interaction.response.send_message(e)

    @app_commands.command(description="Adds a bot to watch for status changes")
    @app_commands.describe(user="The user to watch the status of")
    @app_commands.describe(channel="The Channel to send down messages to")
    @app_commands.describe(down_message="The down message to send to the channel")
    @app_commands.describe(auto_publish="Whether the bot should publish the down message")
    @app_commands.describe(dm="Whether the bot should Direct Message you")
    @app_commands.describe(lock="Whether the bot should Lock the server if the bot goes down")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def add(self, interaction: discord.Interaction, user: discord.User,channel: discord.TextChannel, down_message: str, auto_publish: bool = False, dm:bool = False, lock:bool = False):
        """Adds a bot to watch for status changes"""
    
        if dm == False:
            owner = 0
        elif dm == True:
            owner = interaction.author.id
        
        try:
            channel = self.bot.get_channel(int(channel.id))
            if type(channel) != discord.channel.TextChannel:
                await interaction.response.send_message("That doesn't look like a text channel to me")
                return
            if auto_publish == True and channel.is_news() == False:
                auto_publish = False
        except Exception as e:
            await interaction.response.send_message(f"Failed to get channel, this is usually becuase I do not have access or the channel does not exist. \n Error: || {e} ||")
            return
        
        if user == self.bot.user.id:
            await interaction.response.send_message("You cannot add me for status checks\nYou can only add other bots")
            return
            
        # get the bot
        if not user.bot:
            await interaction.response.send_message("For privacy reasons I can only track bots")
            return

        # Instead of try/catch, just check for permissions
        permissionsInChannel = channel.permissions_for(channel.guild.me)
        if not permissionsInChannel.send_messages: 
            await interaction.response.send_message("I cannot send messages in that channel")
            return
        if not permissionsInChannel.manage_messages: # Needed to be able to publish messages in an announcements channel
            await interaction.response.send_message("I cannot manage messages in that channel")
            return

        if interaction.guild.me.server_permissions.manage_channels == False and lock == False:
            await interaction.response.send_message("In order to lock the server I need to have manage channels permissions")
            return
        
        # If bot has all needed permissions, send a message in that channel (and catch the error if it fails somehow)
        try:
            message = await channel.send("<a:loading:949590942925611058> Loading Status Checker information")
        except:
            await interaction.response.send_message("I do not have permissions to send messages in that channel")
            return

        try:
            collection.insert_one({"_id": user.id, f"{interaction.guild.id}": [channel.id,message.id,down_message,auto_publish,owner,lock]})
        except:
            collection.update_one({"_id": user.id}, {"$set" : {f"{interaction.guild.id}": [channel.id,message.id,down_message,auto_publish,owner,lock]}})

        await message.edit(content=f"Status Checker information loaded\nWatching {user.mention}")
        await interaction.response.send_message(f"Watching {user.mention} I will alert you if their status changes")

    