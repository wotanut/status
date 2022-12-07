import discord
from discord.ext import commands
from discord import app_commands

 # NOTE: This class does not belong in the modals folder as it's only use is here. Furthermore it includes help command information and so is more relevant here.

class Dropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="Home", description="Home page", emoji='🏠'),
            discord.SelectOption(label="Setup", description="Setup page", emoji='🛠️'),
            discord.SelectOption(label="Other Commands", description="Other commands page", emoji="📜")
        ]

        super().__init__(placeholder='Select a command directory', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Home":
            embedHome = discord.Embed(title="Help", description="Help information about the bot", color=0x00ff00)
            embedHome.add_field(name="Status Checker", value="Welcome to the Status Checker help command.",inline=False)
            embedHome.add_field(name="Navigation", value="To navigate the help command, please use the dropdowns below.",inline=False)
            embedHome.add_field(name="Contributing/translating", value="If you would like to contribute please read the [contributing guidelines](https://github.com/wotanut/status/wiki) or if you can't help programmatically tip me on [Ko-fi](https://ko-fi.com/wotanut). If you would like to translate the bot into your language, please join the [support server](https://discord.gg/2w5KSXjhGe) and ask in the #status-checker forums.",inline=False)
            embedHome.add_field(name="Getting Help", value="If you need help with a specific command, please join the [support server](https://discord.gg/2w5KSXjhGe) and ask in the #status-checker forums.",inline=False)
            await interaction.response.edit_message(embed=embedHome)
        elif self.values[0] == "Setup":
            embedSetup = discord.Embed(title="Setup", description="Help information about the setup command", color=0x00ff00)
            embedSetup.add_field(name="/subscribe", value="Subscribe to a service")
            embedSetup.add_field(name="/unsubscribe", value="Unsubscribe from a service")
            embedSetup.add_field(name="/config", value="View your configuration")
            embedSetup.set_footer(text="Please note, when selecting the DM target you can not select any other user, when selecting the guild target you can only select a guild that you have MANAGE_SERVER permissions in.")
            await interaction.response.edit_message(embed=embedSetup)
        elif self.values[0] == "Other Commands":
            embedOther = discord.Embed(title="Other Commands", description="Help information about other commands", color=0x00ff00)
            embedOther.add_field(name="/help", value="Sends help information about the bot")
            embedOther.add_field(name="/ping", value="Checks the latency between our servers and discords")
            embedOther.add_field(name="/invite", value="Sends the invite link for the bot")
            embedOther.add_field(name="/info", value="Sends information about the bot")
            embedOther.add_field(name="/github", value="Sends the github link for the bot")
            embedOther.add_field(name="/debug", value="Sends debug information about the bot")
            embedOther.add_field(name="/status", value="Check the status of a service")
            await interaction.response.edit_message(embed=embedOther)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

# NOTE: This command can be better. It could be dynamic. However, I am not sure how to do that yet. I will look into it in the future.
class Help(commands.Cog):
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Sends help information about the bot")
    async def help(self, interaction : discord.Interaction):
        embed1 = discord.Embed(title="Help", description="Help information about the bot", color=0x00ff00)
        embed1.add_field(name="Status Checker", value="Welcome to the Status Checker help command.",inline=False)
        embed1.add_field(name="Navigation", value="To navigate the help command, please use the dropdowns below.",inline=False)
        embed1.add_field(name="Contributing/translating", value="If you would like to contribute please read the [contributing guidelines](https://github.com/wotanut/status/wiki) or if you can't help programmatically tip me on [Ko-fi](https://ko-fi.com/wotanut). If you would like to translate the bot into your language, please join the [support server](https://discord.gg/2w5KSXjhGe) and ask in the #status-checker forums.",inline=False)
        embed1.add_field(name="Getting Help", value="If you need help with a specific command, please join the [support server](https://discord.gg/2w5KSXjhGe) and ask in the #status-checker forums.",inline=False)
        await interaction.response.send_message(embed=embed1, view=DropdownView(),ephemeral=True)



async def setup(bot):
    await bot.add_cog(Help(bot))