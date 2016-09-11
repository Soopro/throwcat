import json
from blueprints.user.helpers import *
from utils.auth import generate_hashed_password


_default_headers = {
    "Content-Type": "application/json",
}


def test_get_question(app, client):
    user = app.mongodb.User()
    user["slug"] = u"test_slug"
    user["login"] = u"tester@labmice.com"
    user["display_name"] = u"olalala"
    user["password_hash"] = generate_hashed_password(u"xxxx")
    user["email"] = u"tester@labmice.com"
    user["app_key"] = generate_key(u"test_slug")
    user["app_secret"] = generate_secret()
    user.save()

    question = app.mongodb.Question()
    question["slug"] = u"test_question"
    question["owner_id"] = user["_id"]
    question["type"] = 1
    question["title"] = u"my_title"
    question.save()

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    # resource["src"] = ""
    resource["hint"] = u"6*9=?"
    resource["answer"] = u"42"
    # resource["recipe"] = {}
    resource.save()

    resp = client.get('/verification/user/test_slug/question/test_question')
    print resp.data
    assert resp.status_code == 200
    assert b"token" in resp.data
    assert b"question" in resp.data


def test_put_answer_reading(app, client):
    user = app.mongodb.User()
    user["slug"] = u"test_slug"
    user["login"] = u"tester@labmice.com"
    user["display_name"] = u"olalala"
    user["password_hash"] = generate_hashed_password(u"xxxx")
    user["email"] = u"tester@labmice.com"
    user["app_key"] = generate_key(u"test_slug")
    user["app_secret"] = generate_secret()
    user.save()

    question = app.mongodb.Question()
    question["slug"] = u"test_question"
    question["owner_id"] = user["_id"]
    question["type"] = 1
    question["title"] = u"my_title"
    question.save()

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    # resource["src"] = ""
    resource["hint"] = u"6*9=?"  # math teacher died young
    resource["answer"] = u"42"
    # resource["recipe"] = {}
    resource.save()

    resp = client.get('/verification/user/test_slug/question/test_question')
    token = json.loads(resp.data)["token"]

    data = {
        "answer": {"answer": "42"},
        "token": token,
    }
    resp = client.post('/verification/answer', data=json.dumps(data),
                       query_string={"app_key": user["app_key"]},
                       headers=_default_headers)
    print resp.data
    assert resp.status_code == 200
    assert b"true" in resp.data


def test_put_answer_photo(app, client):
    user = app.mongodb.User()
    user["slug"] = u"test_slug"
    user["login"] = u"tester@labmice.com"
    user["display_name"] = u"olalala"
    user["password_hash"] = generate_hashed_password(u"xxxx")
    user["email"] = u"tester@labmice.com"
    user["app_key"] = generate_key(u"test_slug")
    user["app_secret"] = generate_secret()
    user.save()

    question = app.mongodb.Question()
    question["slug"] = u"test_question"
    question["owner_id"] = user["_id"]
    question["type"] = 0
    question["title"] = u"my_title"
    question.save()

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    resource["src"] = u"http://www.example.com/cat.png"
    resource["hint"] = u"click the cat"
    resource["recipe"] = {'ratio': [0.3, 0.3, 0.3, 0.3]}
    resource.save()

    resp = client.get('/verification/user/test_slug/question/test_question')
    token = json.loads(resp.data)["token"]

    data = {
        "answer": {"point": [0.4, 0.4, 0.6, 0.6]},
        "token": token,
    }
    resp = client.post('/verification/answer', data=json.dumps(data),
                       query_string={"app_key": user["app_key"]},
                       headers=_default_headers)
    print resp.data
    assert resp.status_code == 200
    assert b"true" in resp.data


def test_confirm(app, client):
    user = app.mongodb.User()
    user["slug"] = u"test_slug"
    user["login"] = u"tester@labmice.com"
    user["display_name"] = u"olalala"
    user["password_hash"] = generate_hashed_password(u"xxxx")
    user["email"] = u"tester@labmice.com"
    user["app_key"] = generate_key(u"test_slug")
    user["app_secret"] = generate_secret()
    user.save()

    question = app.mongodb.Question()
    question["slug"] = u"test_question"
    question["owner_id"] = user["_id"]
    question["type"] = 1
    question["title"] = u"my_title"
    question.save()

    resource = app.mongodb.Resource()
    resource["owner_id"] = user["_id"]
    resource["question_id"] = question["_id"]
    # resource["src"] = ""
    resource["hint"] = u"6*9=?"  # math teacher died young
    resource["answer"] = u"42"
    # resource["recipe"] = {}
    resource.save()

    resp = client.get('/verification/user/test_slug/question/test_question')
    token = json.loads(resp.data)["token"]

    data = {
        "answer": {"answer": "42"},
        "token": token,
    }
    resp = client.post('/verification/answer', data=json.dumps(data),
                       query_string={"app_key": user["app_key"]},
                       headers=_default_headers)
    print resp.data
    assert resp.status_code == 200
    assert b"true" in resp.data

    signature = json.loads(resp.data)['signature']
    data = {
        "signature": signature,
        "app_secret": user["app_secret"]

    }
    resp = client.post('/verification/confirm', data=json.dumps(data),
                       headers=_default_headers)

    print resp.data
    assert resp.status_code == 200
    assert b"true" in resp.data
