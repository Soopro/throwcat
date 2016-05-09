# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (ValidationError, NotFound)


class ParamError(ValidationError):
    response_code = 305001
    status_message = "PARAM_ERROR"


class QuestionNotFound(NotFound):
    response_code = 305101
    status_message = "QUESTION_NOT_FOUND"
