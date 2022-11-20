import discord
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
import json
import discord
import mcstatus

# local imports
from utilities.data import Application, User, notificationType
from utilities.database import Database

class Helper():
    """
    Helper class

    Returns
    -------
    Helper
        The helper class
    """
    def __init__(self):
        """
        Constructor
        
        Returns
        -------
        Helper
            The helper class
        """
        self.Database = Database()
        pass

    def webhook(self,data):
        """
        Sends a webhook

        Parameters
        ----------
        data : json
            The data to send the webhook with

        Returns
        -------
        Void
        """

        url = data['url']
        content_type = data['content']
        payload = data['payload']

        r = requests.post(url, data=json.dumps(payload), headers={'Content-Type': content_type})

        return True

    def email(self,data):
        """
        Sends an email to the user

        Parameters
        ----------
        data : json
            The data to send the email with

        Returns
        -------
        Void
        """

        sender_email = "wotanutt@gmail.com"
        receiver_email = data["email"]
        password = os.getenv("EMAIL_PASSWORD")

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
        Hi {data['name']}, your service {data['service']} is down.
        
        This is an automated message, please do not reply to this email.
        """
        html = """\
        <html>
        <body>
            <p>Hi {data['name']}, your service {data['service']} is down.</p>
            <br>
            <p>This is an automated message, please do not reply to this email.</p>
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        
        return True

    def sms(self,data):
        """
        Sends an sms to the user
        """

        pass

    async def discord_direct_message(self,data,bot):
        """
        Sends a direct message to the user on discord
        """

        user_id = int(data["id"])
        user = await bot.get_user(user_id)
        await user.send(data["content"] + "\n \n This is an automated message, please do not reply. To cancel this message, please remove the application from your dashboard.")

        pass

    async def discord_server(self,data,bot):
        """
        Sends a discord message to the server
        """

        pass

    async def send_notification(self,notification:json,bot=discord.Bot):
        """
        Sends the notification to the user

        Parameters
        ----------
        notification : json
            The notification to send
        bot : discord.Bot
            The bot to send the notification with if the notification type is that of Helper.discord
        
        Returns
        -------
        bool
            True if the notification was sent, Exception raised if not
        """
        
        # no switch case in python :(

        if notification["type"] == notificationType.WEBHOOK.value:
            self.webhook(notification)
        elif notification["type"] == notificationType.EMAIL.value:
            self.email(notification)
        elif notification["type"] == notificationType.SMS.value:
            self.sms(notification)
        elif notification["type"] == notificationType.DISCORD_DM.value:
            self.discord_direct_message(notification,bot)
        elif notification["type"] == notificationType.DISCORD_CHANNEL.value:
            self.discord_server(notification,bot)
        else:
            raise Exception("Invalid notification type")

        return True

    async def check_applications(self,bot: discord.Bot):
        """
        Checks all the applications in the database

        Parameters
        ----------
        bot : discord.Bot
            The bot to send the notification with if the notification type is that of Helper.discord

        Returns
        -------
        Void
        """

        for app in self.Database.get_all_applications():
            # web apps
            if app.type["name"] == "web":
                try:
                    r = requests.get(app.url)
                    if r.status_code != 200:
                        await self.send_notification(app.notifications, bot)
                        pass
                except:
                    await self.send_notification(app.notifications, bot)
                    pass

            # minecraft servers

            if app.type["name"] == "mc":
                try:
                    mc = mcstatus.JavaServer.lookup(app.url)
                    status = mc.ping()
                except:
                    await self.send_notification(app.notifications, bot)
                    pass
