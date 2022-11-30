# pytest imports
import pytest

# local imports
from ..app.utilities import data,database,driver

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
 

class TestDatabase:

    def test_init(self):
        db = database.Database()
        assert db.applications != None
        assert db.users != None
        
# NOTE: The test for driver is not required, I plan to do more things with the driver seperatly from this project.