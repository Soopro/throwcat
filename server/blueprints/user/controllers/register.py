# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param
from apiresps.validations import Struct
from utils.auth import generate_hashed_password
from flask import current_app

from ..helpers import *
from ..errors import *


@output_json
def get_register_captcha():
    login = get_param("login", Struct.Login, required=True)

    login = login.lower()

    User = current_app.mongodb.User
    if User.find_one_by_login(login):
        raise UserHasExisted

    captcha = send_register_captcha_by_email(login)

    if current_app.debug is True:
        checked = captcha
    else:
        checked = True

    return {
        "login": login,
        "checked": checked,
    }


@output_json
def register():
    slug = get_param("slug", Struct.Slug, required=True)
    captcha = get_param("captcha", Struct.Token, required=True)
    login = get_param("login", Struct.Login, required=True)
    passwd = get_param("passwd", Struct.Pwd, required=True)

    login = login.lower()

    User = current_app.mongodb.User
    if User.find_one_by_login(login):
        raise UserHasExisted

    if not check_register_captcha(login, captcha):
        raise CaptchaError

    display_name = slug
    email = login

    user = User()
    user["slug"] = slug
    user["login"] = login
    user["display_name"] = display_name
    user["password_hash"] = generate_hashed_password(passwd)
    user["email"] = email
    user["app_key"] = generate_key(slug)
    user["app_secret"] = generate_secret()
    user.save()

    del_register_captcha(login)

    return {
        "login": login,
        "updated": user["updated"],
    }
