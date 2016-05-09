# coding=utf-8
from __future__ import absolute_import

import random
from flask import current_app

from .errors import *


def set_pass_ssid(ssid):
    EXPIRE = 5 * 60
    current_app.redis.setex(ssid, "pass", EXPIRE)
    return ssid


def check_pass_ssid(ssid):
    if current_app.redis.get(ssid):
        return True
    else:
        return False


def encode_ssid(user, question, index):
    return "{}-{}-{}".format(user["app_key"], question["_id"], index)


def decode_ssid(ssid):
    app_key, question_id, index = ssid.split("-")
    try:
        index = int(index)
    except Exception:
        raise SsidError

    return app_key, question_id, index


def check_answer(question, index, point):
    try:
        resource = question["resources"][index]
    except Exception:
        raise SsidError

    crop = resource["recipe"]["crop"]
    if (crop["x"] <= point["x"] <= crop["x"] + crop["w"]) and \
       (crop["y"] <= point["y"] <= crop["y"] + crop["h"]):
        return True
    else:
        return False


def output_question(user, question):
    random_index = random.randint(0, len(question["resources"]) - 1)
    return {
        "ssid": encode_ssid(user, question, random_index),
        "title": question["title"],
        "type": question["type"],
        "resource": question["resources"][random_index]
    }
