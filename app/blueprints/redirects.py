# quart imports

from quart import Blueprint, redirect, request

redirects = Blueprint("redirects", __name__)

@redirects.route("/discord")
async def discord_server():
    return redirect("https://discord.gg/2w5KSXjhGe")

@redirects.route("/youtube")
async def youtube():
    return redirect("https://www.youtube.com/channel/UCIVkp1F5JSyE0IKALyPW5sg")
