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