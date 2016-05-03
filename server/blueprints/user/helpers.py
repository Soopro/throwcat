# coding=utf-8
from __future__ import absolute_import

from utils.auth import generate_token
from utils.helpers import (random_string,
                           check_random_string,
                           hmac_sha,
                           str2int)
from flask import current_app
from uuid import uuid4


def set_captcha(key):
    EXPIRE = 5 * 60
    num, captcha = random_string(length=6)
    key = "{}-captcha".format(key)
    current_app.redis.setex(key, num, EXPIRE)
    return captcha


def check_captcha(key, captcha):
    key = "{}-captcha".format(key)
    num = str2int(current_app.redis.get(key))

    return check_random_string(int(num), captcha)


def del_captcha(key):
    key = "{}-captcha".format(key)
    current_app.redis.delete(key)


def set_recovery_captcha(key):
    EXPIRE = 5 * 60
    num, captcha = random_string(length=6)
    key = "{}-recovery-captcha".format(key)
    current_app.redis.setex(key, num, EXPIRE)
    return captcha


def check_recovery_captcha(key, captcha):
    key = "{}-recovery-captcha".format(key)
    num = str2int(current_app.redis.get(key))

    return check_random_string(int(num), captcha)


def del_recovery_captcha(key):
    key = "{}-recovery-captcha".format(key)
    current_app.redis.delete(key)


def generate_key(user_id):
    return unicode(user_id).upper()


def generate_secret():
    return unicode(uuid4().hex).upper()


def generate_user_token(user):
    sha = hmac_sha(user['login'], user['password_hash'])
    return generate_token({
        'user_id': str(user['_id']),
        'sha': sha,
    })


def send_captcha_by_email(email):
    captcha = set_captcha(email)

    subject = ""
    template = ""
    context = ""

    current_app.system_mail_pusher.send_system_mail(email,
                                                    subject,
                                                    template,
                                                    context)

    return captcha


def send_recovery_captcha_by_email(email):
    captcha = set_recovery_captcha(email)

    subject = ""
    template = ""
    context = ""

    current_app.system_mail_pusher.send_system_mail(email,
                                                    subject,
                                                    template,
                                                    context)

    return captcha


def output_user(user):
    return {
        "id": user["_id"],
        "login": user["login"],
        "name": user["name"]
    }


def output_user_with_token(user):
    token = generate_user_token(user)
    user = output_user(user)
    user["token"] = token
    return user


def output_profile(profile):
    return {
        "key": profile["key"],
        "secret": profile["secret"]
    }