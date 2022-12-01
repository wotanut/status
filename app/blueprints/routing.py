# quart imports
from quart import Blueprint, redirect, request, render_template

routing = Blueprint("routing", __name__)

@routing.route("/")
async def index():
    return await render_template("index.html")

@routing.route("/docs")
async def docs():
    return await render_template("docs.html")

@routing.route("/about")
async def about():
    return await render_template("about.html")

@routing.route("/dashboard")
async def dashboard():
    return await render_template("dashboard.html")

@routing.route("/privacy")
async def privacy():
    return await render_template("privacy.html")
