import pytest
import os
import sys
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir + '/../')

from application import create_app


@pytest.fixture(scope='session')
def app():
    test_app = create_app("testing")
    return test_app


@pytest.fixture(scope='function')
def client(app):
    test_client = app.test_client()
    return test_client

