# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param
from apiresps.validations import Struct
from flask import current_app, g

from blueprints.question.helpers import *


@output_json
def get_questions():
    user = g.curr_user

    Question = current_app.mongodb_conn.Question
    questions = Question.find_all_by_oid(user["_id"])

    return [output_question(question) for question in questions]


@output_json
def get_question(question_id):
    Struct.ObjectId(question_id, "question_id")

    user = g.curr_user

    Question = current_app.mongodb_conn.Question
    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise QuestionNotFound

    return output_question(question)


@output_json
def create_question():
    _type = get_param('type', Struct.Int, True)
    title = get_param('title', Struct.Attr, True)

    check_type(_type)

    user = g.curr_user

    question = current_app.mongodb_conn.Question()
    question["owner_id"] = user["_id"]
    question["type"] = _type
    question["title"] = title
    question.save()

    return output_question(question)


@output_json
def update_question(question_id):
    Struct.ObjectId(question_id, "question_id")

    _type = get_param('type', Struct.Int, True)
    title = get_param('title', Struct.Attr, True)

    check_type(_type)

    user = g.curr_user

    Question = current_app.mongodb_conn.Question
    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise QuestionNotFound

    question["type"] = _type
    question["title"] = title
    question.save()

    return output_question(question)


@output_json
def delete_question(question_id):
    Struct.ObjectId(question_id, "question_id")

    user = g.curr_user

    Question = current_app.mongodb_conn.Question
    Resource = current_app.mongodb_conn.Resource

    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise QuestionNotFound

    question.delete()
    Resource.delete_all_by_qid(question_id)

    return output_question(question)
