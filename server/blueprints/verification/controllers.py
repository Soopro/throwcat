# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param, get_args
from apiresps.validations import Struct
from flask import current_app

from .helpers import *
from .errors import *


@output_json
def get_question(user_slug, question_slug):
    User = current_app.mongodb.User
    user = User.find_one_by_slug(user_slug)
    if not user:
        raise AppNotFoundError

    Question = current_app.mongodb.Question
    question = Question.find_one_by_slug_and_oid(question_slug,
                                                 user["_id"])
    if not question:
        raise QuestionIdError

    return output_question(user, question)


@output_json
def put_answer():
    answer = get_param('answer', Struct.Dict, True)
    token = get_param('token', Struct.Text, True)
    app_key = get_args('app_key', Struct.Text, True)

    User = current_app.mongodb.User
    user = User.find_one_by_key(app_key)
    if not user:
        raise CheckError
    verified, data = decode_signature(token)
    if not verified:
        raise CheckError
    Question = current_app.mongodb.Question
    question = Question.find_one_by_id_and_oid(data['question_id'],
                                               data["owner_id"])
    if not question:
        raise CheckError
    verified, signature = check_answer(user, data, answer, app_key)
    if verified:
        return {
            "result": "succeed",
            "signature": signature,
        }
    return {"result": "fail"}


@output_json
def confirm():
    signature = get_param('signature', Struct.Text, True)
    app_secret = get_param('app_secret', Struct.Token, True)

    validated, data = decode_signature(signature)

    if not validated:
        raise ComfirmdError
    User = current_app.mongodb.User
    user = User.find_one_by_key_and_secret(data['app_key'], app_secret)
    if not user:
        raise ComfirmdError

    return {"result": "succeed"}
