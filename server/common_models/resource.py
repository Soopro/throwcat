# coding=utf-8
from __future__ import absolute_import
from utils.models import BaseDocument
from utils.misc import now
from mongokit import ObjectId
from random import randint


class Resource(BaseDocument):
    structure = {
        'owner_id': ObjectId,
        'question_id': ObjectId,
        'src': unicode,
        "hint": unicode,
        "answer": unicode,
        "recipe": dict,
        'creation': int,
        'updated': int
    }

    required_fields = [
        'owner_id',
        'question_id',
        "hint",
    ]

    default_values = {
        'creation': now,
        'updated': now,
    }

    def find_all_by_qid_oid(self, question_id, owner_id):
        return self.find({
            "question_id": ObjectId(question_id),
            "owner_id": ObjectId(owner_id),
        })

    def find_one_by_id_qid_oid(self, _id, question_id, owner_id):
        return self.find_one({
            "_id": ObjectId(_id),
            "owner_id": ObjectId(owner_id),
            "question_id": ObjectId(question_id),
        })

    def random_one_by_qid(self, question_id):
        count = self.find({
            "question_id": ObjectId(question_id),
        }).count()
        return self.find({
            "question_id": ObjectId(question_id),
        }).limit(-1).skip(randint(0, count-1)).next()

    def delete_all_by_qid(self, question_id):
        return self.collection.remove({
            "question_id": ObjectId(question_id),
        })
