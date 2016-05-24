#coding=utf-8
from __future__ import absolute_import

import unittest
import shutil
import os

from flask import current_app, json

from application import create_app

from utils.auth import generate_sid

from utils.misc import now


# basic
class BasicTester(unittest.TestCase):
    def setUp(self):
        config_name = "testcase"
        os.environ["SUPMICE_CONFIG_NAME"] = config_name
        self.app = create_app(config_name)
        # print self.app.config.get("APPS_FOLDER")
        # if os.path.isdir(self.app.config.get("APPS_FOLDER")):
        #     print "set up delete"
        #     shutil.rmtree(self.app.config.get("APPS_FOLDER"))

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.mongodb_database.drop_database(
            self.app.config.get('MONGODB_DATABASE') or 'test')
        self.test_file_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "testfiles")

    def tearDown(self):
        self.app.mongodb_database.drop_database(
            self.app.config.get('MONGODB_DATABASE') or 'test')

        # if os.path.isdir(self.app.config.get("APPS_FOLDER")):
        #     shutil.rmtree(self.app.config.get("APPS_FOLDER"))

        self.app_context.pop()

    def assert_all_in(self, *keys, **kargs):
        container = kargs.get('container')
        for key in keys:
            self.assertIn(key, container)


# no user, no app
class APIBaseTester(BasicTester):
    def setUp(self):
        super(APIBaseTester, self).setUp()
        self.client = self.app.test_client()

        now_time = now()
        self.default_user = {
            "email": "test{}@throwcat.com".format(now_time),
            "slug": "test{}".format(now_time),
            "passwd": "passwd_for_test"
        }

        self.user = {
            "email": "test@throwcat.com",
            "slug": "test",
            "passwd": "passwd_for_test"
        }

        self.register(self.user)

    @staticmethod
    def parse_response(resp):
        return json.loads(resp)

    def parse_content(self, data):
        decoded = self.parse_response(data)
        return decoded

    def parse_err_code(self, data):
        decoded = self.parse_response(data)
        return decoded["errcode"]

    @property
    def default_header(self):
        return [('Content-Type', 'application/json')]

    @property
    def headers(self):
        default_headers = self.default_header
        default_headers.append(("Authorization",
                                "Bearer {}".format(self.user["token"])))
        return default_headers

    def register(self, user):
        headers = self.default_header

        # get register captcha
        data = {
            "login": user["email"]
        }
        captcha_api = "/user/register/captcha"
        response = self.client.post(captcha_api,
                                    headers=headers,
                                    data=json.dumps(data))
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

        captcha = content["checked"]

        # user reguster
        data = {
            "slug": user["slug"],
            "captcha": captcha,
            "login": user["email"],
            "passwd": user["passwd"]
        }
        register_api = "/user/register"
        response = self.client.post(register_api,
                                    headers=headers,
                                    data=json.dumps(data))
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

    def login(self, user):
        headers = self.default_header

        data = {
            "login": user["email"],
            "passwd": user["passwd"]
        }
        login_api = "/user/login"
        response = self.client.post(login_api,
                                    headers=headers,
                                    data=json.dumps(data))
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

        self.user["token"] = content["token"]


# default user
class APITester(APIBaseTester):
    def setUp(self):
        super(APITester, self).setUp()
        self.login(self.user)
        self.get_secret()

    def get_secret(self):
        headers = self.headers
        secret_api = "/user/security/secret"
        response = self.client.get(secret_api, headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

        self.user["app_key"] = content["app_key"]
        self.user["app_secret"] = content["app_secret"]


# default question
class QuestionTester(APITester):
    def setUp(self):
        super(QuestionTester, self).setUp()
        self.question_api = "/question/{}"

        self.question = self.generate_question()
        self.create_question(self.question)

    def generate_question(self):
        return list(self.generate_questions(1))[0]

    def generate_questions(self, count):
        for i in range(count):
            yield {
                "type": 1,
                "title": "title_{}".format(i),
                "resources": [{
                    "src": "http://src.com/{}".format(i),
                    "tip": "tip_{}".format(i),
                    "answer": "answer_{}".format(i),
                    "recipe": {
                        "asoect_ratio": 1,
                        "height": 1000,
                        "width": 1000,
                        "modified": True,
                        "crop": {
                            "h": 0.5,
                            "w": 0.5,
                            "x": 0.25,
                            "y": 0.25
                        }
                    }
                }]
            }

    def create_question(self, question):
        headers = self.headers
        data = {
            "type": question["type"],
            "title": question["title"],
            "resources": question["resources"]
        }
        create_question_api = self.question_api.format("")
        response = self.client.post(create_question_api,
                                    headers=headers,
                                    data=json.dumps(data))
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

        question["id"] = content["id"]
