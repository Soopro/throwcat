# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param
from apiresps.validations import Struct
from flask import current_app

from .helpers import *
from .errors import *


@output_json
def get_question():
    app_key = get_param('app_key', Struct.Token, True)
    question_id = get_param('question_id', Struct.ObjectId, True)

    User = current_app.mongodb.User
    user = User.find_one_by_key(app_key)
    if not user:
        raise AppKeyError

    Question = current_app.mongodb.Question
    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise QuestionIdError

    return output_question(user, question)


@output_json
def put_answer():
    point = get_param('point', Struct.Dict, True)
    ssid = get_param('ssid', Struct.Id, True)

    app_key, question_id, index = decode_ssid(ssid)

    User = current_app.mongodb.User
    user = User.find_one_by_key(app_key)
    if not user:
        raise SsidError

    Question = current_app.mongodb.Question
    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise SsidError

    if check_answer(question, index, point):
        set_pass_ssid(ssid)
        return {"result": "succeed"}
    else:
        return {"result": "fail"}


@output_json
def confirm():
    ssid = get_param('ssid', Struct.Id, True)
    app_secret = get_param('app_secret', Struct.Token, True)

    app_key, qeustion_id, index = decode_ssid(ssid)

    User = current_app.mongodb.User
    user = User.find_one_by_key_and_secret(app_key, app_secret)
    if not user:
        raise ComfirmdError

    if not check_pass_ssid(ssid):
        raise ComfirmdError

    return {"result": "succeed"}
