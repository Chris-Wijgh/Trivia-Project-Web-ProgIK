from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from functions import loginF, apology, L, stats, ranks, Questions, topNR, topP, compare, register_user

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
    if register_user() == True:
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

# index
@app.route("/index", methods=["GET", "POST"])
@L
def index():

     ''' generate user stats '''

     statistics = stats()
     correct = statistics[0]
     score = statistics[1]

     # generate user ranking in all lists
     rankings = ranks()
     rank_nr = rankings[0]
     rank_score = rankings[1]

     return render_template("index.html", correct=correct, score=score, rank_nr=rank_nr, rank_score=rank_score)

# questions
@app.route("/questions", methods=["GET", "POST"])
@L
def questions():

    ''' user gets trivia questions to answer '''
    # remove any left over questions from database
    db.execute("DELETE FROM questions")

    # get questions from API
    opentdb_session = Questions()
    opentdb_session.getToken()
    dbquestions = opentdb_session.getQuestions(amount=10, use_token=True, category=22)

    # add element in dict for all answers
    for x in range(10):
        L = dbquestions[x]['incorrect_answers']
        L.append(dbquestions[x]['correct_answer'])
        dbquestions[x]['all_answers'] = L

    # insert the questions into database
    for i in range(10):
        db.execute("INSERT INTO questions (category, type, difficulty, question, correct_answer) VALUES (:category, :type, :difficulty, :question, :correct_answer)", category=dbquestions[i]['category'].strip(), type=dbquestions[i]['type'].strip(), difficulty=dbquestions[i]['difficulty'].strip(), question=dbquestions[i]['question'].strip(), correct_answer=dbquestions[i]['correct_answer'].strip())

    return render_template("questions.html", dbquestions=dbquestions)


# result
@app.route("/result", methods=["GET", "POST"])
@L
def result():

    # select the correct answers from the db
    correct_answers=db.execute("SELECT question, correct_answer FROM questions")

    correct = 0
    form = request.form
    # compare the answers
    for i in range(len(form)):
        answered = form[str(i)]
        if correct_answers[i]['correct_answer'] == answered:
            correct = correct+1

    beantwoord_raw = db.execute("SELECT vragen_beantwoord FROM stats WHERE user_id=:user_id", user_id=session["user_id"])
    beantwoord = beantwoord_raw[0]['vragen_beantwoord']

    goed_raw = db.execute("SELECT vragen_goed FROM stats WHERE user_id=:user_id", user_id=session["user_id"])
    goed = goed_raw[0]['vragen_goed']

    beantwoord = beantwoord + 10
    goed = goed + correct

    db.execute("UPDATE stats SET vragen_beantwoord = :beantwoord, vragen_goed = :goed WHERE user_id = :user_id", beantwoord = beantwoord, goed = goed, user_id=session["user_id"])

    # remove the data from the database
    db.execute("DELETE FROM questions")


    # return the number of correct answers
    return render_template('end.html', correct=correct)


# Top 10
@app.route("/top10", methods=["GET"])
@L
def top10():

    top10_lijst = topNR()
    top10_score = topP()

    return render_template('top_10.html', top10_lijst=top10_lijst, top10_score=top10_score)


@app.route("/compare", methods=["GET", "POST"])
@L
def compare_page():
    ''' Get the user's data and the other user's data ready for predentation. '''

    other_user = request.form.get("other_user_name")

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




''' NU NOG OVERBODIG '''
# # compared
# @app.route("/compared", methods=["GET", "POST"])
# @L
# def compared():

#     ''' get and present more info if the user asks for it '''

#     if request.method == "POST":
#         # compare user data with other user's data and send it to the html page
#         data = comparing()
#         user = data[0]
#         other_user = data[1]

#         return render_template("compared.html", user=user, other_user=other_user)

#     # otherwise give the basic page
#     return render_template("compare.html")
