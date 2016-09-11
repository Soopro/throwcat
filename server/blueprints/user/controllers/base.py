# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param
from apiresps.validations import Struct
from utils.auth import (generate_hashed_password,
                        check_hashed_password)
from flask import current_app, g

from ..helpers import *
from ..errors import *


# open apis
@output_json
def login():
    login = get_param("login", Struct.Email, True)
    password = get_param("passwd", Struct.Pwd, True)

    login = login.lower()

    User = current_app.mongodb.User
    user = User.find_one_by_login(login)
    if not user:
        raise UserNotFound

    if not check_hashed_password(str(user["password_hash"]), password):
        raise PasswordError

    token = generate_user_token(user)

    return {
        "slug": user["slug"],
        "token": token,
    }


# for user
@output_json
def change_password():
    old_passwd = get_param("passwd", Struct.Pwd, True)
    new_passwd = get_param("new_passwd", Struct.Pwd, True)
    # new_passwd2 = get_param("new_passwd2", Struct.Pwd, True)

    user = g.curr_user

    if not check_hashed_password(str(user["password_hash"]), old_passwd):
        raise PasswordError

    user["password_hash"] = generate_hashed_password(new_passwd)
    user.save()
    token = generate_user_token(user)
    return {
        "slug": user["slug"],
        "token": token,
        "updated": user["updated"],
    }


@output_json
def get_profile():
    user = g.curr_user

    return output_user(user)


@output_json
def get_secret():
    user = g.curr_user

    return output_secret(user)


@output_json
def reset_secret():
    user = g.curr_user

    user["app_secret"] = generate_secret()
    user.save()

    return output_secret(user)


# output
def output_user(user):
    return {
        "id": user["_id"],
        "login": user["login"],
        "slug": user["slug"],
        "display_name": user["display_name"],
        "email": user["email"],
        "updated": user["updated"],
        "creation": user["creation"],
    }

def output_secret(user):
    return {
        "id": user["_id"],
        "slug": user["slug"],
        "app_key": user["app_key"],
        "app_secret": user["app_secret"],
    }