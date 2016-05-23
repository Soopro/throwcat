# coding=utf-8
from __future__ import absolute_import

from apiresps.validations import Struct

from .errors import *


KEYS = {
    "src": Struct.Url,
    "tip": Struct.Attr,
    "answer": Struct.Attr,
    "recipe": {
        # "ah": Struct.Int,
        # "aw": Struct.Int,
        # "rh": Struct.Int,
        # "rw": Struct.Int,
        "asoect_ratio": Struct.Int,
        "height": Struct.Int,
        "width": Struct.Int,
        "modified": Struct.Bool,
        "crop": {
            "h": Struct.Float,
            "w": Struct.Float,
            "x": Struct.Float,
            "y": Struct.Float
        }
    }
}


def check_type(_type):
    if not 0 <= _type < 2:
        raise ParamError("type")
    else:
        return _type


def check_item(item, KEYS, item_str):
    for key, validation in KEYS.iteritems():
        try:
            attr_str = "{}.{}".format(item_str, key)
            if isinstance(validation, dict):
                check_item(item[key], validation, attr_str)
            else:
                validation(item[key], key)
        except Exception:
            raise ParamError("{} error".format(attr_str))

    return item


# def check_resource(resource):
#     KEYS = {
#         "src": Struct.Url,
#         "tip": Struct.Attr,
#         "answer": Struct.Attr,
#         "recipe": check_recipe,
#     }
#     for key, validation in KEYS.iteritems():
#         try:
#             if isinstance(validation, dict):
#                 check_item(validation)
#             else:
#                 validation(resource[key], key)
#         except Exception:
#             raise Exception("resource error")

#     return resource


# def check_recipe(recipe, recipe_str="resource.recipe"):
#     Struct.Dict(recipe, recipe_str)

#     KEYS = {
#         "ah": Struct.Int,
#         "aw": Struct.Int,
#         "rh": Struct.Int,
#         "rw": Struct.Int,
#         "asoect_ratio": Struct.Int,
#         "height": Struct.Int,
#         "width": Struct.Int,
#         "modified": Struct.Bool,
#         "crop": check_crop
#     }
#     for key, validation in KEYS.iteritems():
#         try:
#             validation(recipe[key], key)
#         except Exception:
#             raise Exception("recipe error")

#     return recipe


# def check_crop(crop, crop_str="resource.recipe.crop"):
#     Struct.Dict(crop, crop_str)
#     KEYS = {
#         "h": Struct.Int,
#         "w": Struct.Int,
#         "x": Struct.Int,
#         "y": Struct.Int,
#         "ratio": Struct.Int,
#     }
#     for key, validation in KEYS.iteritems():
#         try:
#             validation(crop[key], key)
#         except Exception:
#             raise Exception("crop error")

#     return crop


def output_question(question):
    return {
        "id": question["_id"],
        "title": question["title"],
        "type": question["type"],
        "resources": question["resources"],
        "creation": question["creation"],
        "updated": question["updated"]
    }