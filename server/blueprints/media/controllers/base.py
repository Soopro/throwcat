# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g
# from PIL import Image
import uuid
import os
import mimetypes

from services.cdn import qiniu

from utils.api_utils import output_json
from utils.request import get_param
from utils.helpers import now, safe_filename

from apiresps.validations import Struct

from ..errors import *


def allowed_file(filename):
    file_ext = ''
    allowed_exts = current_app.config.get('ALLOWED_EXTENSIONS')
    if '.' in filename:
        file_ext = filename.rsplit('.', 1)[1]
    return file_ext.lower() in allowed_exts


@output_json
def list_media():
    user = g.curr_user

    scope = helper_get_media_scope(user)
    medias = current_app.mongodb_conn.\
        Media.find_by_oid_scope(user['_id'], scope)

    media_list = [output_media(media) for media in medias]

    return media_list


@output_json
def upload_authorize():
    filename = get_param('filename', Struct.Filename, True)
    method = get_param('method', Struct.Attr, default=u"POST")
    mimetype = get_param('mimetype', Struct.Attr, default=u"image/jpeg")
    headers = get_param('headers', Struct.Dict, default={})
    md5 = get_param('md5', Struct.MD5)
    is_new = get_param('is_new', Struct.Bool)

    user = g.curr_user

    key = filename = safe_filename(filename, mimetype)
    scope = helper_get_media_scope(user)
    media = helper_find_media(scope, key, user["_id"])

    if is_new and media is not None:
        file_name, file_ext = os.path.splitext(filename)
        key = filename = '{}-{}{}'.format(file_name,
                                          uuid.uuid4().hex,
                                          file_ext)
    elif not is_new:
        if media is None:
            raise MediaNotFound('auth')
        elif media['mimetype'] != mimetype or media['filename'] != filename:
            raise MediaTypeNotAllowed('auth')

    cdn_key = "{}/{}".format(scope, key)
    bucket = current_app.config.get('CDN_UPLOADS_BUCKET')

    try:
        api_url = qiniu.get_api_url()
        auth = qiniu.authorize(bucket, cdn_key)
    except Exception:
        raise MediaAuthorizeFailed

    return {
        'api_url': api_url,
        'name': filename,
        'cdn_key': cdn_key,
        'token': auth,
        'method': method,
        'mimetype': mimetype,
        'headers': headers,
        'md5': md5,
    }


@output_json
def get_media(filename):
    Struct.Filename(filename, 'filename')

    user = g.curr_user

    scope = helper_get_media_scope(user)
    media = helper_find_media(scope, filename, user["_id"])
    if media is None:
        raise MediaNotFound

    return output_media(media)


@output_json
def save_media():
    filename = get_param('name', Struct.Filename, True)
    # use 'name' because filename will conflict with other rest api.
    mimetype = get_param('mimetype', Struct.Attr, True)
    upload = get_param('upload', Struct.Bool, default=False)
    recipe = get_param('recipe', Struct.Dict, default={})

    user = g.curr_user

    scope = helper_get_media_scope(user)
    media = helper_find_media(scope, filename, user["_id"])
    if media is not None:
        raise MediaExists

    media_type = _get_media_type(filename, mimetype)
    key = filename
    ext = _get_media_ext(filename)

    media = current_app.mongodb_conn.Media()
    if upload:
        media['uploaded'] = now()
    media['owner_id'] = user['_id']
    media['scope'] = unicode(scope)
    media['filename'] = unicode(filename)
    media['mimetype'] = unicode(mimetype)
    media['type'] = unicode(media_type)
    media['ext'] = unicode(ext)
    media['key'] = unicode(key)
    media['recipe'] = recipe
    media.save()

    return output_media(media)


@output_json
def update_media(filename):
    Struct.Filename(filename, 'filename')

    recipe = get_param('recipe', Struct.Dict, default={})
    upload = get_param('upload', Struct.Bool, default=False)

    user = g.curr_user

    scope = helper_get_media_scope(user)
    media = helper_find_media(scope, filename, user["_id"])
    if media is None:
        raise MediaNotFound

    if upload:
        media['uploaded'] = now()
    media['recipe'] = recipe
    media.save()

    return output_media(media)


@output_json
def delete_media(filename):
    Struct.Filename(filename, 'filename')

    user = g.curr_user

    scope = helper_get_media_scope(user)
    media = helper_find_media(scope, filename, user["_id"])
    if media is None:
        raise MediaNotFound

    bucket = current_app.config.get('CDN_UPLOADS_BUCKET')

    cdn_key = "{}/{}".format(scope, filename)
    try:
        qiniu.delete(bucket, cdn_key)
    except Exception as e:
        current_app.logger.warn(MediaDeleteFailed(str(e)))

    media.delete()

    return {
        'updated': now(),
        'deleted': 1,
    }


# helpers

def helper_find_media(scope, key, owner_id=None):
    Media = current_app.mongodb_conn.Media
    if not key or not scope:
        raise MediaInvalidKey
    elif owner_id is None:
        media = Media.find_one_by_scope_key(scope, key)
    else:
        media = Media.find_one_by_oid_key(owner_id, key)

    return media


def helper_get_media_scope(user):
    return user["slug"]


def _get_media_ext(filename):
    try:
        return os.path.splitext(filename)[1][1:].lower()
    except:
        return None


def _get_media_type(filename, mimetype=None):
    try:
        media_type = mimetypes.guess_type(filename)[0].split('/')[0]
    except:
        media_type = None
    if not media_type and mimetype:
        media_type = mimetype.split('/')[0]
    return media_type


def _get_media_mimetype(filename):
    try:
        return mimetypes.guess_type(filename)[0]
    except:
        return None


def _media_src(scope, key):
    uploads_url = current_app.config.get('UPLOADS_URL')
    return '/'.join([uploads_url, scope, key])


def _media_original(src, suffix='original'):
    pair = '&' if '?' in src else '?'
    return "{0}{1}{2}".format(src, pair, suffix)


def _media_thumbnail_src(src, ext, suffix='thumbnail'):
    if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
        pair = '&' if '?' in src else '?'
        thumbnail = "{0}{1}{2}".format(src, pair, suffix)
    else:
        thumbnail = src
    return thumbnail


# output
def output_media(media):
    scope = media['scope']
    src = _media_src(scope, media['key'])
    return {
        'id': media['_id'],
        'filename': media['filename'],
        'scope': scope,
        'src': src,
        'original': _media_original(src),
        'recipe': media['recipe'],
        'thumbnail': _media_thumbnail_src(src, media['ext']),
        'type': media['type'],
        'mimetype': media['mimetype'],
        'ext': media['ext'],
        'updated': media['updated'],
    }
