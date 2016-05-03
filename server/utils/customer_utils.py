#coding=utf-8
from __future__ import absolute_import

import os, re, gettext
from flask import json, current_app, g

from apiresps.errors import CustomerNotFound



def helper_get_customer(uid):
    customer = current_app.mongodb_conn.Customer.find_one_by_uid(uid)
    if customer is None:
        raise CustomerNotFound
    return customer