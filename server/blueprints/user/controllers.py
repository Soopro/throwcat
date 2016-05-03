# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param
from apiresps.validations import Struct
from utils.auth import (generate_hashed_password,
                        check_hashed_password)
from flask import current_app, g

from .helpers import *
from .errors import *


# regsister
# # open apis
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
    key = get_param("key", Struct.Alias, True)
    captcha = get_param("captcha", Struct.Token, True)
    login = get_param("login", Struct.Email, True)
    password = get_param("password", Struct.Pwd, True)

    User = current_app.mongodb_conn.User
    if User.find_one_by_login(login):
        raise UserHasExisted

    if not check_captcha(login, captcha):
        raise CaptchaError

    user = User()
    user["name"] = key
    user["login"] = login
    user["password_hash"] = generate_hashed_password(password)
    user.save()

    profile = current_app.mongodb_conn.Profile()
    profile["user_id"] = user["_id"]
    profile["key"] = generate_key(user["_id"])
    profile["secret"] = generate_secret()
    profile.save()

    del_captcha(login)

    return output_user(user)


# recovery
# # open apis
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


# login
# # open apis
@output_json
def login():
    login = get_param("login", Struct.Email, True)
    password = get_param("password", Struct.Pwd, True)

    User = current_app.mongodb_conn.User
    user = User.find_one_by_login(login)
    if not user:
        raise UserNotFound

    if not check_hashed_password(str(user["password_hash"]), password):
        raise PasswordError

    return output_user_with_token(user)


# # for user
@output_json
def get_user_info():
    user = g.curr_user

    return output_user(user)


@output_json
def change_password():
    old_password = get_param("old_password", Struct.Pwd, True)
    new_password = get_param("new_password", Struct.Pwd, True)

    user = g.curr_user

    if not check_hashed_password(str(user["password_hash"]), old_password):
        raise PasswordError

    user["password_hash"] = generate_hashed_password(new_password)
    user.save()

    return output_user(user)


# profile
# # for user
@output_json
def get_profile():
    user = g.curr_user

    Profile = current_app.mongodb_conn.Profile
    profile = Profile.find_one_by_user_id(user["_id"])
    if not profile:
        raise ProfileNotFound

    return output_profile(profile)


@output_json
def reset_profile():
    user = g.curr_user

    Profile = current_app.mongodb_conn.Profile
    profile = Profile.find_one_by_user_id(user["_id"])
    if not profile:
        raise ProfileNotFound

    profile["secret"] = generate_secret()
    profile.save()

    return output_profile(profile)
