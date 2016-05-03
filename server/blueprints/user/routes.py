# coding=utf-8
from __future__ import absolute_import
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
    ('/security/password', change_password, 'PUT'),

    ('/security/secret', get_secret, 'GET'),
    ('/security/secret', reset_secret, 'PUT'),

]
