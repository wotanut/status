import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
import datetime

# local imports
from .. import helper


class events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.help = helper.Helper()

    @commands.Cog.listener()
    async def on_presence_update(self,before,after):

        # checks

        if before.bot == True:
            return
        elif before.id == self.bot.user.id:
            return
        elif before.status == after.status:
            return
        elif self.help.Database.application_is_in_database(before.id) == False:
            return

        # send the notification

        await self.help.send_notification(self.help.Database.get_application(before.id).notifications,self.bot)

    # @bot.event
    # async def on_presence_update(before,after):

    #     application = Helper.get_from_database(before.id)
    #     if application["application_type"] != "bot":
    #         return # if the bot is not a bot, we will not do anything

    #     for notification in bot["notifications"]:
    #         if notification["webhook"]:
    #             Helper.webhook(notification["webhook"]) 
    #         elif notification["email"]:
    #             Helper.email(notification["email"])
    #         elif notification["sms"]:
    #             Helper.sms(notification["sms"])
    #         elif notification["discord"]:

    #             # send the message

    #             channel = await bot.get_channel(notification["discord"]["channel"])
    #             if notification["discord"]["content_type"] == "application/json":
    #                 await channel.send(embed=discord.Embed.from_dict(notification["discord"]["payload"]))
    #             else:
    #                 await channel.send(notification["discord"]["payload"])
                
    #             # auto publish
    #             if notification["discord"]["auto_publish"] == True:
    #                 try:
    #                     await channel.publish()
    #                 except:
    #                     pass
                
    #             # auto lock
    #             if notification["discord"]["auto_lock"] == True:
    #                 guild = await bot.fetch_guild(notification["discord"]["guild"])
    #                 try:
    #                     for channel in guild.channels:
    #                         if channel.id == notification["discord"]["channel"]:
    #                             await channel.edit(guild.default_role, reason="Auto locked channel", overwrites=discord.PermissionOverwrite(send_messages=False))
    #                 except:
    #                     pass
            
    #             pass
    #         elif notification["dm"]:
    #             user = await bot.fetch_user(notification["dm"]["user"])
    #             if notification["dm"]["content_type"] == "application/json":
    #                 await user.send(embed=discord.Embed.from_dict(notification["dm"]["payload"]))
    #             else:
    #                 await user.send(notification["dm"]["payload"])

    #             pass


    #     raise discord.errors.ClientException()

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        # send a message to the channel
        try:
            guild = await self.bot.get_guild(guild)
            channel = await guild.get_channel()[0]
            embed = discord.Embed(title=f"Hello, {guild.name} I am Status Checker", description="I am a bot that will notify you when your application goes offline. To get started, please run the command `/setup`", color=discord.Color.green())
            await channel.send(embed=embed)
        except:
            pass
        # log the join

        log_channel = self.bot.get_channel(1042366316897636362)
        embed = discord.Embed(title="I joined a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id}", color=discord.Color.green())


    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        self.help.remove_from_database(guild.id)

        try:
            user = await self.bot.fetch_user(guild.owner_id)
            embed = discord.Embed(title="Hey there, I am sorry to see you go", description="All references of your guild have been removed from our database", color=discord.Color.red())
            # opportunity for a button
            await user.send(embed=embed)
        except:
            pass

        log_channel = self.bot.get_channel(1042366316897636362)
        embed = discord.Embed(title="I left a guild", description=f"Guild Name: {guild.name} \n Guild ID: {guild.id}", color=discord.Color.red())



async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(events(bot))