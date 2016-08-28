import json

_default_headers = {
    "Content-Type": "application/json",
}


def test_register(client):

    assert False


def test_register_captcha(client):

    assert False


def test_create_question(client):

    assert False


def test_recovery(client):

    assert False


def test_get_recovery_captcha(client):

    assert False


def test_login(client):

    assert False


def test_get_profile(client):

    assert False


def test_change_password(client):
    data = {
        "passwd": "passwd",
        "new_passwd": "new_passwd"
    }
    change_passwd_api = "/user/security/password"
    response = client.put(change_passwd_api,
                          headers=_default_headers,
                          data=json.dumps(data))
    content = json.loads(response.data)
    print content

    assert response.status_code == 200


def test_get_secret(client):

    assert False


def test_reset_secret(client):
    assert False

