import json
from dataclasses import dataclass
from enum import Enum
import datetime

@dataclass
class Application:
    """
    Parameters
    ----------
    id : int
        The id of the application
    type : json
        The type of the application
    notifications : json
        Notifications for the application
    
    Returns
    -------
    Application
        The application
    """
    id: int
    type: json
    notifications: json

@dataclass
class User:
    """
    Parameters
    ----------
    id : int
        The id of the user
    applications : json
        The applications the user has

    Returns
    -------
    User
        The user
    """
    id: int
    applications: json

class Meta:
    """
    Metadata for Status Checker

    Parameters
    ----------
    None

    Attributes
    ----------
    version : str
        The version of the Status Checker
    version_name : str
        The name of the version of the Status Checker
    start_time : datetime
        The time the Status Checker was started
    """
    version = "2.0.0"
    version_name = "Finley"
    start_time = datetime.datetime.now()

@dataclass
class Notification():
    """
    Parameters
    ----------
    type : str
        The type of notification
    target : str
        The target of the notification
    Payload : str
        The payload of the notification

    
    Returns
    -------
    notification
        The notification
    """
    type: str
    target: str
    payload: str

class notificationType(Enum):
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