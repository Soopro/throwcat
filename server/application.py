# coding=utf-8
from __future__ import absolute_import

import os

from flask import Flask, request, current_app
from redis import ConnectionPool, Redis
from mongokit import Connection as MongodbConn

from logging.handlers import RotatingFileHandler

import traceback
import shutil
import logging

from config import config
from utils.encoders import Encoder
from utils.logs import InfoFilter
from utils.api_utils import make_json_response, make_cors_headers
from apiresps.errors import (NotFound,
                             MethodNotAllowed,
                             UncaughtException)

from services.cdn import qiniu

from services.mail_push import MailQueuePusher
from envs import CONFIG_NAME


__version_info__ = ('0', '1', '2')
__version__ = '.'.join(__version_info__)

__artisan__ = ['Majik', 'Redyyu']


def create_app(config_name="development"):
    config_name = CONFIG_NAME or config_name

    app = Flask(__name__)

    app.version = __version__
    app.artisan = __artisan__

    # config
    app.config.from_object(config[config_name])
    app.debug = app.config.get('DEBUG')
    app.json_encoder = Encoder

    # clear folders
    def clear_folders(*folders):
        for folder in folders:
            if os.path.isdir(folder):
                shutil.rmtree(folder)
                os.makedirs(folder)

    # ensure folders
    def ensure_dirs(*folders):
        for folder in folders:
            if not os.path.isdir(folder):
                os.makedirs(folder)

    ensure_dirs(
        app.config.get('LOG_FOLDER')
    )


    # cdn
    qiniu.init(public_key=app.config.get('CDN_PUBLIC_KEY'),
               private_key=app.config.get('CDN_PRIVATE_KEY'))

    # logging
    if app.config.get("TESTING") is True:
        app.logger.setLevel(logging.FATAL)
    else:
        error_file_handler = RotatingFileHandler(
            app.config.get("LOGGING")["error"]["file"],
            maxBytes=app.config.get("LOGGING_ROTATING_MAX_BYTES"),
            backupCount=app.config.get("LOGGING_ROTATING_BACKUP_COUNT")
        )

        error_file_handler.setLevel(logging.WARNING)
        error_file_handler.setFormatter(
            logging.Formatter(app.config.get('LOGGING')['error']['format'])
        )

        info_filter = InfoFilter(logging.INFO)
        info_handler = RotatingFileHandler(
            app.config.get('LOGGING')['info']['file'],
            maxBytes=app.config.get("LOGGING_ROTATING_MAX_BYTES"),
            backupCount=app.config.get("LOGGING_ROTATING_BACKUP_COUNT")
        )
        info_handler.setLevel(logging.INFO)
        info_handler.addFilter(info_filter)
        info_handler.setFormatter(logging.Formatter(
            app.config.get('LOGGING')['info']['format']
        ))
        app.logger.addHandler(error_file_handler)
        app.logger.addHandler(info_handler)

    # database connections
    rds_pool = ConnectionPool(host=app.config.get("REDIS_HOST"),
                              port=app.config.get("REDIS_PORT"),
                              db=app.config.get("REDIS_DB"))
    rds_conn = Redis(connection_pool=rds_pool)

    mongodb_conn = MongodbConn(
        host=app.config.get("MONGODB_HOST"),
        port=app.config.get("MONGODB_PORT"),
        max_pool_size=app.config.get("MONGODB_MAX_POOL_SIZE")
    )

    mongodb = mongodb_conn[app.config.get("MONGODB_DATABASE")]

    # register mongokit models
    from common_models import (User, Media, Question, Resource)
    mongodb_conn.register([User, Media, Question, Resource])

    # inject database connections to app object
    app.redis = rds_conn
    app.mongodb_conn = mongodb_conn
    app.mongodb = mongodb

    # inject common services
    # app.sa_mod = Analyzer(rds_conn, rds_conn,
    #                       app.config.get("ONLINE_LAST_MINUTES"))

    # mail push
    smtp_server = {
        "server": app.config.get("SMTP_SERVER"),
        "user": app.config.get("SMTP_USERNAME"),
        "password": app.config.get("SMTP_PASSWORD")
    }
    system_mail_from = app.config.get("MAIL_FROM")
    system_mail_enabled = app.config.get("SEND_MAIL")
    app.system_mail_pusher = MailQueuePusher(rds_conn,
                                             smtp_server,
                                             system_mail_from,
                                             system_mail_enabled)

    # register error handlers
    @app.errorhandler(404)
    def app_error_404(error):
        current_app.logger.warn(
            "Error: 404\n{}".format(traceback.format_exc())
        )
        return make_json_response(NotFound())

    @app.errorhandler(405)
    def app_error_405(error):
        current_app.logger.warn(
            "Error: 405\n{}".format(traceback.format_exc())
        )
        return make_json_response(MethodNotAllowed())

    @app.errorhandler(400)
    def app_error_400(error):
        current_app.logger.warn(
            "Error: 400\n{}".format(traceback.format_exc())
        )
        return make_json_response(UncaughtException(repr(error)))

    if app.config.get("TESTING") is not True:
        @app.errorhandler(Exception)
        def app_error_uncaught(error):
            current_app.logger.warn(
                "Uncaught Exception: {}\n{}".format(repr(error),
                                                    traceback.format_exc())
            )
            return make_json_response(UncaughtException(repr(error)))

    # register before request handlers
    @app.before_request
    def app_before_request():
        # cors response
        if request.method == "OPTIONS":
            resp = current_app.make_default_options_response()
            cors_headers = make_cors_headers()
            resp.headers.extend(cors_headers)
            return resp

    # app init handlers
    app.app_init_handlers = dict()

    # app cleanup handlers
    app.app_cleanup_handlers = dict()

    # register blueprints
    from blueprints.user import blueprint as users_module
    app.register_blueprint(users_module, url_prefix="/user")

    from blueprints.media import blueprint as media_module
    app.register_blueprint(media_module, url_prefix="/media")

    from blueprints.question import blueprint as question_module
    app.register_blueprint(question_module, url_prefix="/question")

    from blueprints.verification import blueprint as verification_module
    app.register_blueprint(verification_module, url_prefix="/verification")

    print "-------------------------------------------------------"
    print "Throwcat: {}".format(app.version)
    print "Developers: {}".format(', '.join(app.artisan))
    print "-------------------------------------------------------"

    return app
