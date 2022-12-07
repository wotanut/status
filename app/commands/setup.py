import discord
from discord import app_commands
from discord.ext import commands
import requests

# local imports
import views.modals as modals
import views.dropdowns as dropdowns

class configuration(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="subscribe",description="Subscribe to a service")
    async def subscribe(self, interaction : discord.Interaction):
        await interaction.response.send_modal(modals.Setup())

    @app_commands.command(name="unsubscribe",description="Unsubscribe from a service")
    async def unsubscribe(self, interaction : discord.Interaction):
        await interaction.response.send_message("Please select a service to unsubscribe from.", view=dropdowns.unSubscribeView())
    
    @app_commands.command(name="config", description="View your configuration")
    async def config(self, interaction : discord.Interaction):
        await interaction.response.send_message("Please select a service to view the configuration of.", view=dropdowns.configView())

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(configuration(bot))