import csv
import urllib.request
import requests


from flask import redirect, render_template, request, session
from functools import wraps
from html.parser import HTMLParser


def login():
    # login function
    """ TODO Chris """

def register():
    # registration and login function
    """ TODO Chris """

def pHash():
    # encrypts user password
    """ TODO Chris """

def L():
    # check if user is logged in
    """ TODO Chris """

def logout():
    # logs user out
    """ TODO Chris """

def stats():
    #  gives user NR correct and % correct
    """ TODO Chris """

def ranks():
    # gives user ranking in NR and % lists
    """ TODO Chris """

def questions():
    # gives list of lists of questions from external DB
    class Client(object):
        def __init__(self):
                self.__API_BASEURL = 'https://opentdb.com'
                self.__API_ENDPOINT = '/api.php'
                self.__API_TOKEN_ENDPOINT = '/api_token.php'
                self.__API_TOKEN = False

        def __apiRequest(self, url, params):
            """
                Used internally by the Client object to make calls to the API.
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
                unescape = HTMLParser().unescape
                questions_list = []
                for question_dict in questions_from_tdb:
                    category = unescape(question_dict['category'])
                    type = question_dict['type']
                    difficulty = question_dict['difficulty']
                    question = unescape(question_dict['question'])
                    correct_answer = unescape(question_dict['correct_answer'])
                    incorrect_answers = unescape(question_dict['incorrect_answers'])
                    questions_list.extend((category, type, difficulty, question, correct_answer, incorrect_answers))



                return questions_list

def store():
    # stores data of answered question in user's stat DB
    """ TODO Chris """

def topNR():
    # gives top 10 of users based on questions answered correctly
    """ TODO Chris """

def topP():
    # gives top 10 of users based on % questions answered correctly
    """ TODO Chris """

def compare():
    # search for onther user's stats based on user name
    """ TODO Chris """

def result():
    # checks answers + provides correct answer
    """ TODO Dido """
