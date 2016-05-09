# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.helpers import now
from mongokit import ObjectId


class User(BaseDocument):
    structure = {
        'login': unicode,
        'slug': unicode,
        'password_hash': unicode,
        'display_name': unicode,
        'email': unicode,
        'app_key': unicode,
        'app_secret': unicode,
        'creation': int,
        'updated': int,
        'deleted': bool
    }

    required_fields = [
        'login',
        'slug',
        'password_hash',
        'display_name',
        'email',
        'app_key',
        'app_secret',
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

    def find_one_by_slug(self, slug):
        return self.find_one({
            "slug": slug,
            "deleted": False
        })

    def find_one_by_key(self, app_key):
        return self.find_one({
            'app_key': app_key,
            "deleted": False
        })

    def find_all_by_display_name(self, display_name):
        return self.find({
            "display_name": display_name,
            "deleted": False
        })

    def find_one_by_key_and_secret(self, app_key, app_secret):
        return self.find_one({
            'app_key': app_key,
            'app_secret': app_secret,
            "deleted": False
        })
