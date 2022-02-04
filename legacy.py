### legacy help command


class MyHelp(commands.HelpCommand):
  def get_command_signature(self, command):
    return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)
  async def send_bot_help(self, mapping):
      embed = diskord.Embed(title="Help")
      for cog, commands in mapping.items():
          filtered = await self.filter_commands(commands, sort=True)
          command_signatures = [self.get_command_signature(c) for c in filtered]
          if command_signatures:
              cog_name = getattr(cog, "qualified_name", "No Category")
              embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
      channel = self.get_destination()
      await channel.send(embed=embed)

  async def send_command_help(self, command):
        embed = diskord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()


## legacy add bot command


@commands.has_permissions(manage_guild=True)
@bot.command(help="Adds a bot to watch for status changes")
async def add_bot(ctx):
  await ctx.message.delete()

  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel


  embed = diskord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
  embed.add_field(name = f"Channel:",value = f"None yet! tag one to select", inline = True)
  bed = await ctx.send(embed=embed)

  # get the channel


  try:
        msg = await bot.wait_for("message",check=check, timeout=30)
        await msg.delete()
        try:
          channel = msg.content.replace("<","")
          channel = channel.replace("#","")
          channel = channel.replace(">","")
          try:
            channel = bot.get_channel(int(channel))
          except Exception as e:
            await ctx.send(f"Failed to get channel, this is usually becuase I do not have access or the channel does not exist. \n Error: || {e} ||")
          if type(channel) != diskord.channel.TextChannel:
            await ctx.send("That doesn't look like a text channel")
            await bed.delete()
            return
        except:
          await ctx.send("That doesn't look like a channel to me")
          await bed.delete()
          return
        embed = diskord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"None yet! tag one to select", inline = True)
        await bed.edit(embed=embed)
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")



  # get the bot

  try:
        input = await bot.wait_for("message",check=check, timeout=30)
        await input.delete()
        try:
          user = input.content.replace("<","")
          user = user.replace("@","")
          user = user.replace(">","")
          user = user.replace("!","")
          user = bot.get_user(int(user))
          if not user.bot:
            await ctx.send("For privacy reasons I can only track bots")
            await bed.delete()
            return
          #await ctx.send(f"User's ID is {user.id} \n User Name \n {user.name} \n Mention {user.mention}")
        except:
          await ctx.send("That doesn't look like a bot to me")
          await bed.delete()
          return
        embed = diskord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{user.mention}", inline = True)
        embed.add_field(name = f"Down Message:",value = f"Choose a message to be sent when the bot changes status", inline = True)
        await bed.edit(embed=embed)
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")


  # get the down message


  try:
        down_message = await bot.wait_for("message",check=check, timeout=30)
        await down_message.delete()
        embed = diskord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{user.mention}", inline = True)
        embed.add_field(name = f"Down Message:",value = f"{down_message.content}", inline = True)
        if channel.is_news():
          embed.add_field(name = f"Auto Publish",value = f"I have detected that the channel you selected ({channel.mention}) is an announcement catagory, would you like me to automatically publish the down message?", inline = True)
        await bed.edit(embed=embed)
  except asyncio.TimeoutError:
      await ctx.send("Sorry, you didn't reply in time!")


  # get the state of auto publish (depending on type of channel)

  auto_publish = False
  if channel.is_news():
    try:
        publish = await bot.wait_for("message",check=check, timeout=30)
        await publish.delete()

        yes = ["y", "yes", "afirm","afirmitave", "positive","true"]
        no = ["n", "no", "negative","false"]


        if publish.content.lower() in yes:
          auto_publish = True
        elif publish.content.lower() in no:
          auto_publish = False
          await bed.delete()
          return
        else:
          await ctx.send(f"I couldn't tell what that meant, you must pick from one of the following options {yes}{no}")

        embed = diskord.Embed(title = f"Status Checker", color= int("0x36393f", 16))
        embed.add_field(name = f"Channel:",value = f"{channel.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{user.mention}", inline = True)
        embed.add_field(name = f"Bot:",value = f"{down_message.content}", inline = True)
        embed.add_field(name = f"Auto Publish",value = f"{publish.content}", inline = True)
        await bed.edit(embed=embed)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        await bed.delete()
        return
  message = await channel.send(f"<a:loading:844891826934251551> Loading Status Checker information")

  try:
    collection.insert_one({"_id": user.id, f"{ctx.guild.id}": [channel.id,message.id,down_message.content,auto_publish]})
  except Exception as e:
    collection.update_one({"_id": user.id}, {"$set" : {f"{ctx.guild.id}": [channel.id,message.id,down_message.content,auto_publish]}})

  await ctx.send(f"Watching {user.mention} I will alert you if their status changes")
