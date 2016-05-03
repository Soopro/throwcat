# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (ConflictError,
                             NotFound,
                             ValidationError)


class UserHasExisted(ConflictError):
    response_code = 300001
    status_message = "USER_HAS_EXISTED"


class UserNotFound(NotFound):
    response_code = 300002
    status_message = "USER_NOT_FOUND"


class ProfileHasExisted(ConflictError):
    response_code = 300101
    status_message = "PROFILE_HAS_EXISTED"


class ProfileNotFound(NotFound):
    response_code = 300102
    status_message = "PROFILE_NOT_FOUND"


class CaptchaError(ValidationError):
    response_code = 300201
    status_message = "CAPTCHA_NOT_MATCH"


class PasswordError(ValidationError):
    response_code = 300301
    status_message = "PASSWORD_NOT_MATCH"


class PasswordMismatchError(ValidationError):
    response_code = 300401
    status_message = 'PASSWORD_CONFIRM_NOT_MATCH'