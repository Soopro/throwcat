# coding=utf-8
from .controllers import *

urlpatterns = [
    # open apis
    ('/question', get_question, 'POST'),
    ('/answer', put_answer, 'POST'),
    ('/comfirmation', confirm, 'POST'),
]
