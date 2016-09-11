# coding=utf-8
from __future__ import absolute_import

import random
from flask import current_app, g
from itsdangerous import (TimedJSONWebSignatureSerializer,
                          BadSignature, SignatureExpired)
from .errors import *


def _get_signature_serializer():
    serializer = TimedJSONWebSignatureSerializer(
        secret_key=current_app.config.get("SECRET_KEY"),
        expires_in=24 * 60
    )
    return serializer


def _verify_photo(resource, data):
    for i in xrange(len(data['point'])):
        if data['point'][i] < resource['recipe']['ratio'][i]:
            return False
    return True


def _verify_reading(resource, data):
    if resource['answer'] == data['answer'].strip():
        return True
    return False


def output_question(user, question):
    Resource = current_app.mongodb.Resource
    resource = Resource.random_one_by_qid(question['_id'])
    serializer = _get_signature_serializer()

    return {
        "question": {
            "title": question["title"],
            "type": question["type"],
            "hint": resource["hint"],
        },
        "token": serializer.dumps({"owner_id": str(user['_id']),
                                   "question_id": str(question['_id']),
                                   "resource_id": str(resource['_id'])})
    }


def check_answer(question, user, signature_payload, answer, app_key):
    Question = current_app.mongodb.Question
    Resource = current_app.mongodb.Resource
    resource = Resource.find_one_by_id_qid_oid(signature_payload['resource_id'],
                                               signature_payload['question_id'],
                                               user['_id'])
    verified = False
    signature = None

    if question['type'] == Question.TYPE_PHOTO:
        verified = _verify_photo(resource, answer)
    elif question['type'] == Question.TYPE_READING:
        verified = _verify_reading(resource, answer)

    if verified:
        serializer = _get_signature_serializer()
        signature = serializer.dumps({'owner_id': str(signature_payload['owner_id']),
                                      'question_id': str(signature_payload['question_id']),
                                      'resource_id': str(resource['_id']),
                                      'app_key': app_key})
    return verified, signature


def decode_signature(signature):
    serializer = _get_signature_serializer()
    try:
        data = serializer.loads(signature)
    except (BadSignature, SignatureExpired):
        return False, None
    return True, data
