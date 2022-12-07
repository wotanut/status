import discord
from discord import app_commands
from discord.ext import commands
import requests

# local imports
import modals.modals as modals

class configuration(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

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