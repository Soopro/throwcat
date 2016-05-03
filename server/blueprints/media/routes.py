# coding=utf-8
from __future__ import absolute_import

from .controllers import *

urls = [
    ("", list_media, "GET"),
    ("", save_media, "POST"),
    ("/<filename>", get_media, "GET"),
    ("/<filename>", update_media, "PUT"),
    ("/<filename>", delete_media, "DELETE"),
    ("/auth/upload", upload_authorize, "POST"),
]