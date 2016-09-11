import json
from blueprints.user.helpers import *
from utils.auth import generate_hashed_password
import pytest

_default_headers = {
    "Content-Type": "application/json",
}


@pytest.fixture(scope='function')
def question(app, user):
    question = app.mongodb.Question()
    question["slug"] = u"test_question"
    question["owner_id"] = user["_id"]
    question["type"] = 1
    question["title"] = u"my_title"
    question.save()
    return question


def test_get_questions(client, question, token_header):
    resp = client.get("/question/", headers=token_header)
    print resp.data
    assert resp.status_code == 200
    assert b"my_title" in resp.data


def test_get_question(client, question, token_header):

    resp = client.get("/question/{}".format(question["_id"]),
                       headers=token_header)
    print resp.data
    assert resp.status_code == 200
    assert b"my_title" in resp.data


def test_create_question(app, client, user, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})
    data = {
        "type": 0,
        "title": "my_title",
        "slug": "my_slug"
    }
    resp = client.post("/question/", data=json.dumps(data),
                       headers=headers)
    print resp.data
    assert resp.status_code == 200
    q = app.mongodb.Question.find_one_by_slug_and_oid("my_slug", user["_id"])
    assert q is not None
    assert q["title"] == "my_title"


def test_update_question(client, question, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})

    data = {
        "type": 1,
        "title": "lalala"
    }
    resp = client.put("/question/{}".format(question["_id"]),
                       data=json.dumps(data),
                       headers=headers)
    print resp.data
    assert resp.status_code == 200
    assert b"lalala" in resp.data


def test_delete_question(app, client, user, question, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})
    resp = client.delete("/question/{}".format(question["_id"]),
                         headers=headers)
    print resp.data
    assert resp.status_code == 200
    q = app.mongodb.Question.find_one_by_slug_and_oid("my_slug", user["_id"])
    assert q is None


def test_get_resources(app, client, user, question, token_header):
    headers = token_header

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    resource["hint"] = u"6*9=?"  # math teacher died young
    resource["answer"] = u"42"
    resource.save()

    resp = client.get("/question/{}/resource".format(question["_id"]), headers=headers)
    print resp.data
    assert resp.status_code == 200
    assert str(question["_id"]) in resp.data


def test_get_resource(app, client, user, question, token_header):
    headers = token_header

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    resource["hint"] = u"6*9=?"  # math teacher died young
    resource["answer"] = u"42"
    resource.save()

    resp = client.get("/question/{}/resource/{}".format(question["_id"],
                                                        resource["_id"]), headers=headers)
    print resp.data
    assert resp.status_code == 200
    assert str(question["_id"]) in resp.data


def test_create_resource(app, client, user, question, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})
    data = {
        "src": "http://example.com/cat.png",
        "hint": "6*9?",
        "answer": "54",
    }
    resp = client.post("/question/{}/resource/".format(question["_id"]), data=json.dumps(data),
                       headers=headers)
    print resp.data
    assert resp.status_code == 200
    resource_id = json.loads(resp.data)["id"]
    resource = app.mongodb.Resource.find_one_by_id_qid_oid(resource_id, question["_id"], user["_id"])
    assert resource is not None


def test_update_resource(app, client, user, question, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    resource["hint"] = u"6*9=?"  # math teacher died young
    resource["answer"] = u"42"
    resource.save()

    data = {
        "hint": "ABC",
        "answer": "DEF"
    }

    resp = client.put("/question/{}/resource/{}".format(question["_id"],
                                                        resource["_id"]),
                      data=json.dumps(data),
                      headers=headers)
    print resp.data
    assert resp.status_code == 200


def test_delete_resource(app, client, user, question, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    resource["hint"] = u"6*9=?"  # math teacher died young
    resource["answer"] = u"42"
    resource.save()

    resp = client.delete("/question/{}/resource/{}".format(question["_id"],
                                                         resource["_id"]),
                       headers=headers)
    print resp.data
    assert resp.status_code == 200
    resource = app.mongodb.Resource.find_one_by_id_qid_oid(resource["_id"], question["_id"], user["_id"])
    assert resource is None

