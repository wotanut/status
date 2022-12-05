# local imports

from .driver import Driver
from .data import Application, Notification

# required imports

import json

class DatabaseV2():
    """
    Database class

    Attributes
    ----------
    applications : Driver
        The applications table
    users : Driver
        The users table

    Methods
    -------
    """
    def __init__(self):
        """
        Constructor for the Database class

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.applications = Driver("Applications","id TEXT PRIMARY KEY, type JSON, notifications JSON")
        self.users = Driver("Users", "id TEXT PRIMARY KEY, applications JSON")

    def __add_json(self, old_json: json, json_to_add :json):
        """
        Adds the json to the end of the old json

        Parameters
        ----------
        old_json : JSON
            The old json
        json_to_add : JSON
            The json to add

        Returns
        -------
        JSON
        """
        old_json.update(json_to_add)
        return old_json

    def __remove_json(self, old_json: json, key: str):
        """
        Removes the json from the old json

        Parameters
        ----------
        old_json : JSON
            The old json
        key : str
            The key to remove

        Returns
        -------
        JSON
        """
        del old_json[key]
        return old_json

    def __nuke(self):
        """
        Nukes the database, let's hope you know what you're doing.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.applications.delete(where="id != 69420123") #bodge
        self.users.delete(where="id != 'admin'")

    def get_all_applications(self):
        """
        Gets all the applications in the database

        Parameters
        ----------
        None

        Returns
        -------
        Array of Applications
        """
        applications = []
        for application in self.applications.select("*"):
            applications.append(Application(int(application[0]),json.loads(application[1],parse_int=int),json.loads(application[2],parse_int=int)))
        return applications

    def get_application_from_database(self, id:int=None, name:str=None):
        """
        Gets the application from the database

        Parameters
        ----------
        id : int, optional
            The id of the application
        name : str, optional
            The name of the application

        Returns
        -------
        Application

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if id:
            application = self.applications.select("*", f"id = {id}")
        elif name:
            application = self.applications.select("*", f"name = {name}")
        else:
            return ValueError("id and name cannot both be None")
        return Application(int(application[0]),json.loads(application[1]),json.loads(application[2]))

    def get_application_notifications(self, id:int=None, name:str=None):
        """
        Gets the notifications for the application

        Parameters
        ----------
        id : int, optional
            The id of the application
        name : str, optional
            The name of the application

        Returns
        -------
        Array of Notifications

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        notifications = []
        if id:
            application = self.applications.select("*", "id = ?", (id,))
        elif name:
            application = self.applications.select("*", "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
        for notification in application[2]:
            notifications.append(Notification(notification[0],notification[1],notification[2]))
        return notifications
    
    def add_application_to_database(self, application:Application):
        """
        Adds the application to the database

        Parameters
        ----------
        application : Application
            The application to add

        Returns
        -------
        None
        """
#         repos.insert("`name`,`description`,`url`,`language`",f"'{nam}' , '{desc}' , '{link}' , '{lang}'")
        self.applications.insert(columns="`id`, `type`, `notifications`",values=f"'{application.id}', '{application.type}', '{application.notifications}'")

    def add_notification_to_application(self, id:int=None, name:str=None, notification:Notification=None):
        """
        Adds the notification to the application

        Parameters
        ----------
        id : int, optional
            The id of the application
        name : str, optional
            The name of the application
        notification : Notification
            The notification to add

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if notification is None:
            return ValueError("notification cannot be None")

        if id:
            application = self.applications.select("*", "id = ?", (id,))
        elif name:
            application = self.applications.select("*", "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
        application[2] = self.__add_json(application[2], notification)
        self.applications.update(application[0],application[1],application[2])

    def remove_application_from_database(self, id:int=None, name:str=None):
        """
        Removes the application from the database

        Parameters
        ----------
        id : int, optional
            The id of the application
        name : str, optional
            The name of the application

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if id:
            self.applications.delete("id = ?", (id,))
        elif name:
            self.applications.delete("name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
    
    def remove_notification_from_application(self, id:int=None, name:str=None, notification:Notification=None):
        """
        Removes the notification from the application

        Parameters
        ----------
        id : int, optional
            The id of the application
        name : str, optional
            The name of the application
        notification : Notification
            The notification to remove

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if notification is None:
            return ValueError("notification cannot be None")

        if id:
            application = self.applications.select("*", "id = ?", (id,))
        elif name:
            application = self.applications.select("*", "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
        application[2] = self.__remove_json(application[2], notification)
        self.applications.update(application[0],application[1],application[2])

    def update_application_in_database(self, id:int=None, name:str=None, application:Application=None):
        """
        Updates the application in the database

        Parameters
        ----------
        id : int, optional
            The id of the application
        name : str, optional
            The name of the application
        application : Application
            The application to update

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if application is None:
            return ValueError("application cannot be None")

        if id:
            self.applications.update(application.id, application.type, application.notifications, "id = ?", (id,))
        elif name:
            self.applications.update(application.id, application.type, application.notifications, "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
    
    def update_notification_in_application(self, id:int=None, name:str=None, notification:Notification=None):
        """
        Updates the notification in the application

        Parameters
        ----------
        id : int, optional
            The id of the application
        name : str, optional
            The name of the application
        notification : Notification
            The notification to update

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if notification is None:
            return ValueError("notification cannot be None")

        if id:
            application = self.applications.select("*", "id = ?", (id,))
        elif name:
            application = self.applications.select("*", "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
        application[2] = self.__remove_json(application[2], notification)
        application[2] = self.__add_json(application[2], notification)
        self.applications.update(application[0],application[1],application[2])

    # USERS
    
    def add_subscription_to_user(self, id:int=None, name:str=None, Application:Application=None, Notification:Notification=None):
        """
        Adds the subscription to the user

        Parameters
        ----------
        id : int, optional
            The id of the user
        name : str, optional
            The name of the user
        Application : Application
            The application to add
        Notification : Notification
            The notification to add

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if Application is None or Notification is None:
            return ValueError("subscription cannot be None")

        if id:
            user = self.users.select("*", "id = ?", (id,))
        elif name:
            user = self.users.select("*", "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
        user[2] = self.__add_json(user[2], Notification)
        self.users.update(user[0],user[1],user[2])
    
    def remove_subscription_from_user(self, id:int=None, name:str=None, Application:Application=None, Notification:Notification=None):
        """
        Removes the subscription from the user

        Parameters
        ----------
        id : int, optional
            The id of the user
        name : str, optional
            The name of the user
        Application : Application
            The application to remove
        Notification : Notification
            The notification to remove

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if Application is None:
            return ValueError("subscription cannot be None")

        if id:
            user = self.users.select("*", "id = ?", (id,))
        elif name:
            user = self.users.select("*", "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
        user[2] = self.__remove_json(user[2], Notification)
        self.users.update(user[0],user[1],user[2])

    def update_subscription_in_user(self, id:int=None, name:str=None, Application:Application=None, Notification:Notification=None):
        """
        Updates the subscription in the user

        Parameters
        ----------
        id : int, optional
            The id of the user
        name : str, optional
            The name of the user
        Application : Application
            The application to update
        Notification : Notification
            The notification to update

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if Application is None or Notification is None:
            return ValueError("subscription cannot be None")

        if id:
            user = self.users.select("*", "id = ?", (id,))
        elif name:
            user = self.users.select("*", "name = ?", (name,))
        else:
            return ValueError("id and name cannot both be None")
        user[2] = self.__remove_json(user[2], Notification)
        user[2] = self.__add_json(user[2], Notification)
        self.users.update(user[0],user[1],user[2])

    def get_user_subscriptions(self):
        """
        Gets the user subscriptions

        Parameters
        ----------
        None

        Returns
        -------
        list
            The list of subscriptions

        Raises
        ------
        None
        """
        subscriptions = []
        for user in self.users.select("*"):
            for application in user[2]:
                for notification in application[1]:
                    subscriptions.append(Application(user[0], application[0], notification[0]))
        return subscriptions