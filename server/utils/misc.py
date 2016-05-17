# coding=utf-8
from __future__ import absolute_import

from functools import partial
from werkzeug.datastructures import ImmutableDict
from werkzeug.utils import secure_filename
from bson import ObjectId
from functools import cmp_to_key
import re
import time
import hashlib
import hmac
import urllib
import urlparse
import mimetypes
import short_url
import random


class DottedImmutableDict(ImmutableDict):
    def __getattr__(self, item):
        try:
            v = self.__getitem__(item)
        except KeyError:
            # ImmutableDict will take care rest errors.
            return ''
        if isinstance(v, dict):
            v = DottedImmutableDict(v)
        return v


class NamedPartial(partial):
    @property
    def __name__(self):
        return self.func.__name__


def route_inject(app_or_blueprint, url_patterns):
    for pattern in url_patterns:
        options = pattern[3] if len(pattern) > 3 else {}
        app_or_blueprint.add_url_rule(pattern[0],
                                      view_func=pattern[1],
                                      methods=pattern[2].split(),
                                      **options)


_valid_slug = re.compile(r'^[a-z0-9_\-]+$')
_word = re.compile(r'\w')
_white_space = re.compile(r'\s')


def pre_process_slug(value):
    """
    :param value: value
    :return: slug after process
    """
    try:
        slug = value.lower()
        if _valid_slug.match(slug) is None:
            raise Exception
    except Exception:
        slug = None

    return slug


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except ValueError:
        return default


def now(dig=10):
    if dig == 10:
        return int(time.time())
    elif dig == 11:
        return int(time.time() * 10)
    elif dig == 12:
        return int(time.time() * 100)
    elif dig == 13:
        return int(time.time() * 1000)
    elif dig == 14:
        return int(time.time() * 10000)
    elif dig == 15:
        return int(time.time() * 100000)
    elif dig == 16:
        return int(time.time() * 1000000)
    else:
        return time.time()


def sleep(t):
    time.sleep(t)


def get_url_params(url, unique=True):
    url_parts = list(urlparse.urlparse(url))
    params = urlparse.parse_qsl(url_parts[4])
    if unique:
        params = dict(params)
    return params


def add_url_params(url, new_params, concat=True, unique=True):
    if isinstance(new_params, dict):
        new_params = [(k, v) for k, v in new_params.iteritems()]

    url_parts = list(urlparse.urlparse(url))
    params = urlparse.parse_qsl(url_parts[4])
    params = new_params if not concat else params + new_params

    if unique:
        params = dict(params)

    url_parts[4] = urllib.urlencode(params)

    return urlparse.urlunparse(url_parts)


def safe_regex_str(val):
    if isinstance(val, unicode):
        val = val.decode("utf-8")
    elif not isinstance(val, str):
        return None
    val = val.replace("/", "\/")
    val = val.replace("*", "\*")
    val = val.replace(".", "\.")
    val = val.replace("[", "\[")
    val = val.replace("]", "\]")
    val = val.replace("(", "\(")
    val = val.replace(")", "\)")
    val = val.replace("^", "\^")
    val = val.replace("|", "\|")
    val = val.replace("{", "\{")
    val = val.replace("}", "\}")
    val = val.replace("?", "\?")
    val = val.replace("$", "\$")
    return val


def sortedby(source, sort_keys, reverse=False):
    keys = {}

    def process_key(key):
        if key.startswith('-'):
            key = key.lstrip('-')
            revs = -1
        else:
            key = key.lstrip('+')
            revs = 1
        keys.update({key: revs})

    if isinstance(sort_keys, basestring):
        process_key(sort_keys)
    elif isinstance(sort_keys, list):
        for key in sort_keys:
            if not isinstance(key, basestring):
                continue
            process_key(key)

    def compare(a, b):
        for key, value in keys.iteritems():
            if a.get(key) < b.get(key):
                return -1 * value
            if a.get(key) > b.get(key):
                return 1 * value
        return 0

    return sorted(source, key=cmp_to_key(compare), reverse=reverse)


def parse_int(num, default=0):
    try:
        return int(float(num))
    except:
        return default


def parse_dict_by_structure(obj, structure):
    if not isinstance(obj, dict):
        return None
    newobj = {}
    for k, v in structure.iteritems():
        if type(obj.get(k)) is not v:
            newobj.update({k: v()})
        else:
            newobj.update({k: obj.get(k)})
    return newobj


def version_str_to_list(str_version):
    try:
        version = [int(v) for v in str_version.split('.')]
        assert len(version) == 3
    except:
        version = None
    return version


def version_list_to_str(list_version):
    try:
        list_version += [0, 0, 0]  # ensure has 3 items
        list_version = list_version[0:3]
        version = '.'.join(map(str, list_version))
    except:
        version = None
    return version


def is_ObjectId(_id):
    return _id and ObjectId.is_valid(_id)


def safe_filename(filename, mimetype=None):
    _starts = re.match(r'_*', filename)

    if not mimetype:
        try:
            mimetype = mimetypes.guess_type(filename)[0]
        except:
            mimetype = None

    name = secure_filename(filename)
    if not name:
        time_now = int(time.time())
        name = u'unknow_filename_{}'.format(time_now)
    if '.' not in name and mimetype:
        ext = mimetypes.guess_extension(mimetype)
        if ext.startswith('.'):
            ext = ext[1:]
        else:
            ext = mimetypes.split('/')[-1]
        name = '{}.{}'.format(name, ext)

    return u"{}{}".format(_starts.group(), name)


def file_md5(fname):
    _hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            _hash.update(chunk)
    return _hash.hexdigest()


def hmac_sha(key, msg, digestmod=None, output=True):
    if digestmod is None:
        digestmod = hashlib.sha1
    sha = hmac.new(str(key), str(msg), digestmod=digestmod)
    if output:
        return sha.hexdigest()
    else:
        return sha


def str2unicode(text):
    if isinstance(text, str):
        return text.decode('utf-8')
    return text


def unicode2str(text):
    if isinstance(text, unicode):
        return text.encode('utf-8')
    return text
