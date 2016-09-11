# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.request import get_param
from apiresps.validations import Struct
from flask import current_app, g

from blueprints.question.helpers import *


@output_json
def get_resources(question_id):
    Struct.ObjectId(question_id, "question_id")

    user = g.curr_user

    Resource = current_app.mongodb.Resource
    resources = Resource.find_all_by_qid_oid(question_id, user["_id"])
    return [output_resource(resource) for resource in resources]


@output_json
def get_resource(question_id, resource_id):
    Struct.ObjectId(question_id, "question_id")
    Struct.ObjectId(resource_id, "resource_id")

    user = g.curr_user

    Resource = current_app.mongodb.Resource
    resource = Resource.find_one_by_id_qid_oid(resource_id, question_id, user["_id"])
    if not resource:
        raise ResourceNotFound

    return output_resource(resource)


@output_json
def create_resource(question_id):
    Struct.ObjectId(question_id, "question_id")

    user = g.curr_user

    Question = current_app.mongodb.Question
    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise QuestionNotFound

    src = get_param('src', Struct.Url)
    hint = get_param('hint', Struct.Attr, required=True)
    answer = get_param('answer', Struct.Attr)
    recipe = get_param('recipe', Struct.Dict)

    user = g.curr_user

    resource = current_app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    resource["src"] = src
    resource["hint"] = hint
    resource["answer"] = answer
    resource["recipe"] = recipe

    resource.save()

    return output_resource(resource)


@output_json
def update_resource(question_id, resource_id):
    Struct.ObjectId(question_id, "question_id")
    Struct.ObjectId(resource_id, "resource_id")

    src = get_param('src', Struct.Url)
    hint = get_param('hint', Struct.Attr, required=True)
    answer = get_param('answer', Struct.Attr)
    recipe = get_param('recipe', Struct.Dict)


    user = g.curr_user

    Question = current_app.mongodb.Question
    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise QuestionNotFound

    Resource = current_app.mongodb.Resource
    resource = Resource.find_one_by_id_qid_oid(resource_id, question["_id"], user["_id"])
    if not resource:
        raise ResourceNotFound

    resource["src"] = src
    resource["hint"] = hint
    resource["answer"] = answer
    resource["recipe"] = recipe
    resource.save()

    return output_resource(resource)


@output_json
def delete_resource(question_id, resource_id):
    Struct.ObjectId(question_id, "question_id")
    Struct.ObjectId(resource_id, "resource_id")

    user = g.curr_user

    Question = current_app.mongodb.Question
    question = Question.find_one_by_id_and_oid(question_id, user["_id"])
    if not question:
        raise QuestionNotFound

    Resource = current_app.mongodb.Resource
    resource = Resource.find_one_by_id_qid_oid(resource_id, question_id, user["_id"])
    if not resource:
        raise ResourceNotFound

    resource.delete()

    return output_resource(resource)
