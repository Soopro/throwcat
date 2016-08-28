# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (PermissionDenied,
                             ConflictError)


class AppNotFoundError(ConflictError):
    response_code = 306001
    status_message = "APP_NOT_FOUND"


class QuestionIdError(ConflictError):
    response_code = 306002
    status_message = "QUESTION_ID_ERROR"


class CheckError(ConflictError):
    response_code = 306003
    status_message = "CHECK_ERROR"


class ComfirmdError(PermissionDenied):
    response_code = 306101
    status_message = "COMFIRM_ERROR"
