import discord
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
import json
import discord
import sqlite3

class Driver():
    def __init__(self,table_name,columns=""):
        """
        Generates a database object

        Parameters
        ----------
        table_name : str
            The name of the table to be created
        columns : str
            The columns to be created in the table
        """
        self.conn = sqlite3.connect("database.db")
        self.table_name = table_name

        self.create_table(f"{table_name}",f"{columns}")
    
    def create_table(self,table_name,columns):
        """
        Creates a table in the database

        Parameters
        ----------
        table_name : str
            The name of the table to be created
        columns : str
            The columns to be created in the table
        """

        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({columns})")
        self.conn.commit()

    def insert(self,columns,values):
        """
        Inserts a row into the table

        Parameters
        ----------
        columns : str
            The columns to be inserted into
        values : str
            The values to be inserted into the columns
        """
        self.conn.execute(f"INSERT INTO {self.table_name}({columns}) VALUES({values})")
        self.conn.commit()

    def select(self,columns,where=None):
        """
        Selects a row from the table

        Parameters
        ----------
        columns : str
            The columns to be selected from
        Where : str, optional
            The where statement to be used, defualts to None
        """
        if where:
            return self.conn.execute(f"SELECT {columns} FROM {self.table_name} WHERE {where}")
        else:
            return self.conn.execute(f"SELECT {columns} FROM {self.table_name}")

    def update(self,where,columns=[],values=[]):
        """
        Updates a row in the table

        Parameters
        ----------
        where : str
            The where statement to be used
        columns : list, optional
            The columns to be updated, defualts to []
        values : list, optional
            The values to be updated, defualts to []
        """
        if len(columns) != len(values):
            raise Exception("columns and values must be the same length")
        else:
            statement = ""
            for c in columns:
                statement = statement + (f"{c} = {values[columns.index(c)]}")
                if columns.index(c) != len(columns) - 1:
                    statement = statement + ", "
            print(f"UPDATE {self.table_name} SET {statement} WHERE {where}")
        self.conn.execute(f"UPDATE {self.table_name} SET {statement} WHERE {where}")
        self.conn.commit()
    
    def delete(self,where):
        """
        Deletes a row from the table

        Parameters
        ----------
        where : str
            The where statement to be used
        """
        self.conn.execute(f"DELETE FROM {self.table_name} WHERE {where}")
        self.conn.commit()
    
    def close(self):
        self.conn.close()

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
        Checks if the application is in the database
        """

        return True # temporary

    @staticmethod
    def get_from_database(id: int):
        """
        Gets the application from the database
        """

        return "e" # will return the json object
    
    @staticmethod
    def remove_from_database(id: int):
        """
        Removes the application from the database
        """

        return True

    @staticmethod
    def remove_notification_from_database(notification: str):
        """
        Removes the notification from the database
        """

        return True

    @staticmethod
    def webhook(data):
        """
        Sends a webhook
        """

        url = data['url']
        content_type = data['content']
        payload = data['payload']

        r = requests.post(url, data=json.dumps(payload), headers={'Content-Type': content_type})

        return True

    @staticmethod
    def email(data):
        """
        Sends an email to the user
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

    @staticmethod
    def sms(data):
        """
        Sends an sms to the user
        """

        pass

    async def check_applications(self,bot: discord.Bot):
        """
        Checks all the applications in the database
        """



        pass