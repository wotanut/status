import discord
import discord.ui as ui
import re
 
# local imports

from utilities.database import Database


async def generate_json(NotificationType, NotificationTarget, NotificationPayload):
    return {
        "NotificationType": NotificationType,
        "NotificationTarget": NotificationTarget,
        "NotificationPayload": NotificationPayload
    }

async def is_valid(interaction: discord.Interaction,NotificationType, NotificationTarget, bot: discord.Client):
    notificationTypes = ["dm","guild","webhook","email"]

    if NotificationType.lower() not in notificationTypes:
        await interaction.response.send_message("Your notification type is invalid. Please try again.")
        return
    
        # TODO: Change this to utilities.data.notificationType
    
    if NotificationType.lower() == "dm":
        try:
            user = await bot.fetch_user(int(NotificationTarget))
        except:
            await interaction.response.send_message("Your notification target is invalid. Please try again.")
            return
    elif NotificationType.lower() == "guild":
        try:
            guild = await bot.fetch_guild(int(NotificationTarget))
        except:
            await interaction.response.send_message("Your notification target is invalid. Please try again.")
            return
    elif NotificationType.lower() == "webhook":
        regex = re.search(r"(http|https)://[a-zA-Z0-9./]+", NotificationTarget)
        if regex == None:
            await interaction.response.send_message("Your notification target is invalid. Please try again.")
            return
    elif NotificationType.lower() == "email":
        regex = re.search(r"[a-z0-9]+@[a-z0-9]+\.[a-z]+", NotificationTarget)
        if regex == None:
            await interaction.response.send_message("Your notification target is invalid. Please try again.")
            return

class Setup(ui.Modal,title="Setup"):
        # ServiceType = ui.Select(placeholder="Select a service type",min_values=1,max_values=1, options=[
        #     discord.SelectOption(label="Web Server", value="website",emoji="<:website:1046716159682166815>"),
        #     discord.SelectOption(label="Bot", value="bot",emoji="<:bot_dev:945077689394536528>"),
        #     discord.SelectOption(label="Minecraft Server", value="mc",emoji="<:MC:1044914771612405760>"),
        # ])
        # TODO: As soon as discord supports select menus in modals, uncomment this

        ServiceType = ui.TextInput(label="Service Type (website,bot,mc)",placeholder="website",required=True,row=0)
        ServiceURL = ui.TextInput(label="Service URL (bot_name)#(discriminator) or url",placeholder="https://sblue.tech/uptime",required=False)

        NotificationType = ui.TextInput(label="Notification Type",placeholder="dm",required=True)
        NotificationTarget = ui.TextInput(label="Notification Target",placeholder="845943691386290198",required=True)
        NotificationPaylod = ui.TextInput(label="Notification Payload",placeholder="Your application is down!",required=True)
    
        

        async def on_submit(self, interaction: discord.Interaction):
            if self.ServiceType.value.lower() == "website":
                ui.Modal.clear_items(self)
                print("Clearing items")
                self.add_item(ui.TextInput(label="Service URL (websites and mc only)",placeholder="https://sblue.tech/uptime",required=False))
                print("Added item")
            


            # if await is_valid(interaction,self.NotificationType.value, self.NotificationTarget.value, interaction.client) == False:
            #     return

            # if self.ServiceType.value.lower() == "website":
            #     if self.ServiceURL.value == None:
            #         await interaction.response.send_message("Your service type is website but you did not provide a service URL. Please try again.")
            #         return
            #     regex = re.search(r"(http|https)://[a-zA-Z0-9./]+", self.ServiceURL.value)
            #     if regex == None:
            #         await interaction.response.send_message("Your service URL is invalid. Please try again.")
            #         return
                
            #     json = await generate_json(self.NotificationType.value, self.NotificationTarget.value, self.NotificationPaylod.value)
            #     Database.add_website(interaction.user.id, self.ServiceURL.value,json)

                

            #     await interaction.response.send_message("Subscribed to website " + self.ServiceURL.value)

            # elif self.ServiceType.value.lower() == "mc":
            #     if self.ServiceURL.value == None:
            #         await interaction.response.send_message("Your service type is minecraft but you did not provide a service URL. Please try again.")
            #         return
            #     regex = re.search(r"(http|https)://[a-zA-Z0-9./]+", self.ServiceURL.value)
            #     if regex == None:
            #         await interaction.response.send_message("Your service URL is invalid. Please try again.")
            #         return

            #     json = await generate_json(self.NotificationType.value, self.NotificationTarget.value, self.NotificationPaylod.value)
            #     Database.add_minecraft(interaction.user.id, self.ServiceURL.value,json)


            #     await interaction.response.send_message("Subscribed to minecraft server " + self.ServiceURL.value)
            
            # elif self.ServiceType.value.lower() == "bot":
            #     if self.Bot.value == None:
            #         await interaction.response.send_message("Your service type is bot but you did not provide a bot. Please try again.")
            #         return
            #     regex = re.search(r"[a-zA-Z0-9]+#[0-9]{4}", self.Bot.value)
            #     if regex == None:
            #         await interaction.response.send_message("Your bot is not. Please try again.")
            #         return

            #     json = await generate_json(self.NotificationType.value, self.NotificationTarget.value, self.NotificationPaylod.value)
            #     Database.add_bot(interaction.user.id, self.Bot.value,json)

            #     await interaction.response.send_message("Subscribed to bot " + self.Bot.value)