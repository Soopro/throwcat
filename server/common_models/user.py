# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.helpers import now
from mongokit import ObjectId


class User(BaseDocument):
    structure = {
        'login': unicode,
        'password_hash': unicode,
        'name': unicode,
        'creation': int,
        'updated': int,
        'deleted': bool
    }

    required_fields = [
        'login',
        'password_hash',
        'name'
    ]

    default_values = {
        'creation': now,
        'updated': now,
        'deleted': False
    }

    def find_all(self):
        return self.find({
            "deleted": False
        })

    def find_all_deleted(self):
        return self.find({
            "deleted": True
        })

    def find_one_by_id(self, user_id):
        return self.find_one({
            "_id": ObjectId(user_id),
            "deleted": False
        })

    def find_one_by_login(self, login):
        return self.find_one({
            "login": login,
            "deleted": False
        })

    def find_all_by_name(self, name):
        return self.find({
            "name": name,
            "deleted": False
        })


class Profile(BaseDocument):
    structure = {
        'user_id': ObjectId,
        'key': unicode,
        'secret': unicode,
        'creation': int,
        'updated': int,
        'deleted': bool
    }

    required_fields = [
        'user_id',
        'key',
        'secret'
    ]

    default_values = {
        'creation': now,
        'updated': now,
        'deleted': False
    }

    def find_all(self):
        return self.find({
            "deleted": False
        })

    def find_all_deleted(self):
        return self.find({
            "deleted": True
        })

    def find_one_by_user_id(self, user_id):
        return self.find_one({
            'user_id': ObjectId(user_id),
            "deleted": False
        })

    def find_one_by_key_and_secret(self, key, secret):
        return self.find_one({
            'key': key,
            'secret': secret,
            "deleted": False
        })