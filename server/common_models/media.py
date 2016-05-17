# coding=utf-8
from __future__ import absolute_import
from utils.models import BaseDocument
from utils.misc import now
from mongokit import ObjectId, INDEX_DESCENDING


class Media(BaseDocument):

    structure = {
        "owner_id": ObjectId,
        "scope": unicode,
        "key": unicode,
        "filename": unicode,
        "type": unicode,
        "mimetype": unicode,
        "ext": unicode,
        "recipe": dict,
        "creation": int,
        "updated": int,
        "uploaded": int,
    }

    required_fields = [
        "owner_id",
        "scope",
        "key",
        "filename",
        "type",
        "mimetype",
        "ext"
    ]

    default_values = {
        "recipe": {},
        "creation": now,
        "updated": now,
        "uploaded": now,
    }

    indexes = [
        {
            'fields': ['owner_id']
        },
        {
            'fields': ['owner_id', 'scope']
        },
        {
            'fields': ['scope', 'key'],
            'unique': True,
        },
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            "_id": ObjectId(_id)
        })

    def find_one_by_scope_key(self, scope, key):
        return self.find_one({
            "scope": scope,
            "key": key
        })

    def find_one_by_oid_key(self, owner_id, key):
        return self.find_one({
            "owner_id": ObjectId(owner_id),
            "key": key
        })

    def find_by_oid_scope_type(self, owner_id, scope, _type):
        return self.find({
            "owner_id": ObjectId(owner_id),
            "scope": scope,
            "type": _type
        }).sort("updated", INDEX_DESCENDING)

    def find_by_oid_scope(self, owner_id, scope):
        return self.find({
            "owner_id": ObjectId(owner_id),
            "scope": scope,
        }).sort("updated", INDEX_DESCENDING)

    def find_by_oid(self, owner_id):
        return self.find({
            "owner_id": ObjectId(owner_id),
        }).sort("updated", INDEX_DESCENDING)
