#coding=utf-8
from __future__ import absolute_import

from .base import QuestionTester
from flask import json


class QuestionAPITestCases(QuestionTester):
    def test_create_question(self):
        question = self.generate_question()
        self.create_question(question)

    def test_get_questions(self):
        headers = self.headers
        get_questions_api = self.question_api.format("")
        response = self.client.get(get_questions_api,
                                   headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

    def test_get_question(self):
        headers = self.headers
        get_question_api = self.question_api.format(self.question["id"])
        response = self.client.get(get_question_api,
                                   headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

    def test_update_question(self):
        headers = self.headers
        data = self.question
        update_question_api = self.question_api.format(self.question["id"])
        response = self.client.put(update_question_api,
                                   data=json.dumps(data),
                                   headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)

    def test_delete_question(self):
        headers = self.headers
        data = self.question
        delete_question_api = self.question_api.format(self.question["id"])
        response = self.client.delete(delete_question_api,
                                      data=json.dumps(data),
                                      headers=headers)
        content = self.parse_content(response.data)

        print content

        self.assertEqual(response.status_code, 200)
