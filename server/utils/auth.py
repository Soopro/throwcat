# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request
from werkzeug.security import generate_password_hash, check_password_hash

import hashlib
import hmac

from datetime import timedelta
from bson import ObjectId
from itsdangerous import (TimedJSONWebSignatureSerializer,
                          JSONWebSignatureSerializer,
                          SignatureExpired,
                          BadSignature)

from apiresps.errors import AuthFailed


def get_timed_serializer(expires_in=None, salt='supmice'):
    if not isinstance(salt, basestring):
        salt = 'supmice'

    if expires_in is None:
        expires_in = current_app.config.get('JWT_EXPIRATION_DELTA', 0)
    if isinstance(expires_in, timedelta):
        expires_in = int(expires_in.total_seconds())
    expires_in_total = expires_in + current_app.config.get('JWT_LEEWAY', 0)

    return TimedJSONWebSignatureSerializer(
        secret_key=current_app.config.get('JWT_SECRET_KEY'),
        expires_in=expires_in_total,
        salt=salt,
        algorithm_name=current_app.config.get('JWT_ALGORITHM', "HS256")
    )


def get_serializer(salt='supmice'):
    if not isinstance(salt, basestring):
        salt = 'supmice'

    return JSONWebSignatureSerializer(
        secret_key=current_app.config.get('JWT_SECRET_KEY'),
        salt=salt,
        algorithm_name=current_app.config.get('JWT_ALGORITHM', "HS256")
    )


def load_token():
    key = current_app.config['JWT_AUTH_HEADER_KEY']
    prefix = current_app.config['JWT_AUTH_HEADER_PREFIX']
    auth = request.headers.get(key, None)

    if auth is None:
        raise AuthFailed('Authorization Required')

    parts = auth.split()

    if parts[0].lower() != prefix.lower():
        raise AuthFailed('Invalid JWT header' 'Unsupported authorization type')
    elif len(parts) == 1:
        raise AuthFailed('Invalid JWT header' 'Token missing')
    elif len(parts) > 2:
        raise AuthFailed('Invalid JWT header' 'Token contains spaces')
    return parts[1]


def load_payload(payload, timed=True, salt=None):
    try:
        if timed:
            return get_timed_serializer(salt=salt).loads(payload)
        else:
            return get_serializer(salt=salt).loads(payload)
    except SignatureExpired:
        raise AuthFailed('Invalid JWT' 'Token is expired')
    except BadSignature:
        raise AuthFailed('Invalid JWT' 'Token is undecipherable')


def get_current_user():
    token = load_token()
    expired_key_prefix = current_app.config.get("INVALID_USER_TOKEN_PREFIX")
    if current_app.redis.get(expired_key_prefix + token):
        raise AuthFailed('Invalid JWT token as the user has logged out!')

    payload = load_payload(token)
    try:
        uid = ObjectId(payload['user_id'])
    except Exception:
        raise AuthFailed("Invalid token")

    user = current_app.mongodb.User.find_one_by_id(uid)

    sha = hmac.new(str(user['login']),
                   str(user['password_hash']),
                   hashlib.sha1)
    if sha.hexdigest() != payload['sha'] or not payload['sha']:
        raise AuthFailed("Invalid token")

    return user


def get_current_user_by_oauth():
    App = current_app.mongodb.App
    AppTrunk = current_app.mongodb.AppTrunk
    OAuth = current_app.mongodb.OAuth
    User = current_app.mongodb.User

    access_token = load_token()
    payload = load_payload(access_token)

    uid = payload["uid"]
    open_id = payload["open_id"]
    ext_key = payload["ext_key"]
    ext_secret = payload["ext_secret"]

    secret_key = current_app.config.get('JWT_SECRET_KEY')
    sha = hmac.new(str(ext_secret), str(secret_key), hashlib.sha1)
    if sha.hexdigest() != payload["sha"]:
        raise AuthFailed("Invalid token")

    app = App.find_one_by_id(open_id)
    trunk = AppTrunk.find_one_by_aid(open_id)
    oauth = OAuth.find_one_by_key_secret(ext_key, ext_secret)
    expired_key_prefix = current_app.config.get("OAUTH_INVALID_TOKEN_PREFIX")
    expired = current_app.redis.get(expired_key_prefix + access_token)
    ext_id = oauth["ext_id"]

    if not trunk or not app:
        raise AuthFailed('Invalid Access no app!')
    elif not oauth or not ext_id or str(app['owner_id']) != uid:
        raise AuthFailed('Invalid Access no authorize!')
    elif expired:
        raise AuthFailed('Invalid Access token is expired!')

    activated = trunk["extension"]["activated"]
    custom_ext = trunk["extension"]["custom"]

    if ext_id != custom_ext.get('id') and ext_id not in activated:
        raise AuthFailed('Invalid Access no extension activated!')

    try:
        user = User.find_one_by_id(uid)
        assert user is not None
    except Exception:
        raise AuthFailed("Invalid Access no user!")

    return user, app, access_token


def get_jwt_token():
    auth = request.headers.get('Authorization')
    parts = auth.split()
    return parts[1]


def generate_token(payload, expires_in=None, salt=None):
    if not isinstance(payload, (dict, list)):
        payload = unicode(payload)
    ts = get_timed_serializer(expires_in=expires_in, salt=salt)
    return ts.dumps(payload).decode("utf-8")


def generate_sid(payload, expires_in=None, salt=None):
    return generate_token(payload, expires_in, salt)


def generate_refresh_token(payload, salt=None):
    if not isinstance(payload, (dict, list)):
        payload = unicode(payload)
    return get_serializer(salt=salt).dumps(payload).decode("utf-8")


def generate_openid(payload, salt=None):
    if not isinstance(payload, (dict, list)):
        payload = unicode(payload)
    return get_serializer(salt=salt).dumps(payload).decode("utf-8")


def generate_hashed_password(pwd):
    return unicode(generate_password_hash(pwd))


def check_hashed_password(hashed, password):
    return check_password_hash(str(hashed), password)
