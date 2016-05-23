#coding=utf-8
from __future__ import absolute_import

from .base import QuestionTester
from flask import json


class VerifyAPITestCases(QuestionTester):
    def get_question(self):
        headers = self.default_header
        data = {
            "app_key": self.user["app_key"],
            "question_id": self.question["id"]
        }
        get_question_api = "/verification/question"
        response = self.client.post(get_question_api,
                                    data=json.dumps(data),
                                    headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

        self.ssid = content["ssid"]

    def put_answer(self):
        headers = self.default_header
        data = {
            "point": {
                "x": 0.5,
                "y": 0.5
            },
            "ssid": self.ssid
        }
        put_question_api = "/verification/answer"
        response = self.client.post(put_question_api,
                                    data=json.dumps(data),
                                    headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

        self.assertEqual(content["result"], "succeed")

    def confirm(self):
        headers = self.default_header
        data = {
            "ssid": self.ssid,
            "app_secret": self.user["app_secret"]
        }
        comfirmation_api = "/verification/comfirmation"
        response = self.client.post(comfirmation_api,
                                    data=json.dumps(data),
                                    headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

    def test_verification(self):
        self.get_question()
        self.put_answer()
        self.confirm()
