# pytest imports
import pytest

# required imports
import discord
from discord.ext import commands

# local imports
from ..app.views import modals as modals
class TestModal:

    @pytest.mark.asyncio
    async def test_generate_json(self):
        assert await modals.generate_json("dm", "845943691386290198", "Your application is down!") == {
            "NotificationType": "dm",
            "NotificationTarget": "845943691386290198",
            "NotificationPayload": "Your application is down!"
        }

    @pytest.mark.asyncio
    async def test_is_valid(self):
        # dm
        assert await modals.is_valid(NotificationType="dm",NotificationTarget="",bot=discord.Client) == True
        assert await modals.is_valid(NotificationType="dm",NotificationTarget="klij;shuyogrqwe8o9fs",bot=discord.Client) == True

        # guild
        assert await modals.is_valid(NotificationType="guild",NotificationTarget="asdf",bot=discord.Client) == "Your notification target is invalid. Please try again."
        assert await modals.is_valid(NotificationType="dm",NotificationTarget="939479619587952640",bot=discord.Client) == True

        # webhook
        assert await modals.is_valid(NotificationType="webhook",NotificationTarget="asdf",bot=discord.Client) == "Your notification target is invalid. Please try again."
        assert await modals.is_valid(NotificationType="webhook",NotificationTarget="https://sblue.tech/webhook/test",bot=discord.Client) == True

        # email
        assert await modals.is_valid(NotificationType="email",NotificationTarget="asdf",bot=discord.Client) == "Your notification target is invalid. Please try again."
        assert await modals.is_valid(NotificationType="email",NotificationTarget="sam@sblue.tech",bot=discord.Client) == True