import discord

class Helper():
    dm = "dm"
    webhook = "webhook"
    email = "email"
    sms = "sms"
    discord = "discord"
    def __init__(self):
        pass

    @staticmethod
    def check_database(id: int):
        """
        Checks if the bot is in the database
        """

        return True # temporary

    @staticmethod
    def get_notification_type(id: int):
        """
        Gets the notification type of the bot
        """

        return Helper.discord # temporary

    @staticmethod
    def webhook():
        """
        Sends a webhook
        """

        pass

    @staticmethod
    def email():
        """
        Sends an email to the user
        """

        pass

    @staticmethod
    def sms():
        """
        Sends an sms to the user
        """

        pass