# coding=utf-8
from __future__ import absolute_import

import os
import re
from flask import json, current_app, g, request

from utils.validators import url_validator
from utils.helpers import (pre_process_alias,
                           version_str_to_list,
                           version_list_to_str,
                           now)

from apiresps.errors import (MethodNotAllowed,
                             ThemeNotFound,
                             ThemeConfigInvalid,
                             ThemePresetsInvalid,
                             ThemeTranslatesInvalid,
                             ThemeTemplateFileInvalid,
                             ThemeTemplateFileNotFound,
                             ThemeTemplateFileCircularInclude,
                             ExtensionConfigInvalid,
                             AppNotFoundOrNotOwner,
                             AppTrunkNotFound,
                             UserNotFound)


# app
def helper_get_app_by_alias(app_alias, owner_id=None, required=True):
    App = current_app.mongodb_conn.App
    app_alias = pre_process_alias(app_alias)

    if not owner_id:
        try:
            user = g.curr_user
            owner_id = user['_id']
            assert owner_id is not None
        except:
            raise AppNotFoundOrNotOwner
    if app_alias and owner_id:
        app = App.find_one_by_oid_alias(owner_id, app_alias)
    else:
        app = None
    if not app and required:
        raise AppNotFoundOrNotOwner
    return app


def helper_get_app_by_id(app_id,
                         owner_id=None,
                         check_owner=True,
                         required=True):
    App = current_app.mongodb_conn.App
    if check_owner:
        if not owner_id:
            try:
                user = g.curr_user
                owner_id = user['_id']
                assert owner_id is not None
            except:
                raise AppNotFoundOrNotOwner
        if owner_id and app_id:
            app = App.find_one_by_id_n_oid(app_id, owner_id)
        else:
            app = None
    else:
        app = App.find_one_by_id(app_id)
    if not app and required:
        raise AppNotFoundOrNotOwner
    return app


def helper_gen_app_uri(app, owner):
    apps_url = current_app.config.get('APPS_URL')
    return os.path.join(apps_url, owner["alias"], app["alias"])


def helper_gen_app_base_url(app, owner, protocol=True):
    if app.get("domain"):
        app_base_url = u"{}://{}".format(app.get('protocol'), app["domain"])
    else:
        app_base_url = helper_gen_app_uri(app, owner)
    if not protocol:
        app_base_url = app_base_url.split("://", 1)[-1]
    return app_base_url


def helper_find_app_exist(app, check_owner=True):
    if app is None or app.get('deleted'):
        return False
    elif check_owner:
        try:
            user = g.curr_user
        except Exception:
            user = {}
        if user.get("_id") != app.get('owner_id') and \
           app.get('owner_id') is not None:
            return False
    return True


def helper_test_suspicious(app):
    if not app:
        raise AppNotFoundOrNotOwner
    owner = current_app.mongodb_conn.User.find_one_by_id(app['owner_id'])
    if not owner:
        raise UserNotFound

    base = helper_gen_app_base_url(app, owner, False)
    prefix = u"{}://".format(app.get('protocol'))
    referrer = request.referrer or ''
    referrer = referrer.replace(prefix, '')
    if base.startswith('www.'):
        base = base[4:]
    if referrer.startswith('www.'):
        referrer = referrer[4:]
    if not referrer.startswith(base) and not current_app.debug:
        current_app.logger.warn(
            "Suspicious requests from {}".format(request.referrer),
        )
        raise MethodNotAllowed


def helper_get_app_trunk(app_id, skip_except=False, ensure=False):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    trunk = AppTrunk.find_one_by_aid(app_id)

    if not trunk and ensure:
        trunk = AppTrunk()
        trunk["app_id"] = app_id
        trunk.save()
    elif not trunk and not skip_except:
        raise AppTrunkNotFound
    return trunk or {}


# theme
def helper_ensure_absurl(src, base_url):
    if not src:
        return ''
    if url_validator(src):
        return src
    else:
        base_url = base_url.rstrip('/')
        src = src.lstrip('/')
        return "{}/{}".format(base_url, src)


def helper_load_default_theme(app_type):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    Template = current_app.mongodb_conn.Template
    scope = u"{}/{}".format(AppTrunk.DEFAULT_THEME_NAME, app_type)
    config_file = AppTrunk.THEME_CONFIG_FILE
    presets_file = AppTrunk.THEME_PRESETS_FILE

    # process config
    config_str = None
    config_data = Template.find_one_by_scope_key(scope, config_file)
    if config_data:
        config_str = config_data['content']
    theme_config = helper_read_app_theme_config(config_str)

    # process presets
    presets_str = None
    presets_data = Template.find_one_by_scope_key(scope, presets_file)
    if presets_data:
        presets_str = presets_data['content']
    theme_presets = helper_read_app_theme_presets(presets_str)

    return {
        "config": theme_config,
        "presets": theme_presets,
    }


def helper_read_app_theme_config(config_str):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    App = current_app.mongodb_conn.App
    try:
        decoded = json.loads(config_str)
        assert isinstance(decoded, dict)
    except Exception:
        raise ThemeConfigInvalid

    theme_config = decoded

    # ensure template
    template = theme_config.get("template")
    if not template or isinstance(template, dict):
        theme_config["template"] = {
            AppTrunk.DEFAULT_TEMPLATE: AppTrunk.DEFAULT_TEMPLATE,
        }

    # ensure alias
    theme_config["alias"] = theme_config.get("alias",
                                             u"theme-{}".format(now()))
    # ensure version
    version = theme_config.get("version", "0.0.0")
    theme_config["version"] = version_str_to_list(version)

    # ensure options
    theme_config["options"] = theme_config.get("options", {})

    # ensure ext slots
    allowed_slots = theme_config.get("allowed_slots", [])
    theme_config["allowed_slots"] = [slot.lower() for slot in allowed_slots
                                     if isinstance(slot, basestring)]

    # ensure capabilities
    capability = theme_config.get("capability")
    capabilities = theme_config.get("capabilities") or capability
    if not capabilities or not isinstance(capabilities, list):
        if isinstance(capabilities, basestring):
            capabilities = [capabilities]
        else:
            capabilities = list(App.APPTYPES)

    theme_config["capabilities"] = capabilities

    return theme_config


def helper_read_app_theme_presets(presets_str):
    if not presets_str:
        return []
    try:
        decoded = json.loads(presets_str)
        assert isinstance(decoded, list)
    except Exception:
        raise ThemePresetsInvalid

    presets = []
    for preset in decoded:
        presets.append({
            "key": preset.get("key"),
            "name": preset.get("name"),
            "preview": preset.get("preview"),
            "code": preset.get("code"),
        })

    return presets


def helper_get_theme_url(payload_id, app=None):
    theme_static_url = current_app.config.get("THEME_STATIC_URL")
    scope = helper_get_theme_scope(payload_id, app).strip('/')
    return os.path.join(theme_static_url, scope)


def helper_get_theme_scope(payload_id, app=None):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    if not payload_id:
        raise ThemeNotFound
    elif payload_id == AppTrunk.DEFAULT_THEME_NAME:
        scope = u"{}/{}".format(AppTrunk.DEFAULT_THEME_NAME, app['type'])
    elif payload_id == AppTrunk.CUSTOM_THEME_NAME:
        scope = u"{}/{}".format(AppTrunk.CUSTOM_THEME_NAME,
                                unicode(app['_id']))
    else:
        scope = u"{}/{}".format(AppTrunk.PUBLIC_THEME_NAME, payload_id)

    return scope


def helper_exists_theme_template(payload_id, app, template_name):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    key = u"{}.{}".format(template_name, AppTrunk.TEMPLATE_EXT)
    scope = helper_get_theme_scope(payload_id, app)
    exists = current_app.mongodb_conn.\
        Template.find_exists_scope_key(scope, key)
    return exists


def helper_get_theme_template(payload_id, app, key):
    scope = helper_get_theme_scope(payload_id, app)
    template = current_app.mongodb_conn.\
        Template.find_one_by_scope_key(scope, key)
    return template


def _fill_theme_profile_meta(theme, meta, app=None):
    theme["author"] = meta.get("author", u"")
    theme["title"] = meta.get("title", u"")
    theme["description"] = meta.get("description", u"")
    theme["capabilities"] = meta.get("capabilities", [])

    payload_id = theme.get("payload_id", u"")
    theme_url = helper_get_theme_url(payload_id, app)
    thumbnail = meta.get("thumbnail", u"")
    poster = meta.get("poster", u"")

    theme["theme_url"] = theme_url
    theme["thumbnail"] = helper_ensure_absurl(thumbnail, theme_url)

    theme["poster"] = helper_ensure_absurl(poster, theme_url)
    theme["preivews"] = [os.path.join(pic, theme_url)
                         for pic in list(meta.get('previews', []))
                         if pic and isinstance(pic, basestring)]
    return theme


def helper_get_current_theme_profile(current_theme, app):
    meta = current_theme.get("config", {})
    output = {}
    output["id"] = app["_id"]
    output["payload_id"] = current_theme["id"]
    output["version"] = version_list_to_str(meta.get("version"))
    output["alias"] = meta.get("alias")
    output["templates"] = meta.get("templates")
    # current theme may not have version and alias
    output["options"] = meta.get("options")
    output["styles"] = meta.get("styles")
    output["danger"] = meta.get("danger", False)
    output["is_current"] = True
    _fill_theme_profile_meta(output, meta, app)
    return output


def helper_get_default_theme_profile(default_theme, app):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    meta = default_theme.get("config", {})
    output = {}
    output["id"] = AppTrunk.DEFAULT_THEME_NAME
    output["payload_id"] = AppTrunk.DEFAULT_THEME_NAME
    output["version"] = version_list_to_str(meta.get("version"))
    output["alias"] = meta.get("alias", AppTrunk.DEFAULT_THEME_NAME)

    _fill_theme_profile_meta(output, meta, app)
    return output


def helper_get_custom_theme_profile(custom_theme, app):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    meta = custom_theme.get("config")
    if not meta:
        return None
    output = {}
    output["id"] = AppTrunk.CUSTOM_THEME_NAME
    output["payload_id"] = AppTrunk.CUSTOM_THEME_NAME
    output["version"] = version_list_to_str(meta.get("version"))
    output["alias"] = meta.get("alias", AppTrunk.CUSTOM_THEME_NAME)

    _fill_theme_profile_meta(output, meta, app)
    return output


def helper_get_theme_profile(theme):
    payload = theme.get("payload", {}) or {}
    meta = payload.get('meta', {})
    output = {}
    output["id"] = theme["_id"]
    output["payload_id"] = payload.get("_id")
    output["version"] = version_list_to_str(payload.get("version"))

    output["alias"] = theme["alias"]
    output["creation"] = theme["creation"]
    output["updated"] = theme["updated"]

    _fill_theme_profile_meta(output, meta)
    return output


# extension
def helper_read_app_extension_config(config_str):
    try:
        decoded = json.loads(config_str)
        assert isinstance(decoded, dict)
    except Exception:
        raise ExtensionConfigInvalid

    ext_config = decoded
    ext_config.setdefault("author", u"")
    ext_config.setdefault("title", u"")
    ext_config.setdefault("description", u"")
    ext_config.setdefault("capabilities", [])
    ext_config.setdefault("protocol", u"")
    ext_config.setdefault("domain", u"")
    ext_config.setdefault("entrance", u"")
    ext_config.setdefault("thumbnail", u"")
    ext_config.setdefault("poster", u"")
    ext_config.setdefault("preivews", [])
    ext_config.setdefault("scripts", u"")

    return ext_config


def helper_get_extension_meta(meta):
    if not meta:
        return {"empty": True}
    output = {}
    output["author"] = meta.get("author")
    output["title"] = meta.get("title")
    output["description"] = meta.get("description")
    output["capabilities"] = meta.get("capabilities")
    base_url = "{}://{}/{}".format(meta.get('protocol', ""),
                                   meta.get('domain', ""),
                                   meta.get('path', "").strip("/"))
    output["base_url"] = base_url
    output["entrance"] = meta.get("entrance", base_url)
    output["thumbnail"] = helper_ensure_absurl(meta.get("thumbnail", ""),
                                               base_url)
    output["poster"] = helper_ensure_absurl(meta.get("poster", ""), base_url)
    output["preivews"] = [helper_ensure_absurl(pic, base_url)
                          for pic in list(meta.get('previews', []))
                          if pic and isinstance(pic, basestring)]
    output["installable"] = bool(meta.get("scripts"))

    return output


def helper_get_extension_profile(ext):
    payload = ext.get("payload", {})
    meta = payload.get('meta', {})
    output = helper_get_extension_meta(meta)
    output["id"] = ext["_id"]
    output["alias"] = ext["alias"]
    output["creation"] = ext["creation"]
    output["updated"] = ext["updated"]

    return output


def helper_get_custom_extension_profile(ext_meta):
    AppTrunk = current_app.mongodb_conn.AppTrunk
    output = helper_get_extension_meta(ext_meta)
    output["id"] = ext_meta.get('id')
    output["alias"] = AppTrunk.CUSTOM_EXT_NAME

    return output


# template
tmpl_reg = r"{0}{1}{2}".format(
    r'(\s*)(\{%\s*(?:include|import)\s+',
    r'["\']?\s*([\w\$\-\./\{\}\(\)]*)\s*["\']?',
    r'\s*[^%\}]*%\})',
)
incl_regex = re.compile(tmpl_reg, re.MULTILINE | re.DOTALL | re.IGNORECASE)
incl_safety_lock = 100


def _relative_path_key(scope, curr_key, include_key):
    include_key = include_key.rstrip('/')

    if include_key.startswith('/'):
        return os.path.normpath(include_key[1:])
    else:
        base = '/'.join(curr_key.split('/')[:-1])
        return os.path.normpath(os.path.join(base, include_key))


def _process_html_includes(content, scope, key, history=[]):
    for space, match, include_key in incl_regex.findall(content):
        incl_key = _relative_path_key(scope, key, include_key)

        if incl_key in history or len(history) > incl_safety_lock:
            raise ThemeTemplateFileCircularInclude(incl_key)

        template = current_app.mongodb_conn.\
            Template.find_one_by_scope_key(scope, incl_key)
        if not template:
            raise ThemeTemplateFileNotFound(incl_key)

        history.append(incl_key)
        sub_content = _process_html_includes(template['content'],
                                             scope,
                                             incl_key,
                                             history)
        sub_splits = sub_content.splitlines()
        _line = u'{}'.format(space)
        # because the regex is match after spaces,
        # so only add spaces for other lines.
        content = content.replace(match, _line.join(sub_splits))

    return content


def helper_parse_tpl(content, scope, key):
    try:
        content = _process_html_includes(content, scope, key, [])
        content = re.sub(r'<(script).*?</\1>(?s)', u'', content)
        content = re.sub(r'<script\s*.*?>', u'', content)
    except ThemeTemplateFileCircularInclude as e:
        raise e
    except Exception as e:
        raise ThemeTemplateFileInvalid

    return content


# socials
def helper_get_socials(socials):
    """ socials json sample
    {
       "facebook":{
           "name":"Facebook",
           "url":"http://....",
           "code":"..."
       },
       "twitter":{
           "name":"Twitter",
           "url":"http://....",
           "code":"..."
       }
    }
    """
    if not socials:
        return []

    social_list = []
    # directly append if is list
    if isinstance(socials, list):
        for social in socials:
            if social.get('key'):
                social_list.append(social)
    # change to list if is dict
    if isinstance(socials, dict):
        for social in socials:
            tmp_social = socials[social]
            tmp_social.update({"key": social})
            social_list.append(tmp_social)

    if not social_list:
        return None

    return social_list


# translates
def helper_get_translates(translates, locale):
    """ translates json sample
    {
       "zh_CN":{"name":"汉语","url":"http://....."},
       "en_US":{"name":"English","url":"http://....."}
    }
    """
    if not translates:
        return None

    trans_list = []
    lang = locale.split('_')[0]

    # directly append if is list
    if isinstance(translates, list):
        for trans in translates:
            if trans.get('key'):
                trans_list.append(trans)
    # change to list if is dict
    if isinstance(translates, dict):
        for trans in translates:
            tmp_trans = translates[trans]
            tmp_trans.update({"key": trans})
            trans_list.append(tmp_trans)

    if not trans_list:
        return None

    for trans in trans_list:
        trans_key = trans['key'].lower()
        if trans_key == locale.lower() or trans_key == lang.lower():
            trans["active"] = True

    return trans_list


def helper_get_translate_texts(payload_id, app):
    scope = helper_get_theme_scope(payload_id, app)
    locale = (app['locale'] or 'en').lower()

    lang_key = os.path.join('languages', '{}.lang'.format(locale))
    lang_file = current_app.mongodb_conn.\
        Template.find_one_by_scope_key(scope, lang_key)

    if not lang_file:
        lang = locale.split('_')[0]
        lang_key = os.path.join('languages', '{}.lang'.format(lang))
        lang_file = current_app.mongodb_conn.\
            Template.find_one_by_scope_key(scope, lang_key)
    dictinoary = []

    if lang_file:
        try:
            dictinoary = json.loads(lang_file['content'])
        except:
            raise ThemeTranslatesInvalid

    return dictinoary

# def helper_get_translate_texts(theme_folder, locale):
#     AppTrunk = current_app.mongodb_conn.AppTrunk
#     path = os.path.join(theme_folder, 'languages', '{}.lang'.format(locale))
#     if not os.path.isfile(path):
#         lang = locale.split('_')[0]
#         path = os.path.join(theme_folder, 'languages',
#                                           '{}.lang'.format(lang))
#     dictinoary = []
#
#     if os.path.isfile(path):
#         try:
#             with open(path) as f:
#                 dictinoary = json.load(f)
#             assert isinstance(dictinoary, list)
#         except:
#             raise ThemeTranslatesInvalid
#
#     return dictinoary


# gfw
def helper_gen_gfw():
    try:
        return bool(current_app.config.get('GFW'))
    except:
        return False


# analytics
def helper_get_analytics(app_id, page_id=None):
    if app_id:
        sa_status = current_app.sa_mod.analyze_app(str(app_id))
        sa = {
            'app': {
                'pv': sa_status.get("pv"),
                'vs': sa_status.get("vs"),
                'uv': sa_status.get("uv"),
                'ip': sa_status.get("ip"),
            }
        }

    if page_id:
        sa_page_status = current_app.sa_mod.analyze_page(str(page_id))
        sa['page'] = {
            'pv': sa_page_status.get("pv"),
            'vs': sa_page_status.get("vs"),
            'uv': sa_page_status.get("uv"),
            'ip': sa_page_status.get("ip"),
        }

    return sa
