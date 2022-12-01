# quart iports
from quart import Blueprint, jsonify

api = Blueprint("api", __name__)


@api.route("/")
async def api():
    return await jsonify({"status": "ok"})

@api.route("/get_from_db/<id>")
async def get_from_db(id):
    """ Get's an application from the database and returns a json object of the stats"""
    return await jsonify({"status": "ok"})

@api.route("/add_to_db/<id>")
async def add_to_db(id):
    """ Adds an application to the database """
    return await jsonify({"status": "ok"})

@api.route("/remove_from_db/<id>")
async def remove_from_db(id):
    """ Removes an application from the database """
    return await jsonify({"status": "ok"})