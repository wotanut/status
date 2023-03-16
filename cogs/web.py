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
    def __init__(self, client):
        self.client = client
    async def cog_load(self):
        self.website.start()
        print("loaded")
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
    
    @app_commands.command(description="Clears every mention of your guild from the Website database")
    @app_commands.describe(website="The Website to remove from the database")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def remove(self ,interaction: discord.Interaction, website: str = None):
        """Clears every mention of your bot from the database"""
        try:
            if website == None:
                collection.update_many( { }, { "$unset": { str(interaction.guild.id): "" } } )
                await interaction.response.send_message(f"Removed all mentions of {interaction.guild.name} from the database")
            else:
                collection.update_one({"_id": website}, {"$unset" : {f"{interaction.guild.id}": ""}})
                await interaction.response.send_message(f"Removed {website} from the database")
        except Exception as e:
            await interaction.response.send_message(e)


    @tasks.loop(minutes=1)
    async def website(self):
        async with aiohttp.ClientSession() as session:
            try:
                results = collection.find()
                for result in results:
                    for query in result:
                        url = result["_id"]
                        print(url)
                        r = await session.get(url=url)
                        if r.status in list(range(100, 500)):
                            server = result[query]
                            channel = self.client.get_channel(server[0])
                            down_message = server[1]
                            auto_publish = server[2]
                            guild_id = server[3]
                            already_down = False
                            print(result[query])
                            print(down_message)
                            print(auto_publish)
                            print(guild_id)
                            print(already_down)
                            collection.update_one({"_id": url}, {"$set" : {f"{guild_id}": [channel ,down_message,auto_publish, guild_id, already_down]}})
                            await session.close()
                            pass
                        else:
                            await session.close()
                            if query == "_id":
                                pass
                            else:
                                server = result[query]
                                channel = self.client.get_channel(server[0])
                                down_message = server[1]
                                auto_publish = server[2]
                                guild_id = server[3]
                                already_down = server[4]
                                if already_down == True:
                                    return
                                down_msg = await channel.send(down_message)
                                already_down = True
                                collection.update_one({"_id": result["_id"]}, {"$set" : {f"{guild_id}": [channel,down_message,auto_publish, guild_id, already_down]}})

                                if auto_publish == True:
                                    try:
                                        await down_msg.publish()
                                    except:
                                        pass
            except Exception as e:
                print(e)

    @app_commands.command(description="Adds a Website to watch for status changes")
    @app_commands.describe(website="The website to watch the status of")
    @app_commands.describe(channel="The Channel to send down messages to")
    @app_commands.describe(down_message="The down message to send to the channel")
    @app_commands.describe(auto_publish="Whether the bot should publish the down message")
    async def add(self, interaction: discord.Interaction, website: str,channel: discord.TextChannel, down_message: str, auto_publish: bool = False):
        already_down = False
        try:
            channel = interaction.client.get_channel(int(channel.id))
            if type(channel) != discord.channel.TextChannel:
                await interaction.response.send_message("That doesn't look like a text channel to me")
                return
            if auto_publish == True and channel.is_news() == False:
                auto_publish = False
        except Exception as e:
            await interaction.response.send_message(f"Failed to get channel, this is usually becuase I do not have access or the channel does not exist. \n Error: || {e} ||")
            return

        permissionsInChannel = channel.permissions_for(channel.guild.me)
        if not permissionsInChannel.send_messages: 
            await interaction.response.send_message("I cannot send messages in that channel")
            return
        if not permissionsInChannel.manage_messages: # Needed to be able to publish messages in an announcements channel
            await interaction.response.send_message("I cannot manage messages in that channel")
            return
        try:
            collection.insert_one({"_id": website, f"{interaction.guild.id}": [channel.id,down_message,auto_publish, interaction.guild.id, already_down ]})
        except:
            collection.update_one({"_id": website}, {"$set" : {f"{interaction.guild.id}": [channel.id,down_message,auto_publish, interaction.guild.id]}})

        await interaction.response.send_message(f"Watching <{website}> I will alert you if their status changes")

        

async def setup(client):
    await client.add_cog(Web(client))
