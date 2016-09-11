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
    answer = get_param('answer', Struct.Dict, required=True)
    token = get_param('token', Struct.Text, required=True)
    app_key = get_args('app_key', required=True)

    User = current_app.mongodb.User
    user = User.find_one_by_key(app_key)
    if not user:
        return {"verified": False}
    verified, signature_payload = decode_signature(token)
    if not verified:
        return {"verified": False}
    Question = current_app.mongodb.Question
    question = Question.find_one_by_id_and_oid(signature_payload['question_id'],
                                               user["_id"])
    if not question:
        return {"verified": False}
    verified, signature = check_answer(question, user,
                                       signature_payload, answer, app_key)
    if verified:
        return {
            "verified": True,
            "signature": signature,
        }
    return {"verified": False}


@output_json
def confirm():
    signature = get_param('signature', Struct.Text, required=True)
    app_secret = get_param('app_secret', Struct.Token, required=True)

    validated, data = decode_signature(signature)

    if not validated:
        return {"confirmed": False}
    User = current_app.mongodb.User
    user = User.find_one_by_key_and_secret(data['app_key'], app_secret)
    if not user:
        return {"confirmed": False}

    return {"confirmed": True}
