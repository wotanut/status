import discord
from discord.ext import commands
from discord.ext.commands import command, Cog
from pymongo import MongoClient
import asyncio
import os
import datetime
from datetime import time


# database connection

cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]

class events(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

    updated = []

    @commands.Cog.listener()
    async def on_presence_update(before,after):
        if not before.bot:
            return

        if before.status == after.status:
            return

        if before.id in updated:
            return
            
        updated.append(before.id)

        try:
            await asyncio.sleep(10)
        
            double_check = bot.get_user(before.id)
        
            if before.status != double_check.status:
                return
        except:
            pass
            
        user = bot.get_user(before.id)
        try:
            results = collection.find()
            for result in results:

                if str(result["_id"]) != str(user.id):
                    # pass do literally nothing
                    pass
                else:
                    for query in result:
                        if str(query) == "_id":
                            pass
                        else:
                            server = result[query]
                            channel = bot.get_channel(server[0])
                            msg = await channel.fetch_message(server[1])
                            down_message = server[2]
                            auto_publish = server[3]
                            owner = int(server[4])
                            lock = server[5]

                            if str(after.status) == "online":
                                await msg.edit(content=f"<:online:949589635061915648> {user.mention} is online")
                                if lock == True:
                                    perms = channel.overwrites_for(channel.guild.default_role)
                                    perms.send_messages=True
                                    await channel.set_permissions(channel.guild.default_role, overwrite=perms)

                            elif str(after.status) == "idle":
                                await msg.edit(content=f"<:idle:949589635087081503> {user.mention} is on idle")
                                if lock == True:
                                    perms = channel.overwrites_for(channel.guild.default_role)
                                    perms.send_messages=True
                                    await channel.set_permissions(channel.guild.default_role, overwrite=perms)
                            elif str(after.status) == "dnd":
                                await msg.edit(content=f"<:dnd:949589635091284019> {user.mention} is on do not disturb")
                                if lock == True:
                                    perms = channel.overwrites_for(channel.guild.default_role)
                                    perms.send_messages=True
                                    await channel.set_permissions(channel.guild.default_role, overwrite=perms)
                            else:
                                await msg.edit(content=f"<:offline:949589634898350101> {user.mention} is offline")
                                if lock == True:
                                    perms = channel.overwrites_for(channel.guild.default_role)
                                    perms.send_messages=False
                                    await channel.set_permissions(channel.guild.default_role, overwrite=perms)

                            down_msg = await channel.send(down_message)
                            if auto_publish == True:
                                try:
                                    await down_msg.publish()
                                except:
                                    pass

                            try:
                                user = bot.get_user(owner)
                                await user.send(down_message)
                            except:
                                pass
                            
        except Exception as e:
            print(e)
            pass
        await asyncio.sleep(10)
        updated.remove(before.id)

    @commands.Cog.listener()
    async def on_guild_remove(guild):
        channel = bot.get_channel(947126649378447400)
        embed=discord.Embed(title="I Left a guild", description=f"{guild.name}", color=0xfa0505)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)
        collection.update_many( { }, { "$unset": { str(guild.id): "" } } )

        results = collection.find()
        for result in results:
            counter = 0
            for query in result:
                if str(query) == "_id":
                    # this is the objects ID, all objects have this
                    pass
                else:
                    counter = counter + 1
                if counter == 0:
                    try:
                        collection.delete_one(result)
                    except:
                        pass
    
    @commands.Cog.listener()
    async def on_guild_join(guild):
        channel = bot.get_channel(947126649378447400)
        embed=discord.Embed(title="I joined a guild", description=f"{guild.name}", color=0x5bfa05)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

        async with aiohttp.ClientSession() as session:
            top = 'https://top.gg/api/bots/845943691386290198/stats'
            dsl = 'https://api.discordlist.space/v2/bots/845943691386290198'
            dbg = 'https://discord.bots.gg/api/v1/bots/845943691386290198/stats'
            async with session.post(top,headers={"Authorization": os.getenv("top")},json={"server_count": int(len(bot.guilds))}) as resp:
                response = await resp.json()
                pass
            async with session.post(dsl,headers={"Authorization": os.getenv("dsl")},json={"serverCount": int(len(bot.guilds))}) as resp:
                response = await resp.json()
                pass
            async with session.post(dbg,headers={"Authorization": os.getenv("dbg")},json={"guildCount": int(len(bot.guilds))}) as resp:
                response = await resp.json()
                pass
        
def setup(bot):
  bot.add_cog(events(bot))