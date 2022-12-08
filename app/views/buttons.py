import discord


class Feedback(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            discord.ui.Button(
                label="Feedback Form",
                url="https://forms.gle/aGccPTY8u8QNemzt7",
                style=discord.ButtonStyle.link,
            ))
