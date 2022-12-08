import discord
from discord.ext import commands

# local imports
import helper as helper
import views.buttons as buttons

class events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.help = helper.Helper()

    @commands.Cog.listener()
    async def on_presence_update(self,before,after):

        # checks

        if before.bot == False:
            return
        elif before.id == self.bot.user.id:
            return
        elif before.status == after.status:
            return
        elif self.help.Database.application_is_in_database(before.id) == False:
            return

        # send the notification

        print(f"Sending notification for {before.name}#{before.discriminator} ({before.id})")

        await self.help.send_notification(self.help.Database.get_application(before.id).notifications,self.bot)

    @commands.Cog.listener()
    async def on_guild_join(self,guild: discord.Guild):
        # send a message to the channel
        try:
            embed = discord.Embed(title=f"Hello, {guild.name} I am Status Checker", description="I am a bot that will notify you when your application goes offline. For more information on my command usage see `/help`. You can find my [support server here.](https://discord.gg/2w5KSXjhGe) and if you're interested in supporting this project you can tip me on [Ko-Fi](https://ko-fi.com/wotanut) or follow me on [GitHub](https://github.com/wotanut)", color=discord.Color.green())
            embed.set_footer(text="Made with ❤️ by Sambot")
            await guild.system_channel.send(embed=embed)
        except Exception as e:
            pass

        # log the join

        log_channel = self.bot.get_channel(1050359176859222017)
        embed = discord.Embed(title="I joined a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id} \n Total Guilds: {len(self.bot.guilds)}", color=discord.Color.green())
        if guild.icon != None:
            embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"Guild Owner: {guild.owner.name}#{guild.owner.discriminator}")
        await log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_remove(self,guild : discord.Guild):
        # self.help.remove_from_database(guild.id)

        try:
            user = await self.bot.fetch_user(guild.owner_id)
            embed = discord.Embed(title="Hey there, I am sorry to see you go", description="All references of your guild have been removed from our database. If you would feel up to, please can you fill in the feedback form below.", color=discord.Color.red())
            await user.send(embed=embed,view=buttons.Feedback())
        except:
            pass

        log_channel = self.bot.get_channel(1050359176859222017)
        embed = discord.Embed(title="I Left a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id} \n Total Guilds: {len(self.bot.guilds)}", color=discord.Color.red())
        if guild.icon != None:
            embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"Guild Owner: {guild.owner.name}#{guild.owner.discriminator}")
        await log_channel.send(embed=embed)



async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(events(bot))
