import json
from utils.auth import generate_hashed_password, check_hashed_password
from blueprints.user.helpers import *
from blueprints.user.helpers import generate_user_token


_default_headers = {
    "Content-Type": "application/json",
}


def test_register(app, client):
    data = {
        "login": u"tester@labmice.com"
    }
    resp = client.post("/user/register/captcha", data=json.dumps(data),
                       headers=_default_headers)
    captcha = json.loads(resp.data)["checked"]

    data = {
        "slug": u"test_slug",
        "captcha": captcha,
        "login": u"tester@labmice.com",
        "passwd": u"password",
    }
    resp = client.post("/user/register", data=json.dumps(data),
                       headers=_default_headers)
    print resp.data
    assert resp.status_code == 200

    user = app.mongodb.User.find_one_by_login(u"tester@labmice.com")
    assert user is not None


def test_recovery(app, client):
    user = app.mongodb.User()
    user["slug"] = u"test_slug"
    user["login"] = u"tester@labmice.com"
    user["display_name"] = u"olalala"
    user["password_hash"] = generate_hashed_password("xxxx")
    user["email"] = u"123@abc.com"
    user["app_key"] = generate_key("test_slug")
    user["app_secret"] = generate_secret()
    user.save()

    data = {
        "login": u"tester@labmice.com"
    }
    resp = client.post("/user/recovery/captcha", data=json.dumps(data),
                       headers=_default_headers)
    captcha = json.loads(resp.data)["recovered"]
    print resp.data
    assert resp.status_code == 200

    data = {
        "captcha": captcha,
        "login": u"tester@labmice.com",
        "passwd": u"new_pass",
    }
    resp = client.post("/user/recovery", data=json.dumps(data),
                       headers=_default_headers)
    print resp.data
    assert resp.status_code == 200

    user = app.mongodb.User.find_one_by_login(u"tester@labmice.com")
    assert user is not None
    assert check_hashed_password(user["password_hash"], u"new_pass")


def test_login(app, client):
    user = app.mongodb.User()
    user["slug"] = u"test_slug"
    user["login"] = u"tester@labmice.com"
    user["display_name"] = u"olalala"
    user["password_hash"] = generate_hashed_password(u"xxxx")
    user["email"] = u"tester@labmice.com"
    user["app_key"] = generate_key(u"test_slug")
    user["app_secret"] = generate_secret()
    user.save()

    data = {
        "login": u"tester@labmice.com",
        "passwd": u"xxxx"
    }

    resp = client.post("/user/login", data=json.dumps(data),
                       headers=_default_headers)
    print resp.data
    assert resp.status_code == 200


def test_get_profile(app, client, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})

    resp = client.get("/user/profile",
                      headers=headers)
    assert resp.status_code == 200
    assert b'display_name' in resp.data


def test_change_password(app, client, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})

    data = {
        "passwd": "xxxx",
        "new_passwd": "new_pass"
    }
    resp = client.put("/user/security/password",
                      headers=headers,
                      data=json.dumps(data))
    print resp.data
    assert resp.status_code == 200
    user = app.mongodb.User.find_one_by_login(u"tester@labmice.com")
    assert user is not None
    assert check_hashed_password(user["password_hash"], u"new_pass")


def test_get_secret(client, token_header):
    headers = token_header

    resp = client.get("/user/security/secret",
                      headers=headers)
    assert resp.status_code == 200
    assert b'app_secret' in resp.data


def test_reset_secret(client, token_header):
    headers = token_header
    headers.update({"Content-Type": "application/json"})
    resp = client.put("/user/security/secret",
                      headers=headers)
    assert resp.status_code == 200
    assert b'app_secret' in resp.data
