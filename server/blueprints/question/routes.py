# coding=utf-8
from .controllers.question import *
from .controllers.resource import *

urlpatterns = [
    # question
    ('/', get_questions, 'GET'),
    ('/<question_id>', get_question, 'GET'),
    ('/', create_question, 'POST'),
    ('/<question_id>', update_question, 'PUT'),
    ('/<question_id>', delete_question, 'DELETE'),

    # resource
    ('/<question_id>/resource', get_resources, 'GET'),
    ('/<question_id>/resource/<resource_id>', get_resource, 'GET'),
    ('/<question_id>/resource/', create_resource, 'POST'),
    ('/<question_id>/resource/<resource_id>', update_resource, 'PUT'),
    ('/<question_id>/resource/<resource_id>', delete_resource, 'DELETE'),

]

