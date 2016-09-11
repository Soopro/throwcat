import json


_default_headers = {
    "Content-Type": "application/json",
}



def test_get_question(app, client, user):
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

    resp = client.get('/verification/user/{}/question/test_question'.format(user['slug']))
    print resp.data
    assert resp.status_code == 200
    assert b"token" in resp.data
    assert b"question" in resp.data


def test_put_answer_reading(app, client, user):
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

    resp = client.get('/verification/user/{}/question/test_question'.format(user['slug']))
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


def test_put_answer_photo(app, client, user):
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

    resp = client.get('/verification/user/{}/question/test_question'.format(user['slug']))
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


def test_confirm(app, client, user):
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

    resp = client.get('/verification/user/{}/question/test_question'.format(user['slug']))
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
