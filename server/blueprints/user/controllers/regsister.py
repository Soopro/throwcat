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
def get_captcha():
    email = get_param("email", Struct.Email, True)

    captcha = send_captcha_by_email(email)

    if current_app.debug is True:
        return {
            "captcha": captcha
        }
    else:
        return {
            "result": "success"
        }


@output_json
def regsister():
    slug = get_param("slug", Struct.Alias, True)
    display_name = get_param("display_name", Struct.Text, True)
    captcha = get_param("captcha", Struct.Token, True)
    login = get_param("login", Struct.Email, True)
    password = get_param("password", Struct.Pwd, True)

    User = current_app.mongodb_conn.User
    if User.find_one_by_login(login):
        raise UserHasExisted

    if not check_captcha(login, captcha):
        raise CaptchaError

    user = User()
    user["slug"] = slug
    user["login"] = login
    user["display_name"] = display_name
    user["password_hash"] = generate_hashed_password(password)
    user["email"] = login
    user["app_key"] = generate_key(slug)
    user["app_secret"] = generate_secret()
    user.save()

    del_captcha(login)

    return output_user(user)
