import discord
from discord import app_commands
from discord.ext import commands
import datetime
import psutil

# local imports

import utilities.data as data

class misc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.meta = data.Meta()

    @app_commands.command(name="ping",description="Checks the latency between our servers and discords")
    async def ping(self, interaction : discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="invite",description="Sends the invite link for the bot")
    async def invite(self, interaction : discord.Interaction):
        try:
            await interaction.user.send(f"Hey there {interaction.user.mention}. Here is the invite link you asked for: https://discord.com/api/oauth2/authorize?client_id=845943691386290198&permissions=380105055296&scope=bot%20applications.commands")
            await interaction.response.send_message("I have sent you a DM with the invite link", ephemeral=True)
        except:
            await interaction.user.send(f"Hi {interaction.user.mention}, I am sorry but I cannot send you a DM. Please enable DMs from server members to use this command")

    @app_commands.command(name="info",description="Sends information about the bot")
    async def info(self, interaction : discord.Interaction):
        embed = discord.Embed(title="Status Checker", description="A bot that will notify you when your application goes offline", color=discord.Color.green())
        embed.set_author(name="Concept by Sambot", url="https://github.com/wotanut", icon_url="https://cdn.discordapp.com/avatars/705798778472366131/3dd73a994932174dadc65ff22b1ceb60.webp?size=2048")
        embed.add_field(name="What is this?", value="Status Checker is an open source bot that notifies you when your application goes offline or becomes unresponsive.")
        embed.add_field(name="How do I use it?", value="Each user has an \"account\" on the bot. For each user they can subscribe to an application and can send notifications to themselves or to a discord guild if they have manage server permissions in that guild. To subscribe to an application run `/subscribe` and to unsubscribe run `/unsubscribe`")
        embed.add_field(name="Sounds cool, you mentioned open source, how can I contribute?", value="First of all, thanks for your interest in contributing to this project. You can check out the source code on [GitHub](https://github.com/wotanut) where there is a more detailed contributing guide :)")
        embed.add_field(name="HELPPP", value="If you need help you can join the [Support Server](https://discord.gg/2w5KSXjhGe)")
        embed.add_field(name="I have a suggestion / bug to report", value="You can join the [Support Server](https://discord.gg/2w5KSXjhGe) and report it there or on the issues tab on [GitHub](https://github.com/wotanut/status)")
        embed.add_field(name="How can I support this project?", value="Thanks for your interest in supporting this project. You can support this project by tipping me on [Ko-Fi](https://ko-fi.com/wotanut) or by starring the [GitHub repository](https://github.com/wotanut). Furthermore, joining the [Discord Server](https://discord.gg/2w5KSXjhGe) is a great way to support the project as well as getting help with the bot")
        embed.set_footer(text="Made with ❤️ by Sambot")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="github", description="Sends the github link for the bot")
    async def github(self, interaction):
        await interaction.response.send_message("https://github.com/wotanut/status")

    @app_commands.command(name="debug", description="Sends debug information for the bot")
    async def debug(self, interaction : discord.Interaction):
        embed = discord.Embed(title="Debug Information", description="Debug information for the bot", color=discord.Color.blue())
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(name="Bot Uptime", value=f"{datetime.datetime.now() - self.meta.start_time}")
        embed.add_field(name="Bot Version", value=f"{self.meta.version} - {self.meta.version_name}")
        embed.add_field(name="Bot Memory Usage", value=f"{psutil.Process().memory_info().rss / 1024 ** 2} MB")
        embed.add_field(name="Bot CPU Usage", value=f"{psutil.cpu_percent()}%")

        await interaction.response.send_message(embed=embed)    


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(misc(bot))