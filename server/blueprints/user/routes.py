#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .controllers import *

urlpatterns = [
    # open apis
    ('/regsister', regsister, 'POST'),
    ('/captcha', get_captcha, 'POST'),
    ('/recovery', recovery, 'POST'),
    ('/recovery/captcha', get_recovery_captcha, 'POST'),
    ('/login', login, 'POST'),

    # for uesr
    ('/info', get_user_info, 'GET'),
    ('/profile', get_profile, 'GET'),
    ('/profile', reset_profile, 'POST'),
    ('/security/password', change_password, 'POST'),
    # ('/security/key', get_key, 'GET'),
    # ('/security/key', recovery_key, 'PUT'),

]
