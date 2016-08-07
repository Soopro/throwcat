# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.misc import now
from mongokit import ObjectId


class Resource(BaseDocument):
    structure = {
        'owner_id': ObjectId,
        'question_id': ObjectId,
        'type': int,   # correspond to question type

        'src': unicode,
        "tip": unicode,
        "answer": unicode,
        "recipe": dict,

        'creation': int,
        'updated': int
    }

    required_fields = [
        'owner_id',
        'title',
        'type'
    ]

    default_values = {
        'creation': now,
        'updated': now,
        'type': 0
    }

    def find_all_by_qid_oid(self, question_id, owner_id):
        return self.find({
            "question_id": ObjectId(question_id),
            "owner_id": ObjectId(owner_id),
        })

    def find_all_by_qid_oid_and_type(self, question_id, owner_id, _type):
        return self.find({
            "question_id": ObjectId(question_id),
            "owner_id": ObjectId(owner_id),
            "type": _type,
        })

    def find_one_by_id_qid_oid(self, _id, question_id, owner_id):
        return self.find_one({
            "_id": ObjectId(_id),
            "owner_id": ObjectId(owner_id),
            "question_id": ObjectId(question_id),
        })

    def random_one_by_qid(self, question_id):
        return self.find({
            "owner_id": ObjectId(question_id),
        })  # todo: random

    def delete_all_by_qid(self, question_id):
        return self.find({
            "question_id": ObjectId(question_id),
        }).delete()
