import json
_default_headers = {
    "Content-Type": "application/json",
}


def test_get_questions(client):
    assert False


def test_get_question(client):
    assert False


def test_create_question(client):
    data = {
        "type": 0,
        "title": "test question",
    }
    response = client.post("/question",
                           headers=_default_headers,
                           data=json.dumps(data))

    assert response.status_code == 200


def test_update_question(client):
    assert False


def test_delete_question(client):
    assert False


def test_get_resources(client):
    assert False


def test_get_resource(client):
    assert False


def test_create_resource(client):
    assert False


def test_update_resource(client):
    assert False


def test_delete_resource(client):
    assert False

