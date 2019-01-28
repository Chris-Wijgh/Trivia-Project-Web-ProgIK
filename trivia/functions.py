from cs50 import SQL
from passlib.apps import custom_app_context as pwd_context

import csv
import urllib.request
import requests
import html

from flask import redirect, render_template, request, session
from functools import wraps


db = SQL("sqlite:///trivia.db")


def loginF():
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

        # query database for username
        rows = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return apology("invalid username and/or password")

        return True


def apology(message, code=400):
    ### verandert ###
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def L(f):
    # check if user is logged in
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def stats():
    numbers = db.execute("SELECT * FROM stats WHERE user_id = :user_id", user_id=session["user_id"])
    questions_nr = numbers[0]['vragen_beantwoord']
    correct = numbers[0]['vragen_goed']

    if correct==0 or questions_nr ==0:
        score = 0

    else:
        score = (correct / questions_nr) * 100 * correct

    return correct, score

def ranks():
    rank_nr = 0
    rank_score = 0
    # generate a list of dicts, ranked by Nr vragen goed, highest first
    numbers_ranked = list(reversed(db.execute("SELECT user_id, vragen_goed FROM stats ORDER by vragen_goed")))

    # add a rank Nr to the ordered entries
    counter = 1
    for item in numbers_ranked:
        item["rank"] = counter
        counter += 1

    # retrieve the user's entry
    for item in numbers_ranked:
        if item["user_id"] == session["user_id"]:
            rank_nr = item["rank"]

    # gets the score data for all users in a list of dictionaries
    data = db.execute("SELECT user_id, vragen_goed, vragen_beantwoord FROM stats ORDER by vragen_goed")

     # create a list of id nrs paired with scores
    scores = list()
    for item in data:
        if item["vragen_goed"]==0 or item["vragen_beantwoord"] ==0:
            score=0

        else:
            score = (item["vragen_goed"] / item["vragen_beantwoord"]) * 100 * item["vragen_goed"]

        u_id = item["user_id"]
        scores.append({"user_id":u_id, "user_score":score})

    scores_ranked = list(reversed(scores))

    # add a rank Nr to the ordered entries
    counter = 1
    for item in scores_ranked:
        item["rank"] = counter
        counter += 1


    # retrieve the user's entry
    for item in scores_ranked:
        if item["user_id"] == session["user_id"]:
            rank_score = item["rank"]

    return rank_nr, rank_score


class Questions(object):
        # gives list of lists of questions from external DB
        def __init__(self):
                self.__API_BASEURL = 'https://opentdb.com'
                self.__API_ENDPOINT = '/api.php'
                self.__API_TOKEN_ENDPOINT = '/api_token.php'
                self.__API_TOKEN = False

        def __apiRequest(self, url, params):
            """
                Used internally by the question object to make calls to the API.
                Parameters:
                    -url: the URL of the API endpoint.
                    -params: parameters for the request.
                Returns the JSON response in the form of a Dictionary.
                Otherwise, an exception is raised.
            """
            try:
                response = requests.get(url, params=params)
            except requests.exceptions.RequestException:
                raise ConnectionError('Failed to connect to OpenTDB.')
            try:
                response.raise_for_status()
                response = response.json()
                assert response['response_code'] == 0
                return response
            except:
                raise ValueError
                ''' TODO '''
                # return apology('Something went wrong')

        def getToken(self):
                """
                    Requests a session token from the API.
                    Returns True if session token was successfully obtained.
                    Otherwise, an exception is raised.
                """
                url = self.__API_BASEURL + self.__API_TOKEN_ENDPOINT
                params = { 'command': 'request' }
                response = self.__apiRequest(url, params)
                self.__API_TOKEN = response['token']
                return True

        def getQuestions(self, amount=10, category=0, use_token=False):
                """
                    Requests a set of questions from the API.
                    Parameters:
                        -amount:    how many questions to request.
                        -category:  which category the questions should be from.
                                    If this is set to False, questions will be from all categories.
                        -use_session_token: whether or not to use the token,
                                            which is generated with getToken()
                    Returns a List of Question objects.
                """
                url = self.__API_BASEURL + self.__API_ENDPOINT
                params = { 'amount': amount }
                try:
                    params['category'] = int(category)
                except:
                    params['category'] = 0
                if use_token and self.__API_TOKEN:
                    params['token'] = self.__API_TOKEN
                response = self.__apiRequest(url, params)
                questions_from_tdb = response['results']

                # html parsing
                for x in range(len(questions_from_tdb)):
                    questions_from_tdb[x]['category'] = html.unescape(questions_from_tdb[x]['category'])
                    questions_from_tdb[x]['type'] = html.unescape(questions_from_tdb[x]['type'])
                    questions_from_tdb[x]['difficulty'] = html.unescape(questions_from_tdb[x]['difficulty'])
                    questions_from_tdb[x]['question'] = html.unescape(questions_from_tdb[x]['question'])
                    questions_from_tdb[x]['correct_answers'] = html.unescape(questions_from_tdb[x]['correct_answers'])
                    for i in range(len(questions_from_tdb[x]['incorrect_answers'])):
                        questions_from_tdb[x]['incorrect_answers'][i] =  html.unescape(questions_from_tdb[x]['incorrect_answers'][i])

                return questions_from_tdb
    # gives list of lists of questions from external DB

def topNR():
     # gives top 10 of users based on questions answered correctly

     # gives inverse ranking of users based on questions correct
     nr_rank_low = db.execute("SELECT user_id, vragen_goed FROM stats ORDER by vragen_goed")

     # generate highest 10 ranking users based on questions correct
     nr_rank_10 = list()
     counter = 0
     if counter < 10:
         for item in reversed(nr_rank_low):
             nr_rank_10.append(item)
             counter += 1

     for item in nr_rank_10:
         u_id = item["user_id"]
         username = db.execute("SELECT username FROM userdata WHERE user_id = :user_id", user_id=u_id)
         item["username"] = username[0]["username"]

     return nr_rank_10

def topP():
     # gives top 10 of users based on score

     # gets the relevant data for all users in a list of dictionaries
     data = db.execute("SELECT user_id, vragen_goed, vragen_beantwoord FROM stats ORDER by vragen_goed")

     # create a list of id nrs paired with scores
     scores = list()
     for item in data:
         if item["vragen_goed"]==0 or item["vragen_beantwoord"] ==0:
            score=0
         else:
            score = (item["vragen_goed"] / item["vragen_beantwoord"]) * 100 * item["vragen_goed"]
         u_id = item["user_id"]
         username = db.execute("SELECT username FROM userdata WHERE user_id = :user_id", user_id=u_id)
         scores.append({"user_id":u_id, "username":username[0]["username"],"user_score":score})

    # generate highest 10 ranking users based on score
     score_rank_10 = list()
     counter = 0
     if counter < 10:
         for item in reversed(scores):
            score_rank_10.append(item)
            counter += 1
     return score_rank_10

def compare(other_user):
    # search for other user's ID based on user name
    other_id = db.execute("SELECT user_id FROM userdata WHERE username = :username", username=other_user)

    # search for other user's stat's based on other user's ID
    numbers = db.execute("SELECT * FROM stats WHERE user_id = :user_id", user_id=other_id)
    questions_nr = numbers[0]['vragen_beantwoord']
    other_correct = numbers[0]['vragen_goed']

    if questions_nr == 0 or other_correct == 0:
        other_score = 0

    else:
        other_score = (other_correct / questions_nr) * 100 * other_correct

    # generate a list of dicts, ranked by Nr vragen goed, lowest first
    numbers_ranked = db.execute("SELECT user_id, vragen_goed FROM stats ORDER by vragen_goed")


    # start retrieving other user's rankings
    other_rank_nr = 0
    other_rank_score = 0

    # generate a list of dicts, ranked by Nr vragen goed, highest first
    numbers_ranked = list(reversed(db.execute("SELECT user_id, vragen_goed FROM stats ORDER by vragen_goed")))

    # add a rank Nr to the ordered entries
    counter = 1
    for item in numbers_ranked:
        item["rank"] = counter
        counter += 1

    # retrieve the other user's entry
    for item in numbers_ranked:
        if item["user_id"] == other_id:
            other_rank_nr = item["rank"]

    # gets the score data for all users in a list of dictionaries
    data = db.execute("SELECT user_id, vragen_goed, vragen_beantwoord FROM stats ORDER by vragen_goed")

    # create a list of id nrs paired with scores
    scores = list()
    for item in data:
        if item["vragen_goed"] == 0 or item["vragen_beantwoord"] == 0:
            score = 0

        else:
            score = (item["vragen_goed"] / item["vragen_beantwoord"]) * 100 * item["vragen_goed"]

        u_id = item["user_id"]
        scores.append({"user_id":u_id, "user_score":score})

    scores_ranked = list(reversed(scores))

    # add a rank Nr to the ordered entries
    counter = 1
    for item in scores_ranked:
        item["rank"] = counter
        counter += 1

    # retrieve the other user's entry
    for item in scores_ranked:
        if item["user_id"] == other_id:
            other_rank_score = item["rank"]

    return other_correct, other_score, other_rank_nr, other_rank_score

