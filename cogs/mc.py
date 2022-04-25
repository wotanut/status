import discord
from discord import app_commands
from pymongo import MongoClient
import os
from mcstatus import JavaServer, BedrockServer

# database connection
cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]

class Minecraft(app_commands.Group):
    """All commands related to Minecraft servers"""

    @app_commands.command(description="Check the status of a Minecraft server")
    @app_commands.describe(ip = "The IP of the server to check on")
    async def status(self, interaction: discord.Interaction,ip:str):
        """Check the status of a Minecraft server"""
        try:
            server = JavaServer.lookup(ip)
        except:
            try:
                server = BedrockServer.lookup(ip)
            except:
                await interaction.response.send_message(f"The server could not be found.")
                return
        status = server.status()
        await interaction.response.send_message(f"The server has {status.players.online} players and replied in {status.latency} ms")

    @app_commands.command(description="Check the latency of a Minecraft server")
    @app_commands.describe(ip = "The IP of the server to check on")
    async def latency(self, interaction: discord.Interaction,ip:str):
        """Check the latency of a Minecraft server"""
        try:
            server = JavaServer.lookup(ip)
        except:
            try:
                server = BedrockServer.lookup(ip)
            except:
                await interaction.response.send_message(f"The server could not be found.")
                return
        status = server.status() 
        await interaction.response.send_message(f"The server replied in {status.latency} ms")