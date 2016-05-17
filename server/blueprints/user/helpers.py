# coding=utf-8
from __future__ import absolute_import

from utils.auth import generate_token
from utils.short_url import (random_short_url,
                             check_random_short_url)
from utils.misc import (hmac_sha,
                           parse_int)
from flask import current_app
from uuid import uuid4


def set_register_captcha(key):
    EXPIRE = 5 * 60 * 60
    key = "{}-register-captcha".format(key)
    stored_num = parse_int(current_app.redis.get(key), None)
    num, captcha = random_short_url(length=6, preset_int=stored_num)
    current_app.redis.setex(key, num, EXPIRE)
    return captcha


def check_register_captcha(key, captcha):
    key = "{}-register-captcha".format(key)
    num = parse_int(current_app.redis.get(key), None)
    return check_random_short_url(num, captcha)


def del_register_captcha(key):
    key = "{}-register-captcha".format(key)
    current_app.redis.delete(key)


def set_recovery_captcha(key):
    EXPIRE = 15 * 60
    key = "{}-recovery-captcha".format(key)
    stored_num = parse_int(current_app.redis.get(key), None)
    num, captcha = random_short_url(length=6, preset_int=stored_num)
    current_app.redis.setex(key, num, EXPIRE)
    return captcha


def check_recovery_captcha(key, captcha):
    key = "{}-recovery-captcha".format(key)
    num = parse_int(current_app.redis.get(key), None)
    return check_random_short_url(num, captcha)


def del_recovery_captcha(key):
    key = "{}-recovery-captcha".format(key)
    current_app.redis.delete(key)


def generate_key(slug):
    return u"{}-{}".format(slug, uuid4().hex.upper())


def generate_secret():
    return unicode(uuid4().hex).upper()


def generate_user_token(user):
    sha = hmac_sha(user['login'], user['password_hash'])
    return generate_token({
        'user_id': str(user['_id']),
        'sha': sha,
    })


def send_register_captcha_by_email(email):
    captcha = set_register_captcha(email)

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
