# Data from the applications table

## type
```
{
    id : The applications unique ID. THIS IS NOT A BOT ID
    "type" : " either dbot, web or mc"
    url : " the url of the application" <- only applicable for MC and WEB
    bot_id : " the bot id of the application" <- only applicable for dbot
    name : " the name of the application"
}
```

## notifications
```
{
    <AN ID, THIS MATCHES EXACTLY TO THE APPLICATION IN THE USERS TABLE> : {
        "type" : "email sms discord_dm etc...",
        email : {
            address : "the email address to send to",
            content : "the content of the email"
        }
        sms : {
            number : "the number to send to",
            content : "the content of the sms"
        }
        discord_dm : {
            id : "the id of the user to send to",
            content : "the content of the dm"
        }
        discord_channel : {
            id : "the id of the channel to send to",
            content : "the content of the message"
            auto_publish : bool
            lock_server : bool
            pin : bool
        }
        webhook : {
            url : "the url of the webhook",
            payload : "the content of the webhook"
            content_type " usually application/json but can also be other types"
        }
    }
}
```

# Data from the users tables

## applications
```
{
    id : "user ID <- randomly generated",
    subscriptions : {
        application_id : "the id of the application",
        notification_id : "the id of the notification"
    }
}
```