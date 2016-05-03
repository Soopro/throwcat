#coding=utf-8
from __future__ import absolute_import

import os, re
from datetime import datetime
from flask import json, current_app

from utils.helpers import parse_int
from utils.validators import url_validator

from apiresps.errors import (TaxonomyNotFound,
                             TermNotFound,
                             MenuNotFound,
                             ContentNotFound,
                             ContentTypeNotFound,
                             ContentNotEnoughStorage,
                             ContentNotEnoughLiveStorage)


def parse_file_metas(page, base_url, options = None):
    data = {}
    if not options:
        options = {}
    
    meta = page.get("meta")
    for m in meta:
        data[m] = meta[m]
    _id = page.get('_id') or page.get('id')
    data['id'] = unicode(_id)
    data['alias'] = page.get('alias')
    data['parent'] = page.get('parent', u'')
    data['priority'] = page.get('priority',0)
    data['type'] = data['content_type'] = page.get('content_type')
    data['status'] = page.get('status', 0)
    data['updated'] = page.get('updated')
    data['creation'] = page.get('creation')
    data['date'] = meta.get('date', u'')
    data['date_formatted'] = helper_format_date(data['date'],
                                                options.get('date_format'))
    data['excerpt'] = helper_gen_excerpt(page['content'], 
                                         options.get('excerpt_length'),
                                         options.get('excerpt_ellipsis'))
    des = meta.get('description')
    data['description'] = data['excerpt'] if not des else des
    data['url'] = helper_gen_data_url(base_url, page)

    return data


def parse_file_content(content_string):
    return content_string


def clean_file_metas(meta):
    ContentFile = current_app.mongodb_conn.ContentFile
    for key in ContentFile.structure:
        meta.pop(key, None)
    meta.pop('id', None)
    meta.pop('date_formatted', None)
    meta.pop('url', None)
    meta.pop('type', None)
    meta.pop('excerpt', None)
    
    return meta


def helper_gen_data_url(base_url, data, static_type = 'page', index= 'index'):
    meta = data.get('meta',{})
    alias = data.get('alias')
    path = alias if alias != index else ''
    if data.get('content_type') == static_type:
        url = os.path.join(base_url, path)
    else:
        url = os.path.join(base_url, data['content_type'], path)
    return url


DEFAULT_EXCERPT_LENGTH = 162
DEFAULT_EXCERPT_ELLIPSIS = u'&hellip;'
def helper_gen_excerpt(content, length = DEFAULT_EXCERPT_LENGTH, 
                                ellipsis = DEFAULT_EXCERPT_ELLIPSIS):
    excerpt_length = parse_int(length) or DEFAULT_EXCERPT_LENGTH
    excerpt_ellipsis = ellipsis or DEFAULT_EXCERPT_ELLIPSIS
    
    content = parse_file_content(content)
    excerpt = re.sub(r'<[^>]*?>', '', content)

    if excerpt:
        excerpt = u" ".join(excerpt.split()) # remove empty strings.
        excerpt = u"{}{}".format(excerpt[0:excerpt_length], excerpt_ellipsis)
    return excerpt


DEFAULT_INPUT_DATE_FORMAT = '%Y-%m-%d'
def helper_format_date(date, to_format):
    if isinstance(date, basestring):
        input_date_format = current_app.config.get('DEFAULT_INPUT_DATE_FORMAT',
                                                    DEFAULT_INPUT_DATE_FORMAT)
        try:
            date_object = datetime.strptime(date, input_date_format)
        except Exception:
            return date

    elif isinstance(date, int):
        if len(str(date)) == 13:
            date = int(date/1000)
        try:
            date_object = datetime.fromtimestamp(date)
        except Exception:
            return date
    else:
        return date

    try:
        _fmted = date_object.strftime(to_format.encode('utf-8'))
        date_formatted = _fmted.decode('utf-8')
    except Exception:
        date_formatted = date
    return date_formatted

# menu
def helper_get_menu(app_id, menu_id):
    menu = current_app.mongodb_conn.\
                      Menu.find_one_by_aid_id(app_id, menu_id)
    if menu is None:
        raise MenuNotFound
    return menu


def helper_gen_menu(menus, base_url):
    if not menus:
        return {}
    def process_menu_url(menu):
        for item in menu:
            link = item.get("link")
            if link and not url_validator(link):
                item["url"] = os.path.join(base_url, link.strip('/'))
            else:
                item["url"] = link
            item["nodes"] = process_menu_url(item.get("nodes",[]))
        return menu

    menu_dict = {}
    for menu in menus:
        nodes = menu.get("nodes",[])
        nodes = process_menu_url(nodes)
        menu_dict[menu.get("alias")] = nodes

    return menu_dict

def helper_reformed_nodes(items):
    Menu = current_app.mongodb_conn.Menu
    CH_KEY = Menu.MENU_ITEM_CHILDREN_KEY
    STRUCTURE = Menu.MENU_ITEMS_STRUCTURE
    
    if not isinstance(items, list):
        items = []
    
    new_items = []
    for item in items:
        new_item = {}
        for k, struct in STRUCTURE.iteritems():
            _cls = struct[0]
            _default = struct[1]
            if k not in item or not isinstance(item.get(k), _cls):
                new_item[k]= _default
            else:
                new_item[k]= item.get(k)
            if new_item.get(CH_KEY):
                new_item[CH_KEY] = helper_reformed_nodes(new_item[CH_KEY])
        new_items.append(new_item)
    return new_items



def _process_children_terms(terms):
    term_aliases = []
    for term in terms:
        term["children"]= []
        term_alias = term.get("alias")
        term_aliases.append(term_alias)
        for t in terms:
            if term_alias != t.get("parent"):
                continue
            elif term_alias == t.get("alias"):
                t["parent"] = u''
                continue
            term["children"].append(t)
    
    root_terms = [term for term in terms 
                   if not term.get("parent") \
                   or term.get("parent") not in term_aliases ]
    output_terms = []
    
    def expand_term(term, terms):
        # check circular references children
        # if this process is from top level,
        # which is no valid parent or not parent at all.
        # then circular references will never be expaned.
        if term in terms:
            return terms
        terms.append(term)
        for t in term.get("children", []):
            t['level'] = term['level']+1            
            terms = expand_term(t, terms)
        return terms
    
    for term in root_terms:
        # reset root terms level and parent
        term['level'] = 0
        term["parent"] = u''
        # expand all root terms to same level
        output_terms = expand_term(term, output_terms)
    
    return output_terms

# taxonomy
def helper_gen_taxonomy(taxonomies, terms):
    if not taxonomies:
        return {}
    terms = list(terms)
    tax_dict = {}
    for tax in taxonomies:
        curr_terms = []
        for x in terms:
            if x['taxonomy'] != tax["alias"]:
                continue
            curr_terms.append({
                "alias": x.get("alias"),
                "title": x.get("title"),
                "meta": x.get("meta",{}),
                "taxonomy": x.get("taxonomy"),
                "parent": x.get("parent"),
                "priority": x.get("priority"),
                "children": [],
                "updated": x.get("updated")
            })
        
        curr_terms = sorted(curr_terms, key=lambda k: k['priority'])
        curr_terms = _process_children_terms(curr_terms)
        
        # for term in  curr_terms:
        #     print ('-'*term['level'], term['alias'],
        #            term['parent'], term['priority'],
        #            [{"alias": child["alias"]} for child in term['children']])

        tax_dict[tax["alias"]] = {
            "title": tax.get("title"),
            "alias": tax.get("alias"),
            "content_types": tax.get("content_types"),
            "terms": curr_terms
        }
        
        # narrow down the search range of terms.
        terms[:] = [y for y in terms if y['taxonomy'] != tax["alias"]]

    return tax_dict
    

def helper_get_taxonomy(app_id, tax_id):
    tax = current_app.mongodb_conn.\
                      Taxonomy.find_one_by_aid_id(app_id, tax_id)
    if tax is None:
        raise TaxonomyNotFound
    return tax


# terms
def helper_get_term(app_id, tax_alias, term_id):
    term = current_app.mongodb_conn.\
                      Term.find_one_by_aid_n_tax_n_id(app_id,
                                                      tax_alias,
                                                      term_id)
    if term is None:
        raise TermNotFound
    return term

def helper_test_waste_terms(terms):
    terms = list(terms)
    used_terms = _process_children_terms(terms)
    bad_terms = []
    for term in terms:
        if term not in used_terms:
            bad_terms.append(term.get('alias'))
    return bad_terms


# content
def helper_get_content_file(app_id, type_alias, file_id):
    if isinstance(type_alias, basestring):
        content_file = current_app.mongodb_conn.\
                            ContentFile.find_one_by_aid_type_id(app_id,
                                                                type_alias,
                                                                file_id)
    else:
        content_file = current_app.mongodb_conn.\
                            ContentFile.find_one_by_aid_id(app_id, file_id)

    if content_file is None:
        raise ContentNotFound
    
    return content_file


def helper_get_content_type(app_id, type_id):
    content_type = current_app.mongodb_conn.\
                    ContentType.find_one_by_aid_id(app_id, type_id)
    if content_type is None:
        raise ContentTypeNotFound
    return content_type


def helper_verify_content_type(ctype_alias, app, skip_except=False):
    content_type = current_app.mongodb_conn.\
                        ContentType.find_one_by_aid_ctype(app["_id"],
                                                          ctype_alias)
    if not content_type:
        if not skip_except:
            raise ContentTypeNotFound
        else:
            return False

    return True


def helper_gen_file_marks(file, curr_meta = None):
    ContentFile = current_app.mongodb_conn.ContentFile
    
    if file["alias"] == ContentFile.DEFAULT_INDEX_ALIAS:
        file["is_front"] = True
    if file["alias"] == ContentFile.DEFAULT_404_ALIAS:
        file["is_404"] = True
    if curr_meta and file["alias"] == curr_meta["alias"] \
    and file["content_type"] == curr_meta["content_type"]:
        file["is_current"] = True
    return file


def helper_check_storage(app_id, customer, status, archive):
    ContentFile = current_app.mongodb_conn.ContentFile
    max_storage = customer.get_storage(ContentFile.MAXIMUM_STORAGE)
    if ContentFile.count_used(app_id) >= max_storage:
        raise ContentNotEnoughStorage
    
    if status == ContentFile.STATUS_PUBLISHED and not archive:
        max_live = customer.get_storage(ContentFile.MAXIMUM_STORAGE)
        if ContentFile.count_live(app_id) >= max_live:
            raise ContentNotEnoughLiveStorage
    
    return True
