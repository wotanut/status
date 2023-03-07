# pytest imports
import pytest

# local imports
from ..app.utilities import data,driver, database_v2

# other imports
import json

class TestData:

    def test_application(self):
        app = data.Application(id=1,type="test",notifications="test")
        assert app.id == 1
        assert app.type == "test"
        assert app.notifications == "test"

    def test_user(self):
        user = data.User(id=1,applications="test")
        assert user.id == 1
        assert user.applications == "test"

    # NOTE: Meta is a static object so there is no need to test it

    def test_notification(self):
        notif = data.notificationType
        assert notif.EMAIL.value == "EMAIL"
        assert notif.WEBHOOK.value == "WEBHOOK"
        assert notif.DISCORD_DM.value == "DISCORD_DM"
        assert notif.DISCORD_CHANNEL.value == "DISCORD_CHANNEL"
        assert notif.SMS.value == "SMS"

# TODO: Properly setup the database for each test 

class TestDatabase:

    # sterilize the database
    def setup_method(self):
        json_type = """{"type": "dbot", "url": "None", "bot_id": 123456, "name" :"Test Bot"}"""
        self.json_type_i = json.loads(json_type,parse_int=int)
        json_notifications = """
        {
            "1" :{
                "type": "WEBHOOK",
                "target": "https://discord.com/api/webhooks/1234567890/1234567890",
                "payload": "None"
            },
            "2" : {
                "id" : 2,
                "type": "DISCORD_DM",
                "target": "123456789",
                "payload": "Your Application is down"
            },
            "3" : {
                "id" : 3,
                "type": "DISCORD_CHANNEL",
                "target": "123456789",
                "payload": "Your Application {application_name} is down"
            },
            "4" :{
                "id" : 4,
                "type": "EMAIL",
                "target": "test@test",
                "payload": "Your Application is down"
            },
            "5" :{
                "id" : 5,
                "type": "SMS",
                "target": "123456789",
                "payload": "Your Application is down"
            }
        }
        """
        self.json_notifications_i = json.loads(json_notifications,parse_int=int)

    def test_init(self):
        db = database_v2.DatabaseV2()
        assert db.applications != None
        assert db.users != None

    def test_add_json(self):
        db = database_v2.DatabaseV2()
        json = db._DatabaseV2__add_json({"test_1": "_test_key"},{"test_2":"test_value"})
        assert json == {"test_1": "_test_key","test_2":"test_value"}
        assert json != {"test_1": "_test_key"}
    
    def test_remove_json(self):
        db = database_v2.DatabaseV2()
        json = db._DatabaseV2__remove_json({"test_1": "_test_key","test_2":"test_value"},"test_2")
        assert json == {"test_1": "_test_key"}
        assert json != {"test_1": "_test_key","test_2":"test_value"}

    def test_nuke(self):
        db = database_v2.DatabaseV2()
        # app = data.Application(id=1,type=json.loads(self.json_type),notifications=json.loads(self.json_notifications))
        # db.add_application_to_database(app)
        db._DatabaseV2__nuke()
        assert db.get_all_applications() == []

    def test_applications(self):
        """
        Tests everything that could be in the applications section of the database.

        Methods
        -------
        get_all_applications()
        get_application_from_database(id, name)
        get_application_notifications(id, name)

        add_application_to_database(app)
        add_notification_to_application(id, name, notification)

        remove_application_from_database(id, name)
        remove_notification_from_application(id, name, notification_id)

        update_application_in_database(id, name, app)
        update_notification_in_application(id, name, notification)
        """
        db = database_v2.DatabaseV2()
        assert db.get_all_applications() == []
        app = data.Application(id=1,type=json.dumps(self.json_type_i),notifications=json.dumps(self.json_notifications_i))
        db.add_application_to_database(app)
        
        # assert db.get_all_applications() == [app]
        assert db.get_application_from_database(1) == app
        assert db.get_application_from_database(2) == None
        assert db.get_application_from_database() == ValueError
        assert db.get_application_from_database("Test Bot") == app

    def test_users(self):
        """
        Tests everything that could be in the users section of the database

        Methods
        -------
        add_subscription_to_user(id,name,application,notification)
        remove_subscription_from_user(id,name,application,notification)
        update_subscription_in_user(id,name,application,notification)
        get_user_subscriptions(id)
        """




        


        
        
# NOTE: The test for driver is not required, I plan to do more things with the driver seperatly from this project.