# coding=utf-8
from .controllers import *

urlpatterns = [
    # open apis
    ('/', get_verify_terms, 'GET'),
    ('/<term_id>', get_verify_term, 'GET'),

    # for user
    ('/', get_questions, 'GET'),
    ('/<question_id>', get_question, 'GET'),
    ('/', create_question, 'POST'),
    ('/<question_id>', update_question, 'PUT'),
    ('/<question_id>', delete_question, 'DELETE'),

    # for admin
    ('/<term_id>', create_verify_term, 'POST'),
    ('/<term_id>', update_verify_term, 'PUT'),
    ('/<term_id>', delete_verify_term, 'DELETE'),
]
