import asyncio
import os

import aiohttp
import discord
import requests
from discord.ext import commands, tasks
from discord import app_commands
from pymongo import MongoClient

# database connection
cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status-web"]


class Web(commands.GroupCog):
    """Watch over Websites"""

    @app_commands.command(description="Check the status of a website")
    @app_commands.describe(url="The website to check on")
    async def status(self, interaction: discord.Interaction, url: str):
        """Check the status of a website"""
        async with aiohttp.ClientSession() as session:
            try:
                r = await session.get(url=url)
                await interaction.response.send_message(
                    f"The website responded with the status code: {r.status} \n {r.reason}"
                )
            except Exception as e:
                await interaction.response.send_message(
                    f" I couldn't find {e} \n try <https://{e}> instead.")

    @app_commands.command(description="Check the latency of a website")
    @app_commands.describe(url="The website to check on")
    async def latency(self, interaction: discord.Interaction, url: str):
        """Check the latency of a website"""
        try:
            await interaction.response.send_message(
                f"The website responded in {requests.get(url=url).elapsed.total_seconds()} seconds"
            )
        except Exception as e:
            await interaction.response.send_message(e)

    @app_commands.command(description="Take a screenshot of a website")
    @app_commands.describe(url="The website to take a screenshot of")
    async def screenshot(self, interaction: discord.Interaction, url: str):
        """Take a screenshot of a website"""
        try:
            embed = discord.Embed(
                title="Screenshot",
                description=f"The screenshot of {url}",
                color=0x00FF00,
            )
            embed.set_image(url=f"https://image.thum.io/get/{url}")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(e)

async def setup(client):
    await client.add_cog(Web(client))
