#coding=utf-8
from __future__ import absolute_import
from flask import Blueprint, request

from apiresps import APIError

from utils.misc import route_inject
from utils.api_utils import make_json_response

from ..helpers import verify_access

from .routes import urlpatterns


bp_name = "verification"

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

# endpoint types
open_api_endpoints = [
    "{}.get_question".format(bp_name),
    "{}.put_answer".format(bp_name),
    "{}.confirm".format(bp_name),
]


@blueprint.before_request
def before():
    verify_access(open_apis=open_api_endpoints)


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
