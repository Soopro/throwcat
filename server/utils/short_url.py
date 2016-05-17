# coding=utf-8
from __future__ import absolute_import

from short_url


def random_short_url(length=6, preset_int=None, case_sensitive=False):
    if not preset_int or not isinstance(preset_int, int):
        end = len(short_url.DEFAULT_ALPHABET)**(length-1)
        random_num = random.randint(0, end)
    else:
        random_num = preset_int

    random_str = short_url.encode_url(random_num, length)
    if not case_sensitive:
        random_str = random_str.upper()

    return random_num, random_str


def check_random_short_url(random_num, random_str, case_sensitive=False):
    if not random_num:
        return False
    if not case_sensitive:
        random_str = random_str.lower()
    return random_num == short_url.decode_url(random_str)
