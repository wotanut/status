from flask import abort, redirect, url_for, Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

# redirects

@app.route('/bot/invite')
def index():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=845943691386290198&permissions=2147896384&scope=bot%20applications.commands")


# errors

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',code="404 - Not Found"), 404