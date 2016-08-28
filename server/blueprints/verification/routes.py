# coding=utf-8
from .controllers import *

urlpatterns = [
    # open apis
    ('/user/<user_slug>/question/<question_slug>', get_question, 'GET'),
    ('/answer', put_answer, 'POST'),
    ('/confirm', confirm, 'POST'),
]
