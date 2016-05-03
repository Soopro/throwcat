# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (MethodNotAllowed,
                             NotFound,
                             ConflictError,
                             ValidationError,
                             InternalServerError)


class MediaTypeNotAllowed(MethodNotAllowed):
    response_code = 301001
    status_message = "MEDIA_TYPE_NOT_ALLOWED"


class MediaNotFound(NotFound):
    response_code = 301002
    status_message = "MEDIA_NOT_FOUND"


class MediaExists(ConflictError):
    response_code = 301003
    status_message = "MEDIA_PATH_CONFLICT"


class MediaAuthorizeFailed(ValidationError):
    response_code = 301004
    status_message = "MEDIA_AUTHORIZE_FAILED"


class MediaUploadFailed(InternalServerError):
    response_code = 301005
    status_message = "MEDIA_UPLOAD_FAILED"


class MediaDeleteFailed(InternalServerError):
    response_code = 301006
    status_message = "MEDIA_DELETE_FAILED"


class MediaInvalidKey(ValidationError):
    response_code = 301007
    status_message = "MEDIA_INVALID_KEY"
