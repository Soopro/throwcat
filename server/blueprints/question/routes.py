#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .controllers import *

urlpatterns = [
    # open apis
    ('/', get_questions, 'GET'),
    ('/<alias>', get_question, 'GET'),
    
    # for admin
    ('/<alias>', create_question, 'POST'),
    ('/<alias>', update_question, 'PUT'),
    ('/<alias>', delete_question, 'DELETE'),
]
