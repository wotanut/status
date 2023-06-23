from dataclasses import dataclass
from enum import Enum
import datetime


class Meta:
    """
    Metadata for Status Checker

    Attributes
    ----------
    version : str
        The version of Status Checker
    version_name : str
        The name of the version of Status Checker
    start_time : datetime
        The time the Status Checker was started
    """
    version = "2.0.0"
    version_name = "Finley"
    start_time = datetime.datetime.now()

class ApplicationType:
    """
    Attributes
    ----------

    """
    DISCORD_BOT = "DBOT"
    WEB = "WEB"
    MINECRAFT = "MINECRAFT"

class NotificationType(Enum):
    """
    Supported types of notifications

    Attributes
    ----------
    WEBHOOK : str
        A webhook
    EMAIL : str
        An email
    DISCORD_DM : str
        A discord direct message
    DISCORD_CHANNEL : str
        A discord channel message
    SMS : str
        An sms

    Returns
    -------
    notificationType
        The notification type
    """
    WEBHOOK = "WEBHOOK"
    EMAIL = "EMAIL"
    DISCORD_DM = "DISCORD_DM"
    DISCORD_CHANNEL = "DISCORD_CHANNEL"
    SMS = "SMS"

@dataclass
class User:
    """
    Attributes
    ----------
    id : int
        The id of the user, this is the same as their discord ID
    notifications : List
		A list of notification ID's that the user owns
    """
    id: int
    notifications: list

@dataclass
class Notification():
    """
    Attributes
    ----------
    id: int
		The id of the notification
    type : NotificationType
        The type of notification
    target : str
        The target of the notification, must be consistent with the type
    Payload : str
        The payload of the notification
    """
    id: int
    type: NotificationType
    target: str
    payload: str

@dataclass
class Application:
    """
    Attributes
    ----------
    id : int
        The id of the application
    type : AplicationType
		The type of application
    notifications : list
        A list of notifications that should be fired when the application goes down
    """
    id: int
    name: str
    icon: str
    type: ApplicationType
    notifications: list
