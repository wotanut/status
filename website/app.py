from flask import Flask, render_template, redirect


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/bot/invite")
def invite():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=845943691386290198&permissions=2147896384&scope=bot%20applications.commands"),302

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

# error handlers

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run()