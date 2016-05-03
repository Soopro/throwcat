#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .controllers import *

urlpatterns = [
    # open apis
    ('/register', register, 'POST'),
    ('/register/captcha', get_register_captcha, 'POST'),
    ('/recovery', recovery, 'POST'),
    ('/recovery/captcha', get_recovery_captcha, 'POST'),
    ('/login', login, 'POST'),

    # for uesr
    ('/profile', get_profile, 'GET'),
    ('/security/password', change_password, 'POST'),

    ('/security/secret', get_secret, 'GET'),
    ('/security/secret', reset_secret, 'PUT'),

]
