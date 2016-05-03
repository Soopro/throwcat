# coding=utf-8
from flask import Blueprint

from apiresps import APIError

from utils.api_utils import make_json_response
from utils.helpers import route_inject

from ..helpers import verify_access

from .routes import urls

bp_name = "media"

blueprint = Blueprint("media", __name__)

route_inject(blueprint, urls)

# endpoint types
admin_api_endpoints = [
    "{}.list_media".format(bp_name),
    "{}.save_media".format(bp_name),
    "{}.get_media".format(bp_name),
    "{}.update_media".format(bp_name),
    "{}.delete_media".format(bp_name),
    "{}.upload_authorize".format(bp_name)
]


@blueprint.before_request
def media_module_before_request():
    verify_access(user_apis=admin_api_endpoints)


@blueprint.errorhandler(APIError)
def blueprint_api_err(error):
    return make_json_response(error)