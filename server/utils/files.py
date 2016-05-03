import datetime
import zipfile

import os


def unzip(file_path, to_path):
    with zipfile.ZipFile(file_path, "r") as z:
        z.extractall(to_path)


def modification_date(filepath):
    """
    get the standard str format of utc datetime 
    of the given file's last-modified
    """
    if not filepath:
        return ''
    t = os.path.getmtime(filepath)
    return datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')


def modification_timestamp(filepath):
    return os.path.getmtime(filepath)


def zipdir(zipfile_location, source_dir):
    """
    package a directory into a zip file
    :param zipfile_location: the location of output zipfile
    :param source_dir: the direcotry need to be compressed
    :return:
    """
    with zipfile.ZipFile(zipfile_location, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                arcname = os.path.relpath(os.path.join(root, file), source_dir)
                zip.write(os.path.join(root, file), arcname)