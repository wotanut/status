from .data import *
from .driver import *

# TODO: MORE METHODS AND IMPROVE EXISTING METHODS

class Database():
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
    __init__() -> None
        Constructor for the Database class
    __add_json(to_update:json,update:json) -> json
        Adds something to a json object
    __remove_json(to_remove:json) -> json
        Removes a specified key from a json object
    application_is_in_database(id:int) -> bool
        Checks if the application is in the database
    get_all_applications() -> Array
        Gets all the applications in the database
    get_application_from_database(id:int) -> Application
        Gets the application from the database
    add_application_to_database(id:int,type:json,notifications:json) -> bool
        Adds the application to the database
    remove_application_from_database(id:int) -> bool
        Removes the application from the database
    add_application_notification(id:int,notification:json) -> bool
        Adds the notification to the application
    remove_application_notification(id:int,notification:json) -> bool
        Removes the notification from the application
    get_notifications(id:int) -> json
        Gets the notifications of the application
    add_notification(id:int,notification:json) -> bool
        Adds the notification to the application
    remove_notification(id:int,notification:json) -> bool
        Removes the notification from the application
    update_notification(id:int,notification:json) -> bool
        Updates the notification from the user
    add_website(id:int,website:json) -> bool
        Adds a website to the database
    add_bot(id:int,bot:json) -> bool
        Adds a bot to the database
    add_minecraft(id:int,minecraft:json) -> bool
        Adds a minecraft server to the database

    TODO: Add methods for these
    

    remove_website
    update_website

    remove_bot
    update_bot

    remove_minecraft
    update_minecraft
        

    
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

    def __add_json(self,to_update:json,update:json):
            """
            Adds something to a json object

            Parameters
            ----------
            to_update : json
                The json object to update
            update : json
                The json object to update with
            
            Returns
            -------
            json
                The updated json object
            """
            for key in update:
                to_update[key] = update[key]
            return to_update
        
    def __remove_json(self,to_remove:json):
        """
        Removes a specified key from a json object

        Parameters
        ----------
        to_remove : json
            The json object to remove the key from
        
        Returns
        -------
        json
            The updated json object
        """
        for key in to_remove:
            del to_remove[key]
        return to_remove

    def get_all_applications(self):
        """
        Gets all the applications in the database

        Parameters
        ----------
        None

        Returns
        -------
        Array
            An array of Application objects
        """
        applications = []
        for application in self.applications.select("*"):
            applications.append(Application(application[0],application[1],application[2]))
        return applications

    def application_is_in_database(self,id:int):
        """
        Checks if the application is in the database

        Parameters
        ----------
        id : int
            The id of the application to check
        
        Returns
        -------
        bool
            True if the application is in the database, False if not
        """
        if self.applications.select("*",f"id = {id}") != None:
            return True
        return False
    
    def get_application_from_database(self,id:int):
        """
        Gets the application from the database

        Parameters
        ----------
        id : int
            The id of the application to get
        
        Returns
        -------
        Application
            The application object
        """
        if self.application_is_in_database(id):
            return Application(id,self.applications.select("type",f"id = {id}"),self.applications.select("notifications",f"id = {id}"))
        else:
            raise Exception("Application not in database")
    
    def add_application_to_database(self,id:int,type:json,notifications:json):
        """
        Adds the application to the database

        Parameters
        ----------
        id : int
            The id of the application to add
        type : json
            The type of the application
        notifications : json
            The notifications of the application
        
        Returns
        -------
        bool
            True if the application was added, Exception raised if not
        """
        if not self.__application_is_in_database(id):
            self.applications.insert("id,type,notifications",f"{id},{type},{notifications}")
            return True
        else:
            raise Exception("Application already in database")
    
    def remove_application_from_database(self,id:int):
        """
        Removes the application from the database

        Parameters
        ----------
        id : int
            The id of the application to remove
        
        Returns
        -------
        bool
            True if the application was removed, Exception raised if not
        """
        if self.__application_is_in_database(id):
            self.applications.delete(f"id = {id}")
            return True
        else:
            raise Exception("Application not in database")
    
    def add_application_notification(self,id:int,notification:json):
        """
        Adds the notification to the application

        Parameters
        ----------
        id : int
            The id of the application to add the notification to
        notification : json
            The notification to add
        
        Returns
        -------
        bool
            True if the notification was added, Exception raised if not
        """
        if self.__application_is_in_database(id):
            notifications = self.applications.select("notifications",f"id = {id}")
            
            # need to properly update the json object
            
            self.applications.update(f"id = {id}",["notifications"],[notifications])
            return True
        else:
            raise Exception("Application not in database")
    
    def remove_application_notification(self,id:int,notification:json):
        """
        Removes the notification from the application

        Parameters
        ----------
        id : int
            The id of the application to remove the notification from
        notification : json
            The notification to remove
        
        Returns
        -------
        bool
            True if the notification was removed, Exception raised if not
        """
        if self.__application_is_in_database(id):
            notifications = self.applications.select("notifications",f"id = {id}")
            
            # need to properly update the json object
            
            self.applications.update(f"id = {id}",["notifications"],[notifications])
            return True
        else:
            raise Exception("Application not in database")
    
    def get_notifications(self,id:int):
        """
        Gets the notifications for a user

        Parameters
        ----------
        id : int
            The id of the user to get the notifications for
        
        Returns
        -------
        User
            The user object
        """
        if self.users.select("*",f"id = {id}") != None:
            return User(id,self.users.select("applications",f"id = {id}"))
        else:
            raise Exception("User not in database")
    
    def add_notification(self,id:int,notification:json):
        """
        Adds the notification to the user

        Parameters
        ----------
        id : int
            The id of the user to add the notification to
        notification : json
            The notification to add
        
        Returns
        -------
        bool
            True if the notification was added, Exception raised if not
        """
        if self.users.select("*",f"id = {id}") != None:
            notifications = self.users.select("applications",f"id = {id}")
            
            # need to properly update the json object
            
            self.users.update(f"id = {id}",["applications"],[notifications])

            self.add_application_notification(notification["application"],notification)
            return True
        else:
            raise Exception("User not in database")
    
    def remove_notification(self,id:int,notification:json):
        """
        Removes the notification from the user

        Parameters
        ----------
        id : int
            The id of the user to remove the notification from
        notification : json
            The notification to remove
        
        Returns
        -------
        bool
            True if the notification was removed, Exception raised if not
        """
        if self.users.select("*",f"id = {id}") != None:
            notifications = self.users.select("applications",f"id = {id}")
            
            # need to properly update the json object
            
            self.users.update(f"id = {id}",["applications"],[notifications])

            self.remove_application_notification(notification["application"],notification)
            return True
        else:
            raise Exception("User not in database")
    
    def update_notification(self,id:int,notification:json):
        """
        Updates the notification from the user

        Parameters
        ----------
        id : int
            The id of the user to update the notification from
        notification : json
            The notification to update
        
        Returns
        -------
        bool
            True if the notification was updated, Exception raised if not
        """
        if self.users.select("*",f"id = {id}") != None:
            notifications = self.users.select("applications",f"id = {id}")
            
            # need to properly update the json object
            
            self.users.update(f"id = {id}",["applications"],[notifications])
            return True
        else:
            raise Exception("User not in database")
    
    async def add_website(self,url:str,user:int,notifications:json):
        """
        Adds the website to the database

        Parameters
        ----------
        url : str
            The url of the website to add
        user : int
            The id of the user to add the website to
        notifications : json
            The notifications of the website
        
        Returns
        -------
        bool
            True if the website was added, Exception raised if not
        """
        
        pass

    async def add_minecraft(self, url:str, user:int, notifications:json):
        """
        Adds the minecraft server to the database

        Parameters
        ----------
        url : str
            The url of the minecraft server to add
        user : int
            The id of the user to add the minecraft server to
        notifications : json
            The notifications of the minecraft server
        
        Returns
        -------
        bool
            True if the minecraft server was added, Exception raised if not
        """
        
        pass

    async def add_bot(self, id:int, user:int, notifications:json):
        """
        Adds the bot to the database

        Parameters
        ----------
        id : int
            The id of the bot to add
        user : int
            The id of the user to add the bot to
        notifications : json
            The notifications of the bot
        
        Returns
        -------
        bool
            True if the bot was added, Exception raised if not
        """
        
        pass