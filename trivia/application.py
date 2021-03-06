from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from functions import loginF, L, stats, ranks, Questions, topNR, topP, compare, register_user

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
    ''' Front page
    Redirects user to login and registration.
    '''

    return render_template("frontpage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    ''' Logs user in
    If succesful, redirects user to index.
    '''

    if loginF() == True:

        # remember which user has logged in
        rows = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["user_id"]

        # redirect user to home page
        return redirect(url_for("index"))

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    ''' Logs user out
    and redirects user to login.
    '''

    # forget any user_id
    session.clear()

    # redirect user to login form
    flash('You have been logged out')
    return redirect(url_for("login"))


# register
@app.route("/register", methods=["GET", "POST"])
def register():
    ''' Registers new user
    If succesful, redirects user to index.
    '''
    if register_user() == True:
        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/index", methods=["GET", "POST"])
@L
def index():
    ''' Generates user stats and displays them. '''

    # generate user stats
    statistics = stats()
    correct = statistics[0]
    score = statistics[1]

    # generate user ranking in all lists
    rankings = ranks()
    rank_nr = rankings[0]
    rank_score = rankings[1]

    return render_template("index.html", correct=correct, score=score, rank_nr=rank_nr, rank_score=rank_score)


@app.route("/questions", methods=["GET", "POST"])
@L
def questions():
    ''' User gets trivia questions to answer '''

    # remove any left over questions from database
    db.execute("DELETE FROM questions")

    # get questions from API
    opentdb_session = Questions()
    dbquestions = opentdb_session.getQuestions(amount=10, category=22)

    # add element in dict for all answers
    for x in range(10):
        L = dbquestions[x]['incorrect_answers']
        L.append(dbquestions[x]['correct_answer'])
        dbquestions[x]['all_answers'] = L

    # insert the questions into database
    for i in range(10):
        db.execute("INSERT INTO questions (category, type, difficulty, question, correct_answer) VALUES (:category, :type, :difficulty, :question, :correct_answer)", category=dbquestions[i]['category'].strip(), type=dbquestions[i]['type'].strip(), difficulty=dbquestions[i]['difficulty'].strip(), question=dbquestions[i]['question'].strip(), correct_answer=dbquestions[i]['correct_answer'].strip())

    return render_template("questions.html", dbquestions=dbquestions)


@app.route("/result", methods=["GET", "POST"])
@L
def result():
    ''' Displays the amount of questions the user has correctly answered '''

    # select the correct answers from the db
    correct_answers=db.execute("SELECT question, correct_answer FROM questions")

    correct = 0
    form = request.form

    # if user did not answer all questions, flash an error
    if len(form) < 10:
        flash("You need to answer all questions before submitting")
        return redirect(url_for("questions"))

    allanswers = {}

    # compare the answers
    for i in range(10):
        answered = form[str(i)]

        # create dict for all answers so the user can see what he/she answered
        allanswers[answered] = correct_answers[i]['correct_answer']

        if correct_answers[i]['correct_answer'] == answered:
            correct = correct + 1

    beantwoord_raw = db.execute("SELECT vragen_beantwoord FROM stats WHERE user_id=:user_id", user_id=session["user_id"])
    beantwoord = beantwoord_raw[0]['vragen_beantwoord']

    goed_raw = db.execute("SELECT vragen_goed FROM stats WHERE user_id=:user_id", user_id=session["user_id"])
    goed = goed_raw[0]['vragen_goed']

    beantwoord = beantwoord + 10
    goed = goed + correct

    # update stats in database
    db.execute("UPDATE stats SET vragen_beantwoord = :beantwoord, vragen_goed = :goed WHERE user_id = :user_id", beantwoord = beantwoord, goed = goed, user_id=session["user_id"])

    # remove the data from the database
    db.execute("DELETE FROM questions")

    # return the number of correct answers
    return render_template('end.html', correct=correct, allanswers=allanswers)


@app.route("/top10", methods=["GET"])
@L
def top10():
    ''' Displays top 10 lists to user '''

    top10_lijst = topNR()
    top10_score = topP()

    return render_template('top_10.html', top10_lijst=top10_lijst, top10_score=top10_score)


@app.route("/compare", methods=["GET", "POST"])
@L
def compare_page():
    ''' Get the user's stats and the other user's stats and presents it '''

    other_user = request.form.get("other_user_name")

    # if user input is incorrect, return an error
    if compare(other_user) == False:
        flash("Invalid username!")
        return render_template("index.html")

    other_user_stats = compare(other_user)

    # get the user's stats and ranks
    statistics = stats()
    correct = statistics[0]
    score = statistics[1]

    # generate user ranking in all lists
    rankings = ranks()
    rank_nr = rankings[0]
    rank_score = rankings[1]

    # get the other user's stats and ranks
    other_correct = other_user_stats[0]
    other_score = other_user_stats[1]
    other_rank_nr = other_user_stats[2]
    other_rank_score = other_user_stats[3]

    user = {"correct":correct, "score":score, "rank_nr":rank_nr, "rank_score":rank_score}
    other_user = {"name":other_user, "correct":other_correct, "score":other_score, "rank_nr":other_rank_nr, "rank_score":other_rank_score}

    data = []
    data.append(user)
    data.append(other_user)

    return render_template("compare.html", data=data)
