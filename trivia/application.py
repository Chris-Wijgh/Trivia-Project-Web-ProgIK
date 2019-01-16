from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from functions import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# front page
@app.route("/")
@app.route("/index", methods=["GET"])

# front page linking to login and registration

### TODO Jesper


# login
@app.route("/login", methods=["GET", "POST"])

# login page for registered users

### TODO Chris


# register
@app.route("/register", methods=["GET", "POST"])

# registration + login for unregistered users

### TODO Chris


# index
@app.route("/index", methods=["GET", "POST"])
@L

# user homepage and own stats

### TODO Chris

# questions
@app.route("/questions", methods=["GET", "POST"])
@L

# user gets trivia questions to answer

### TODO Dido

# result
@app.route("/result", methods=["GET"])
@L

# user gets right/wrong + correct answers, stores score stats in user-stats DB

### TODO Dido

# Top 10
@app.route("/top10", methods=["GET"])
@L

# user gets top 10 lists of NR questions correct and % questions correct

### TODO Chris

# compare
@app.route("/compare", methods=["GET", "POST"])
@L

# user can search for onther user's stats based on user name

### TODO Chris


# compared
@app.route("/compared", methods=["GET", "POST"])
@L

# user gets stats based on query in compare + can search again

### TODO Chris

# apology
@app.route("/apology", methods=["GET"])

# page when something goes wrong

### TODO Jesper












##
##      examples and database import. NEEDS CHANGE.
##

"""

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():

"""



