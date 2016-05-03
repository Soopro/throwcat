# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (ValidationError,
                             PermissionDenied,
                             InternalServerError,
                             MethodNotAllowed,
                             BadRequest,
                             NotFound,
                             ConflictError)


class ResetPwdKeyRequired(BadRequest):
    response_code = 305001
    status_message = "RESET_PWD_KEY_REQUIRED"


class ResetPwdKeyInvalid(ValidationError):
    response_code = 305002
    status_message = "RESET_PWD_KEY_INVALID"


class ResetPwdKeyExpired(BadRequest):
    response_code = 305003
    status_message = "RESET_PWD_KEY_EXPIRED"


class PlanInvalid(ValidationError):
    response_code = 305004
    status_message = "PLAN_INVALID"

    
class InviteCodeDuplicate(ConflictError):
    response_code = 305005
    status_message = "INVITE_CODE_DUPLICATE"

    
class UserLoginOccupied(ConflictError):
    status_message = "USER_LOG_TAKEN"
    response_code = 305006


class UserAliasOccupied(ConflictError):
    status_message = "USER_NAME_TAKEN"
    response_code = 305007


class TooManyInviteCodes(InternalServerError):
    response_code = 305008
    status_message = "TOO_MANY_INVITE_CODES"


class InviteCodeNotExists(NotFound):
    response_code = 305009
    status_message = "INVITE_CODE_NOT_EXISTS"


class InviteCodeUsed(ConflictError):
    response_code = 305010
    status_message = "INVITE_CODE_USED"

    
class UserWrongPassword(BadRequest):
    response_code = 305012
    status_message = "WRONG_PASSWORD"


class UserActivateAlreadyDone(ConflictError):
    response_code = 305013
    status_message = 'USER_ALREADY_ACTIVATED'


class UserPublicRegisterNotAllowed(MethodNotAllowed):
    response_code = 305014
    status_message = "PUBLIC_REGISTER_NOT_ALLOWED"


class UserPasswordMismatch(ValidationError):
    response_code = 305015
    status_message = 'USER_PWD_CONFIRM_NOT_MATCH'