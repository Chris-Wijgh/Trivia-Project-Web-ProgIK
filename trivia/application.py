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





@app.route("/")
@app.route("/frontpage", methods=["GET"])
@L
def front_page():

    ''' front page linking to login and registration '''

    return render_template("frontpage.html")


### TODO Jesper


# login
@app.route("/login", methods=["GET", "POST"])
def login():

    ''' logs user in '''

    if loginF() == True:
        # remember which user has logged in
        rows = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["user_id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    '''' logs user out '''

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


# register
@app.route("/register", methods=["GET", "POST"])
def register():

    ''' registers new user '''

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

        #ensure password confirmation was submitted
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
        session["user_id"] = rows[0]["user_id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# index
@app.route("/index", methods=["GET", "POST"])
@L
# def index():

#     ''' generate user stats '''

#     stats()
#     correct = correct
#     score = score

#     # generate user ranking in all lists
#     ranks()
#     rank_nr = rank_nr
#     rank_score = rank_score

#     return render_template("index.html", correct=correct, score=score, rank_nr=rank_nr, rank_score=rank_score)

def index():
    return render_template("index.html")

# questions
@app.route("/questions", methods=["GET", "POST"])
@L
def questions():

    ''' user gets trivia questions to answer '''
    opentdb_session = Questions()
    opentdb_session.getToken()
    dbquestions = opentdb_session.getQuestions(amount=10, use_token=True, category=22)

    # question_dict = {}
    # for x in dbquestions:
    #     question_dict['question'] = x['question']
    #     question_dict['correct_answer'] = x['correct_answer']
    #     question_dict['incorrect_answers'] = x['incorrect_answers']
    #     all_answers = x['incorrect_answers']
    #     all_answers.append(x['correct_answer'])
    #     question_dict['all_answers'] = all_answers


    for x in range(9):
        L = dbquestions[x]['incorrect_answers']
        L.append(dbquestions[x]['correct_answer'])
        dbquestions[x]['all_answers'] = L

    return render_template("questions.html", dbquestions=dbquestions)


# result
@app.route("/result", methods=["GET"])
@L
def result():

    ''' user gets right/wrong + correct answers, stores score stats in user-stats DB '''

    return apology('something went wrong')




# Top 10
@app.route("/top10", methods=["GET"])
@L
def ab():
    return apology('t')




# compare
@app.route("/compare", methods=["GET", "POST"])
@L
# def compare_page():

#     ''' get and present the info after the user asks for it '''

#     if request.method == "POST":

#         # get the user's stats and ranks
#         stats()
#         correct = correct
#         score = score

#         ranks()
#         rank_nr = rank_nr
#         rank_score = rank_score


#         # get the other user's stats and ranks
#         other_user = request.form.get("other_user_name")
#         compare(other_user)

#         other_correct = other_correct
#         other_score = other_score
#         other_rank_nr = other_rank_nr
#         other_rank_score = other_rank_score

#         return render_template("compared.html", correct=correct, score=score, rank_nr=rank_nr, rank_score=rank_score, other_correct=other_correct, other_score=other_score, other_rank_nr=other_rank_nr, other_rank_score=other_rank_score)

#     # otherwise give the basic page
#     return render_template("compare.html")

def b():
    return apology('t')
# compared
@app.route("/compared", methods=["GET", "POST"])
@L
# def compared():

#     ''' get and present more info if the user asks for it '''

#     if request.method == "POST":

#         # get the user's stats and ranks
#         stats()
#         correct = correct
#         score = score

#         ranks()
#         rank_nr = rank_nr
#         rank_score = rank_score


#         # get the other user's stats and ranks
#         other_user = request.form.get("other_user_name")
#         compare(other_user)

#         other_correct = other_correct
#         other_score = other_score
#         other_rank_nr = other_rank_nr
#         other_rank_score = other_rank_score

#         return render_template("compared.html", correct=correct, score=score, rank_nr=rank_nr, rank_score=rank_score, other_correct=other_correct, other_score=other_score, other_rank_nr=other_rank_nr, other_rank_score=other_rank_score)

#     # otherwise give the basic page if the user somehow lands here without being sent by "compare"
#     return render_template("compared.html")
def c():
    return apology('t')