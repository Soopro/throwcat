#coding=utf-8
from __future__ import absolute_import
from flask import Blueprint, request

from apiresps import APIError

from utils.helpers import route_inject
from utils.api_utils import make_json_response

from ..helpers import verify_access

from .routes import urlpatterns


bp_name = "user"

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

# endpoint types
open_api_endpoints = [
    "{}.register".format(bp_name),
    "{}.recovery".format(bp_name),
    "{}.get_register_captcha".format(bp_name),
    "{}.get_recovery_captcha".format(bp_name),
    "{}.login".format(bp_name),
]

user_api_endpoints = [
    "{}.get_user_info".format(bp_name),
    "{}.get_profile".format(bp_name),
    "{}.reset_profile".format(bp_name),
    "{}.change_password".format(bp_name),
]


@blueprint.before_request
def before():
    verify_access(open_apis=open_api_endpoints,
                  user_apis=user_api_endpoints)


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
