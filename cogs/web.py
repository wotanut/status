import discord
from discord import app_commands
from pymongo import MongoClient
import requests
import os

# database connection
cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]

class Web(app_commands.Group):
    """Watch over Websites"""

    @app_commands.command(description="Check the status of a website")
    @app_commands.describe(url = "The website to check on")
    async def status(self, interaction: discord.Interaction,url:str):
        """Check the status of a website"""
        await interaction.response.send_message(f"The website responded with the status code: {requests.get(url=url).status_code} \n {requests.get(url=url).reason}")

    @app_commands.command(description="Check the latency of a website")
    @app_commands.describe(url = "The website to check on")
    async def latency(self, interaction: discord.Interaction,url:str):
        """Check the latency of a website"""
        await interaction.response.send_message(f"The website responded in {requests.get(url=url).elapsed.total_seconds()} seconds")
    
    @app_commands.command(description="Take a screenshot of a website")
    @app_commands.describe(url = "The website to take a screenshot of")
    async def screenshot(self, interaction: discord.Interaction,url:str):
        """Take a screenshot of a website"""
        embed = discord.Embed(title="Screenshot", description=f"The screenshot of {url}", color=0x00ff00)
        embed.set_image(url=f"https://image.thum.io/get/{url}")
        await interaction.response.send_message(embed=embed)