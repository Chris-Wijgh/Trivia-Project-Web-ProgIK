from cs50 import SQL
from passlib.apps import custom_app_context as pwd_context

import csv
import urllib.request
import requests
import html

from flask import redirect, render_template, request, session, flash
from functools import wraps
from operator import itemgetter


db = SQL("sqlite:///trivia.db")


def loginF():
    ''' Logs user into their account '''

    # forget any user_id
    session.clear()

    if request.method == "POST":

        # validate user input
        if not request.form.get("username"):
            return flash("Must provide username!")

        elif not request.form.get("password"):
            return flash("Must provide password!")

        rows = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return flash("Invalid username and/or password")

        return True

def register_user():
    ''' Creates an account for first time users
    and logs user in.
    '''

    # forget any user_id
    session.clear()

    if request.method == "POST":

        # validate user input
        if not request.form.get("username"):
            return flash("Must provide username!")

        elif not request.form.get("password"):
            return flash("Must provide password!")

        elif not request.form.get("confirmation"):
            return flash("Must provide password confirmation!")

        elif request.form.get("password") != request.form.get("confirmation"):
            return flash("Passwords do not match")

        # insert new user data into database and encrypts password
        insert = db.execute("INSERT INTO userdata (username, password) VALUES (:username, :password)", username=request.form.get("username") , password=pwd_context.hash(request.form.get("password")))
        if not insert:
            return flash("Username already exists")

        # log in
        rows = db.execute("SELECT * FROM userdata WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return flash("Invalid username and/or password!")

        # remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # create a stats row for new user
        insert_stats = db.execute("INSERT INTO stats (user_id) VALUES (:user_id)", user_id=session["user_id"])

        return True

def L(f):
    """ Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def stats():
    ''' Queries the number of questions answered correctly
    and caculates a weighted score.
    '''

    # query user stats
    numbers = db.execute("SELECT * FROM stats WHERE user_id = :user_id", user_id=session["user_id"])
    questions_nr = numbers[0]['vragen_beantwoord']
    correct = numbers[0]['vragen_goed']

    # avoid division by zero
    if correct==0 or questions_nr ==0:
        score = 0

    else:
        score = round((correct / questions_nr) * 100 * correct)

    return correct, score

def ranks():
    ''' Calculates the position of the user in the rank list of number of questions answered correctly
    and the rank list of highest score.
    '''

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

        # avoid division by zero
        if item["vragen_goed"]==0 or item["vragen_beantwoord"] ==0:
            score=0

        else:
            score = round((item["vragen_goed"] / item["vragen_beantwoord"]) * 100 * item["vragen_goed"])

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
    def __init__(self):
        ''' Initializes the baseurl and endpoint.'''

        self.__API_BASEURL = 'https://opentdb.com'
        self.__API_ENDPOINT = '/api.php'

    def __apiRequest(self, url, params):
        ''' Used internally by the question object to make calls to the API. '''

        # request from api
        response = requests.get(url, params=params)
        response.raise_for_status()

        # convert to json format
        response = response.json()

        assert response['response_code'] == 0
        return response

    def getQuestions(self, category, amount=10):
        """ Requests a set of questions from the API
        and returns them parsed.
        """

        url = self.__API_BASEURL + self.__API_ENDPOINT

        # set parameters for api request
        params = {'amount': amount}
        params['category'] = int(category)
        response = self.__apiRequest(url, params)
        questions_from_tdb = response['results']

        # HTML parsing
        for x in range(len(questions_from_tdb)):
            questions_from_tdb[x]['category'] = html.unescape(questions_from_tdb[x]['category'])
            questions_from_tdb[x]['type'] = html.unescape(questions_from_tdb[x]['type'])
            questions_from_tdb[x]['difficulty'] = html.unescape(questions_from_tdb[x]['difficulty'])
            questions_from_tdb[x]['question'] = html.unescape(questions_from_tdb[x]['question'])
            questions_from_tdb[x]['correct_answer'] = html.unescape(questions_from_tdb[x]['correct_answer'])

            for i in range(len(questions_from_tdb[x]['incorrect_answers'])):
                questions_from_tdb[x]['incorrect_answers'][i] =  html.unescape(questions_from_tdb[x]['incorrect_answers'][i])

        return questions_from_tdb

def topNR():
     ''' Creates top 10 of users based on questions answered correctly. '''

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
    ''' Creates top 10 of users based on score '''

    # gets the relevant data for all users in a list of dictionaries
    data = db.execute("SELECT user_id, vragen_goed, vragen_beantwoord FROM stats ORDER by vragen_goed")

    # create a list of id nrs paired with scores
    scores = list()
    for item in data:

        # avoid division by zero
        if item["vragen_goed"]==0 or item["vragen_beantwoord"] ==0:
            score=0
        else:
            score = round((item["vragen_goed"] / item["vragen_beantwoord"]) * 100 * item["vragen_goed"])

        u_id = item["user_id"]
        username = db.execute("SELECT username FROM userdata WHERE user_id = :user_id", user_id=u_id)
        scores.append({"user_id":u_id, "username":username[0]["username"],"user_score":score})

    # sorts list based on score
    scores = sorted(scores, key=itemgetter('user_score'))

    # generate highest 10 ranking users based on score
    score_rank_10 = list()
    counter = 0
    if counter < 10:
        for item in reversed(scores):
            score_rank_10.append(item)
            counter += 1

    return score_rank_10

def compare(other_user):
    ''' Compares the stats of the user with another requested user. '''

    # search for other user's ID based on user name, return false if user input is wrong
    try:
        other_id_raw = db.execute("SELECT user_id FROM userdata WHERE username = :username", username=other_user)
        other_id = other_id_raw[0]["user_id"]
    except:
        return False

    # search for other user's stat's based on other user's ID
    numbers = db.execute("SELECT * FROM stats WHERE user_id = :user_id", user_id=other_id)
    questions_nr = numbers[0]['vragen_beantwoord']
    other_correct = numbers[0]['vragen_goed']

    # avoid division by zero
    if questions_nr == 0 or other_correct == 0:
        other_score = 0

    else:
        other_score = round((other_correct / questions_nr) * 100 * other_correct)

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
            score = round((item["vragen_goed"] / item["vragen_beantwoord"]) * 100 * item["vragen_goed"])

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

