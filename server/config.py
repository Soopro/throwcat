# coding=utf-8
from __future__ import absolute_import

from datetime import timedelta
from utils.misc import DottedImmutableDict
import os


class Config(object):

    # env
    DEBUG = True
    SECRET_KEY = 'throwcat_777'

    # path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DEPLOY_DIR = os.path.join(BASE_DIR, 'deployment_data')
    LOG_FOLDER = os.path.join(DEPLOY_DIR, 'logs')

    # url
    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False
    DENIED_ORIGINS = []

    PROTOCOL = 'http'
    API_DOMAIN = 'sup.local:5000'
    UPLOADS_DOMAIN = '7xqqrw.com1.z0.glb.clouddn.com'

    UPLOADS_URL = '{}://{}'.format(PROTOCOL, UPLOADS_DOMAIN)
    API_URL = '{}://{}'.format(PROTOCOL, API_DOMAIN)

    # default data
    DEFAULT_DATE_FORMAT = '%Y-%m-%d'
    DEFAULT_INPUT_DATE_FORMAT = DEFAULT_DATE_FORMAT
    DEFAULT_LOCALE = u'en'
    DEFAULT_PROTOCOL = u'http'

    # JWT
    JWT_SECRET_KEY = SECRET_KEY  # SECRET_KEY
    JWT_ALGORITHM = 'HS256'
    JWT_VERIFY_EXPIRATION = True,
    JWT_LEEWAY = 0
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600 * 24 * 30)
    JWT_AUTH_HEADER_KEY = 'Authorization'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'
    # JWT_AUTH_URL_RULE = '/api/user/login'

    # Reset Password
    RESET_PWD_EXPIRATION = 3600 * 1

    # OAUTH2
    OAUTH_CODE_EXPIRATION = 60 * 10
    OAUTH_TOKEN_EXPIRATION = 3600 * 24 * 2
    OAUTH_RATE_LIMIT = 100
    OAUTH_RATE_EXPIRATION = 3600 * 24 * 1
    OAUTH_INVALID_TOKEN_PREFIX = 'invalid_oauth_token:'
    OAUTH_INVALID_CODE_PREFIX = 'invalid_oauth_code:'

    # invalid user for redis
    INVALID_USER_TOKEN_PREFIX = 'invalid_user_token:'
    INVALID_MEMBER_TOKEN_PREFIX = 'invalid_member_token:'

    # rate limit
    RATE_LIMIT_PREFIX = 'rate_limit:'

    # invalid remote addr
    INVALID_REMOTE_ADDR_PREFIX = 'invalid-remote_addr:'
    INVALID_REMOTE_ADDR_LIMIT = 100
    INVALID_REMOTE_ADDR_EXPIRATION = 3600 * 24 * 7

    # logging
    LOGGING = {
        'error': {
            'format': '%(asctime)s %(levelname)s: %(message)s' +
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "supmice_error.log")
        },
        'info': {
            'format': '%(asctime)s %(levelname)s: %(message)s' +
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "supmice_info.log")
        }
    }

    LOGGING_ROTATING_MAX_BYTES = 64 * 1024 * 1024
    LOGGING_ROTATING_BACKUP_COUNT = 5

    # DATABASES
    MONGODB_HOST_ENV = 'localhost'
    if os.environ.get('MONGO_PORT_27017_TCP_ADDR') is not None:
        MONGODB_HOST_ENV = os.environ.get('MONGO_PORT_27017_TCP_ADDR')

    MONGODB_PORT_ENV = 27017
    if os.environ.get('MONGO_PORT_27017_TCP_PORT') is not None:
        MONGODB_PORT_ENV = int(os.environ.get('MONGO_PORT_27017_TCP_PORT'))

    REDIS_HOST_ENV = '127.0.0.1'
    if os.environ.get('REDIS_PORT_6379_TCP_ADDR') is not None:
        REDIS_HOST_ENV = os.environ.get('REDIS_PORT_6379_TCP_ADDR')

    REDIS_PORT_ENV = 6379
    if os.environ.get('REDIS_PORT_6379_TCP_PORT') is not None:
        REDIS_PORT_ENV = int(os.environ.get('REDIS_PORT_6379_TCP_PORT'))

    # mongodb
    MONGODB_HOST = EXT_MONGODB_HOST = MONGODB_HOST_ENV
    MONGODB_PORT = EXT_MONGODB_PORT = MONGODB_PORT_ENV
    MONGODB_MAX_POOL_SIZE = 10
    MONGODB_DATABASE = 'sup_db'

    # redis
    REDIS_URL = "redis://redis"
    REDIS_HOST = REDIS_HOST_ENV
    REDIS_PORT = REDIS_PORT_ENV
    REDIS_DB = 0

    # send mail
    SMTP_SERVER = 'smtp.ym.163.com'
    SMTP_USERNAME = 'notify@supmice.com'
    SMTP_PASSWORD = 'SendMail2015!?'
    MAIL_FROM = "notify@supmice.com"
    # mail from must same as user name for 163 mail sever
    SEND_MAIL = True

    # cdn
    CDN_TIMEOUT = 30
    CDN_CONNECTION_POOL = 10
    CDN_CONNECTION_MAX_POOL = 20
    CDN_CONNECTION_RETRIES = 3
    CDN_UPLOADS_BUCKET = 'throwcat'

    CDN = 'qiniu'
    CDN_ACCOUNT = 'r@supmice.com'
    CDN_PUBLIC_KEY = 'b0cZgsAbLgUuyQivxbfS9WGTXdTo_jZhigSLRsyp'
    CDN_PRIVATE_KEY = 'TvM9XxdeJTAVL6LVhRyOmeBzvoMzYVeRiuR3AJUJ'


class DevelopmentConfig(Config):
    MONGODB_DATABASE = 'throwcat_dev'


class TestCaseConfig(Config):
    TESTING = True
    SEND_MAIL = False
    SECRET_KEY = 'secret'
    MONGODB_DATABASE = 'test'


class ProductionConfig(Config):
    DEBUG = False

    DEPLOY_DIR = '/data/deployment_data'
    LOG_FOLDER = os.path.join(DEPLOY_DIR, "logs")

    PROTOCOL = 'http'
    API_DOMAIN = 'api.soopro.com'
    UPLOADS_DOMAIN = '7xqqrw.com1.z0.glb.clouddn.com'

    UPLOADS_URL = '{}://{}'.format(PROTOCOL, UPLOADS_DOMAIN)
    API_URL = '{}://{}'.format(PROTOCOL, API_DOMAIN)

    MONGODB_DATABASE = 'throwcat_beta'

    # logging
    LOGGING = {
        'error': {
            'format': '%(asctime)s %(levelname)s: %(message)s' +
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "supmice_error.log")
        },
        'info': {
            'format': '%(asctime)s %(levelname)s: %(message)s' +
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "supmice_info.log")
        }
    }

    CDN = 'qiniu'
    CDN_ACCOUNT = 'one@supmice.com'
    CDN_PUBLIC_KEY = 'HJlYHEfL15m4D9LnEf0ey-O4MR2mKMsslk_dS_sy'
    CDN_PRIVATE_KEY = 'KUr_iIlYuHL4QkNGj2c4lFnVHW_rb94YPeMSUzs0'


class TestingConfig(Config):

    DEPLOY_DIR = '/data/deployment_data'
    LOG_FOLDER = os.path.join(DEPLOY_DIR, "logs")

    PROTOCOL = 'http'
    API_DOMAIN = 'api.sup.farm'
    UPLOADS_DOMAIN = '7xqqrw.com1.z0.glb.clouddn.com'

    UPLOADS_URL = '{}://{}'.format(PROTOCOL, UPLOADS_DOMAIN)
    API_URL = '{}://{}'.format(PROTOCOL, API_DOMAIN)

    MONGODB_DATABASE = 'throwcat_beta'

    # logging
    LOGGING = {
        'error': {
            'format': '%(asctime)s %(levelname)s: %(message)s' +
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "supmice_error.log")
        },
        'info': {
            'format': '%(asctime)s %(levelname)s: %(message)s' +
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "supmice_info.log")
        }
    }

    CDN = 'qiniu'
    CDN_ACCOUNT = 'ci@supmice.com'
    CDN_PUBLIC_KEY = 'yDEwEaKnfTbUmkxOgyEEsHt9iWG-IIh4iZoO8iTd'
    CDN_PRIVATE_KEY = 'axASEFK7NNBKv4NxMKd_Uir1k3z6xyyq86vIX8Cl'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    "testcase": TestCaseConfig,
    'default': DevelopmentConfig
}
