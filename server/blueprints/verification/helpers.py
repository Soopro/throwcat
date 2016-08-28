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
    for i in xrange(data['point']):
        if resource['recipe']['ratio'][i] < data['point'][i]:
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
        "token": serializer.dumps({"user_id": user['_id'],
                                   "question_id": question['_id'],
                                   "resource_id": resource['_id']})
    }


def check_answer(user, data, answer, app_key):
    Resource = current_app.mongodb.Resource
    resource = Resource.find_one_by_id_qid_oid(data['resource_id'],
                                               data['question_id'],
                                               data['owner_id'])
    verified = False
    signature = None
    if resource['type'] == Resource.TYPE_PHOTO:
        verified = _verify_photo(resource, answer)
    elif resource['type'] == Resource.TYPE_READING:
        verified = _verify_reading(resource, answer)

    if verified:
        serializer = _get_signature_serializer()
        signature = serializer.dumps({'user_id': user['_id'],
                                      'owner_id': data['owner_id'],
                                      'question_id': data['question_id'],
                                      'resource_id': resource['_id'],
                                      'app_key': app_key})
    return False, signature


def decode_signature(signature):
    serializer = _get_signature_serializer()
    try:
        data = serializer.loads(signature)
    except (BadSignature, SignatureExpired):
        return False, None
    return True, data
