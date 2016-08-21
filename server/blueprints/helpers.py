# coding=utf-8
from __future__ import absolute_import

from flask import g, request

from apiresps.errors import AuthFailed

from utils.auth import get_current_user


def verify_jwt():
    try:
        current_user = get_current_user()
        if current_user is None:
            raise Exception
    except Exception:
        raise AuthFailed('not found')

    g.curr_user = current_user


def verify_access(user_apis=None, open_apis=None):
    if user_apis is None:
        user_apis = []
    if open_apis is None:
        open_apis = []
    if request.endpoint in open_apis:
        pass
    else:
        verify_jwt()
