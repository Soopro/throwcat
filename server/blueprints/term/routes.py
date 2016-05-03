#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .controllers import *

urlpatterns = [
    # open apis
    ('/', get_verify_terms, 'GET'),
    ('/<alias>', get_verify_term, 'GET'),
    
    # for admin
    ('/<alias>', create_verify_term, 'POST'),
    ('/<alias>', update_verify_term, 'PUT'),
    ('/<alias>', delete_verify_term, 'DELETE'),
]
