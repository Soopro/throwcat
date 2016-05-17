# coding=utf-8
from __future__ import absolute_import

from flask import Blueprint
from apiresps import APIError
from utils.misc import route_inject
from utils.api_utils import make_json_response

from ..helpers import verify_access
from .routes import urlpatterns


bp_name = "user"

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

# endpoint types
admin_api_endpoints = [
    "{}.get_questions".format(bp_name),
    "{}.get_question".format(bp_name),
    "{}.create_question".format(bp_name),
    "{}.update_question".format(bp_name),
    "{}.delete_question".format(bp_name),
]


@blueprint.before_request
def before():
    verify_access(user_apis=admin_api_endpoints)


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
