# coding=utf-8
from .controllers import *

urlpatterns = [
    # open apis
    ('/verfication', get_question, 'GET'),
    ('/verfication', put_answer, 'POST'),
    ('/comfirmation', confirm, 'POST'),
]
