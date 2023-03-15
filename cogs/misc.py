import discord
from discord import app_commands
from pymongo import MongoClient
from dotenv import load_dotenv
import os
# database connection
load_dotenv()
cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]

class Misc(app_commands.Group):
    """Misc commands"""

    #@app_commands.command(description="Check the latency of a bot")
    #async def ping(self,interaction: discord.Interaction):
    #    await interaction.response.send_message(f":ping_pong: Pong!\n **Bot**: {round(self.bot.latency * 1000)} ms")  

    @app_commands.command(description="Get a link to invite the bot")
    async def invite(self,interaction: discord.Interaction):
        await interaction.response.send_message("https://dsc.gg/status-checker")

    @app_commands.command(description="View the bots privacy policy")
    async def privacy(self,interaction: discord.Interaction):
        await interaction.response.send_message("https://bit.ly/SC-Privacy-Policy")

    @app_commands.command(description="View the bots Terms Of Service")
    async def terms(self,interaction: discord.Interaction):
        await interaction.response.send_message("https://bit.ly/SC-TOS")

    @app_commands.command(description="Get some useful debugging information about the bot")
    async def debug(self,interaction: discord.Interaction):
        embed=discord.Embed(title="Debug Information",color=0x08bbe7)
        embed.add_field(name="Version", value="1.0.2", inline=True)
        embed.add_field(name="Version Name", value="Rick", inline=True)
        # embed.add_field(name="Uptime", value=str(datetime.timedelta(seconds=int(round(time.time()-startTime)))), inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Get some help about the bot")
    async def help(self, interaction: discord.Interaction):
        embed=discord.Embed(title="FAQ", url="https://github.com/wotanut", color=0x258d58)
        embed.set_author(name="Made by Sambot#7421", url="https://github.com/wotanut")
        embed.add_field(name="What is this bot?", value="Status checker is a bot that was made to instantly inform you and your users of when your bot goes offline.", inline=False)
        embed.add_field(name="Why did you make this bot?", value="In the early horus of March 12th 2021 OVH burned down. Mine and many other discord bots were down for hours. I decided to try and find a bot that could do what Status Checker did but found none.", inline=False)
        embed.add_field(name="Can I track my members with this?", value="No, this bot tracks **other bots only**", inline=False)
        embed.add_field(name="Can I self host this bot?", value="Yes but I don't recommend it. If you want to find the source code please have a dig around my GitHub profile. I will not link directly to it to discourage you from trying to self host it.", inline=False)
        embed.add_field(name="I have a bug to report", value="Please do so in our [support server ](https://discord.gg/2w5KSXjhGe)", inline=True)
        embed.add_field(name="How do I get started?", value="/add", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Get the down message for your bot")
    @app_commands.describe(member="The user to get the down message for")
    async def config(self, interaction: discord.Interaction, member: discord.Member):
        user_id = member.id
        results = collection.find_one({"_id": user_id})
        
        if results is None:
            return await interaction.responce.send("Hm I can't find that bot in my database!")
        else:
            for query in results:
                if str(query) == "_id":
                    pass
                else:
                    server = results[query]
                    channel = interaction.client.get_channel(server[0])
                    down_message = server[2]
                    auto_publish = server[3]
                    lock = server[5]
                    embed=discord.Embed(title="Config", description="Shows the config of the selected user")
                    embed.add_field(name="Down Message", value=f"{down_message}", inline=True)
                    embed.add_field(name="Channel set", value=f"<#{channel.id}>")
                    embed.add_field(name="Auto Publish", value=f"Auto Publish is set to {auto_publish}", inline=False)
                    embed.add_field(name="Lock", value=f"Locking the server is set to {lock}", inline=True)
                    await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Check the latency of a bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f":ping_pong: Pong!\n **Bot**: {round(interaction.client.latency * 1000)} ms")  
    
    @app_commands.command(description="Give some information about the bot")
    async def stats(self, interaction: discord.Interaction):
        members = 0
        for guild in interaction.client.guilds:
            members += guild.member_count - 1

    
        embed=discord.Embed(title="Status Checker Stats")
        embed.set_author(name="Concept by SamBot#7421", url="https://github.com/wotanut")
        embed.add_field(name="Guilds", value=f"```{len(interaction.client.guilds)}```", inline=True) 
        embed.add_field(name="Users", value=f"```{members}```", inline=True)
        embed.set_footer(text="Thank you for supporting Status Checker :)")
        await interaction.response.send_message(embed=embed)


