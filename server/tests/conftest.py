import pytest
import os
import sys
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir + '/../')
from blueprints.user.helpers import *
from utils.auth import generate_hashed_password


from application import create_app


@pytest.fixture(scope='session')
def app():
    test_app = create_app("testcase")
    return test_app


@pytest.fixture(scope='function')
def client(app):
    test_client = app.test_client()
    app.mongodb_conn.drop_database(app.config.get("MONGODB_DATABASE"))
    return test_client


@pytest.fixture(scope='function')
def user(app):
    user = app.mongodb.User()
    user["slug"] = u"test_slug"
    user["login"] = u"tester@labmice.com"
    user["display_name"] = u"olalala"
    user["password_hash"] = generate_hashed_password(u"xxxx")
    user["email"] = u"tester@labmice.com"
    user["app_key"] = generate_key(u"test_slug")
    user["app_secret"] = generate_secret()
    user.save()
    return user


@pytest.fixture(scope='function')
def token_header(app, user):
    with app.app_context():
        token = generate_user_token(user)
    return {"Authorization": "Bearer {}".format(token)}
