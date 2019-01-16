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

db = SQL("sqlite:///trivia.db")




# front page
@app.route("/")
@app.route("/index", methods=["GET"])
def front_page():
    return apology('something went wrong')
# front page linking to login and registration

### TODO Jesper


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    return apology('something went wrong')
# login page for registered users

### TODO Chris


# register
@app.route("/register", methods=["GET", "POST"])
def register():
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation")

        # ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password doesn't match")

        # insert new user data into database
        insert = db.execute("INSERT INTO userdata (username, password) VALUES (:username, :password)", username=request.form.get("username") , password=pwd_context.hash(request.form.get("password")))

        if not insert:
            return apology("Username already exists")

        # query database for username
        rows = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# index
@app.route("/index", methods=["GET", "POST"])
#@L
def index():
    return apology('something went wrong')
# user homepage and own stats

### TODO Chris

# questions
@app.route("/questions", methods=["GET", "POST"])
#@L
def questions():
    return apology('something went wrong')

# user gets trivia questions to answer

### TODO Dido

# result
@app.route("/result", methods=["GET"])
#@L
def result():
    return apology('something went wrong')
# user gets right/wrong + correct answers, stores score stats in user-stats DB

### TODO Dido

# Top 10
@app.route("/top10", methods=["GET"])
#@L
def top10():
    return apology('something went wrong')
# user gets top 10 lists of NR questions correct and % questions correct

### TODO Chris

# compare
@app.route("/compare", methods=["GET", "POST"])
#@L
def compare():
    return apology('something went wrong')
# user can search for onther user's stats based on user name

### TODO Chris


# compared
@app.route("/compared", methods=["GET", "POST"])
#@L
def compared():
    return apology('something went wrong')
# user gets stats based on query in compare + can search again

### TODO Chris

'''

# apology
 @app.route("/apology", methods=["GET"])
 def a():
     return apology('something went wrong')
 page when something goes wrong

### TODO Jesper
'''











##
##      examples and database import. NEEDS CHANGE.
##

# """

# # configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


# @app.route("/")
# @app.route("/index", methods=["GET", "POST"])
# @login_required
# def index():

# """



## test