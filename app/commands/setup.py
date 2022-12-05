import discord
from discord import app_commands
from discord.ext import commands
import os
import requests

# local imports
from ..modals.modals import Setup

class setup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="status",description="Check the status of a service")
    async def status(self, interaction : discord.Interaction, service:str = None, bt:discord.Member = None):
        #BUG: shows up as bt in discord when it should show up as bot
        if service == None and bt == None:
            await interaction.response.send_message("Please provide a service or a bot to check the status of.")
            return
        if service != None and bt != None:
            await interaction.response.send_message("You can only check the status of a bot or a service, not both.")
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
                await interaction.response.send_message(f"Bot {bt.mention} is {bt.status}") # BUG: Shows up as offline
            except Exception as e:
                await interaction.response.send_message(f"Unable to get bot {bt.name}, are you sure it is a valid bot? \n \n Error: || {e} || ")

    @app_commands.command(name="subscribe",description="Subscribe to a service")
    async def subscribe(self, interaction : discord.Interaction):
        await interaction.response.send_modal(Setup())

    # TODO: Add a command to unsubscribe from a service
    # TODO: Add a config command

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(setup(bot))