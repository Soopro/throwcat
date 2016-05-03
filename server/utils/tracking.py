#coding=utf-8
from __future__ import absolute_import

from flask import current_app
from bson import ObjectId

from utils.helpers import now
from apiresps.errors import MethodNotAllowed


def _create_track_user(uid):
    tracking = current_app.mongodb_conn.UserBehavior.find_one_by_uid(uid)
    if tracking is None:
        tracking = current_app.mongodb_conn.UserBehavior()
        tracking["user_id"] = ObjectId(uid)
        tracking.save()
    return tracking


def _get_track_user(uid):
    tracking = current_app.mongodb_conn.UserBehavior.find_one_by_uid(uid)
    if tracking is None:
        tracking = _create_track_user(uid)
    return tracking
    
    
def track_user_activated(uid):
    _create_track_user(uid)


def track_user_login(uid):
    tracking = _get_track_user(uid)
    if tracking is not None:
        tracking["last_login"] = now()
        tracking.save()


def track_user_logout(uid):
    tracking = _get_track_user(uid)
    if tracking is not None:
        tracking["last_logout"] = now()
        tracking.save()
        

def track_user_use_secret(uid, action=None):
    if not action or not isinstance(action, basestring):
        action = 'unknow'

    secret_rate_limit = current_app.config.get("SECRET_RATE_LIMIT", 1000)
    secret_rate_risk = current_app.config.get("SECRET_RISK_LIMIT", 100)
    secret_rate_expiration = current_app.config.get("SECRET_RATE_EXPIRATION",
                                                    3600*24)
    if secret_rate_limit < 0:
        return

    tracking = _get_track_user(uid)
    
    curr_secret = tracking.get("use_secret", [])
    summary = tracking.get("use_secret_summary", {}).get(action, 0)
    risk = tracking.get("risk", 0)
    curr_time = now()
    curr_secret = curr_secret[0:secret_rate_limit]
    if len(curr_secret) == secret_rate_limit:
        if curr_secret.pop(0) > curr_time - secret_rate_expiration:
            risk+=1

    curr_secret.append(curr_time)
    tracking["use_secret"] = curr_secret
    tracking["use_secret_summary"][action] = summary+1
    tracking["risk"] = risk
    tracking.save()
    
    # if a user's risk rank is too high will stop the action
    if risk > secret_rate_risk:
        raise MethodNotAllowed