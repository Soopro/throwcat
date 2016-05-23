#coding=utf-8
from __future__ import absolute_import

from .base import APIBaseTester
from flask import json


class UserAPITestCases(APIBaseTester):
    def test_register(self):
        self.register(self.default_user)

    def test_login(self):
        self.login(self.user)

    def test_change_passwd(self):
        self.login(self.user)

        passwd = self.user["passwd"]
        new_passwd = "{}_1".format(passwd)

        self.change_passwd(passwd, new_passwd)

        self.change_passwd(new_passwd, passwd)

    def change_passwd(self, passwd, new_passwd):
        headers = self.headers
        data = {
            "passwd": passwd,
            "new_passwd": new_passwd
        }
        change_passwd_api = "/user/security/password"
        response = self.client.put(change_passwd_api,
                                   headers=headers,
                                   data=json.dumps(data))
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

        self.user["token"] = content["token"]
