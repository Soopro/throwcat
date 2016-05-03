# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param
from apiresps.validations import Struct
from utils.auth import generate_hashed_password
from flask import current_app

from .helpers import *
from .errors import *


@output_json
def get_recovery_captcha():
    email = get_param("email", Struct.Email, True)

    User = current_app.mongodb_conn.User
    if not User.find_one_by_login(email):
        raise UserNotFound

    captcha = send_recovery_captcha_by_email(email)

    if current_app.debug is True:
        return {
            "captcha": captcha
        }
    else:
        return {
            "result": "success"
        }


@output_json
def recovery():
    login = get_param("login", Struct.Email, True)
    new_password = get_param("new_password", Struct.Pwd, True)
    captcha = get_param("captcha", Struct.Token, True)

    if not check_recovery_captcha(login, captcha):
        raise CaptchaError

    User = current_app.mongodb_conn.User
    user = User.find_one_by_login(login)
    if not user:
        raise UserNotFound

    user["password_hash"] = generate_hashed_password(new_password)
    user.save()

    return output_user(user)
