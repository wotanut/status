import discord

import utilities.database_v2 as db

class unSubscribe(discord.ui.Select):
    def __init__(self):
        database = db.DatabaseV2()

        subs = database.get_user_subscriptions()

        options = [

        ]

        for sub in subs:
            options.append(discord.SelectOption(label=sub[0],description=sub[1]))
        options.append(discord.SelectOption(label="All",description="Unsubscribe from all services",emoji="🌐"))
        options.append(discord.SelectOption(label="Cancel",description="Cancel the operation",emoji="❌"))

        super().__init__(placeholder='Select a service', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "All":
            database = db.DatabaseV2()
            for sub in database.get_user_subscriptions():
                database.remove_subscription_from_user(sub[0])
            await interaction.response.edit_message(content = f"Removed all services from the database. You will no longer receive updates for any services",view=None)
        elif self.values[0] == "Cancel":
            await interaction.response.edit_message(content = f"Cancelled operation.",view=None)
            return
        else:
            try:
                database = db.DatabaseV2()
                database.remove_subscription_from_user(self.values[0])
            except Exception as e:
                await interaction.response.edit_message(content = f"Failed to remove {self.values[0]} from the database. Please try again later, or conctact a developer. \n 'n Error: ||{e}||",view=None)

        await interaction.response.edit_message(content = f"Removed {self.values[0]} from the database. You will no longer receive updates for this service",view=None)

class unSubscribeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(unSubscribe())