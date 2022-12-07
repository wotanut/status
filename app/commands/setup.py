import discord
from discord import app_commands
from discord.ext import commands
import requests

# local imports
import modals.modals as modals

class configuration(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="status",description="Check the status of a service")
    @app_commands.rename(bt = "bot")
    @app_commands.describe(bt = "The bot to check the status of")
    @app_commands.describe(service = "The service to check the status of")
    async def status(self, interaction : discord.Interaction, service:str = None, bt:discord.Member = None):
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
                userstatus = interaction.guild.get_member(bt.id).status
                if userstatus == discord.Status.online:
                    await interaction.response.send_message(f"<:online:949589635061915648> Bot {bt.mention} is online")
                elif userstatus == discord.Status.idle:
                    await interaction.response.send_message(f"<:idle:949589635087081503> Bot {bt.mention} is idle")
                elif userstatus == discord.Status.dnd:
                    await interaction.response.send_message(f"<:dnd:949589635091284019> Bot {bt.mention} is dnd")
                else:
                    await interaction.response.send_message(f"<:offline:949589634898350101> Bot {bt.mention} is offline")
            except Exception as e:
                await interaction.response.send_message(f"Unable to get bot {bt.name}, are you sure it is a valid bot? \n \n Error: || {e} || ")

    @app_commands.command(name="subscribe",description="Subscribe to a service")
    async def subscribe(self, interaction : discord.Interaction):
        await interaction.response.send_modal(modals.Setup())

    @app_commands.command(name="unsubscribe",description="Unsubscribe from a service")
    async def unsubscribe(self, interaction : discord.Interaction):
        # TODO: Functionality to unsubscribe from a service
        await interaction.response.send_message("You have been unsubscribed from all services.")
    
    @app_commands.command(name="config", description="View your configuration")
    async def config(self, interaction : discord.Interaction):
        # TODO: Functionality for viewing configuration
        await interaction.response.send_message("You have no configuration.")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(configuration(bot))