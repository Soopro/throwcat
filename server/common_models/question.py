# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.misc import now
from mongokit import ObjectId


class Question(BaseDocument):
    structure = {
        'owner_id': ObjectId,
        'title': unicode,
        'type': int,
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

    def find_all_by_oid(self, owner_id):
        return self.find({
            "owner_id": ObjectId(owner_id)
        })

    def find_all_by_oid_and_type(self, owner_id, _type):
        return self.find({
            "owner_id": ObjectId(owner_id),
            "type": _type
        })

    def find_one_by_id_and_oid(self, _id, owner_id):
        return self.find_one({
            "_id": ObjectId(_id),
            "owner_id": ObjectId(owner_id)
        })
