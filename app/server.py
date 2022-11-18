import flask
from flask import Flask, jsonify, render_template, redirect

app = Flask(__name__)

# routing
 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# api

@app.route("/api")
def api():
    return jsonify({"status": "ok"})

@app.route("/api/get_from_db/<id>")
def get_from_db(id):
    """ Get's an application from the database and returns a json object of the stats"""
    return jsonify({"status": "ok"})

@app.route("/api/add_to_db/<id>")
def add_to_db(id):
    """ Adds an application to the database """
    return jsonify({"status": "ok"})

@app.route("/api/remove_from_db/<id>")
def remove_from_db(id):
    """ Removes an application from the database """
    return jsonify({"status": "ok"})

# redirects

@app.route("/discord")
def discord():
    return redirect("https://discord.gg/2w5KSXjhGe")

@app.route("/youtube")
def youtube():
    return redirect("https://www.youtube.com/channel/UCIVkp1F5JSyE0IKALyPW5sg")


def check_if_database_exists():
    """ Checks if the database exists, if it doesn't it will create it """
    pass

app.run(host="0.0.0.0",port=1234)