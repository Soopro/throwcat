# coding=utf-8
from __future__ import absolute_import

import hmac, hashlib, base64, time, json, requests, urllib


UPLOAD_API = 'http://upload.qiniu.com'
RS_API = 'http://rs.qiniu.com'
RSF_API = 'http://rsf.qbox.me'

DEPRECATED_POLICY_FIELDS = set([
    'asyncOps'
])
POLICY_FIELDS = set([
    'callbackUrl',
    'callbackBody',
    'callbackHost',
    'callbackBodyType',
    'callbackFetchKey',

    'returnUrl',
    'returnBody',

    'endUser',
    'saveKey',
    'insertOnly',

    'detectMime',
    'mimeLimit',
    'fsizeLimit',
    'fsizeMin',

    'persistentOps',
    'persistentNotifyUrl',
    'persistentPipeline',
])


cdn_requests_session = None


config = {
    'CDN_PUBLIC_KEY': None,
    'CDN_PRIVATE_KEY': None,
    'CDN_CONNECTION_POOL': 100,
    'CDN_CONNECTION_MAX_POOL': 100,
    'CDN_CONNECTION_RETRIES': 2,
    'CDN_TIMEOUT': 30,
}

def init(public_key, private_key, conn_pool = 100, max_pool = 100,
                                  retries = 2, timeout = 30):
    config['CDN_PUBLIC_KEY'] = public_key
    config['CDN_PRIVATE_KEY'] = private_key
    config['CDN_CONNECTION_POOL'] = conn_pool
    config['CDN_CONNECTION_MAX_POOL'] = max_pool
    config['CDN_CONNECTION_RETRIES'] = retries
    config['CDN_TIMEOUT'] = timeout


def _init_get_cdn_requests():
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections = config.get('CDN_CONNECTION_POOL', 10),
        pool_maxsize = config.get('CDN_CONNECTION_MAX_POOL', 20),
        max_retries = config.get('CDN_CONNECTION_RETRIES', 2)
    )
    session.mount('http://', adapter)
    global cdn_requests_session
    cdn_requests_session = session


def _copy_policy(policy, to, strict_policy):
    for k, v in policy.items():
        if k in DEPRECATED_POLICY_FIELDS:
            continue
        if not strict_policy or k in POLICY_FIELDS:
            to[k] = v


def _response_handler(response):
    if response.status_code not in [200, 204, 206]:
        raise Exception(response.json())
    else:
        return True


def get_cdn_requests():
    if not cdn_requests_session:
        _init_get_cdn_requests()
    return cdn_requests_session


def get_api_url():
    return UPLOAD_API


def authorize(bucket, key = None, expires = 3600,
                      policy = None, strict_policy = True):

    public_key = config.get('CDN_PUBLIC_KEY')
    private_key = config.get('CDN_PRIVATE_KEY')

    scope = bucket
    if key is not None:
        scope = '{}:{}'.format(bucket, key)

    args = dict(
        scope = scope,
        deadline = int(time.time()) + expires,
        returnBody = '''{
          "name": $(fname),
          "mimetype": $(mimeType),
          "ext": $(ext),
          "size": $(fsize),
          "w": $(imageInfo.width),
          "h": $(imageInfo.height),
          "hash": $(etag),
          "key": $(key)
        }'''
    )
    if policy is not None:
        _copy_policy(policy, args, strict_policy)

    # data
    data = json.dumps(args, separators=(',', ':'))
    data = base64.urlsafe_b64encode(data)

    # private_token
    sha1 = hmac.new(private_key, data, hashlib.sha1)
    private_token = base64.urlsafe_b64encode(sha1.digest())

    return '{0}:{1}:{2}'.format(public_key, private_token, data)


def upload(bucket, key, file, mimetype = None, headers = None):
    fields = dict()
    fields['key'] = key
    fields['token'] = authorize(bucket, key)

    if mimetype is None:
        mimetype = 'application/octet-stream'

    files = {'file': (file['filename'], file['stream'], mimetype)}
    timeout = config.get('CDN_TIMEOUT')
    url = UPLOAD_API

    cdn_req = get_cdn_requests()
    r = cdn_req.post(url, headers = headers, files = files,
                          data = fields, timeout = timeout)

    return _response_handler(r)


def clean(bucket, prefix, batch = True):
    cdn_req = get_cdn_requests()
    timeout = config.get('CDN_TIMEOUT')
    public_key = config.get('CDN_PUBLIC_KEY')
    private_key = config.get('CDN_PRIVATE_KEY')

    # list
    params = {
        "bucket": bucket,
        "prefix": prefix
    }
    params_encoded = urllib.urlencode(params)
    list_url = '{}/{}?{}'.format(RSF_API, 'list', params_encoded)
    list_auth = ManagerAuth(public_key, private_key)

    r = cdn_req.post(list_url, auth = list_auth, timeout = timeout)
    try:
        result = r.json()
        keys = [item.get('key') for item in result.get('items', [])]
    except:
        raise Exception('bad result')

    if not keys:
        return True

    if not batch:
        for key in keys:
            delete(bucket, key)
        return True

    operations = []
    for key in keys:
        res = base64.urlsafe_b64encode('{0}:{1}'.format(bucket, key))
        cmd = '/{}/{}'.format('delete', res)
        operations.append(cmd)

    body = dict(op=operations)
    batch_url = '{}/{}'.format(RS_API, 'batch')
    auth = ManagerAuth(public_key, private_key)
    r = cdn_req.post(batch_url, data = body, auth = auth,
                                timeout = timeout)

    return _response_handler(r)


def delete(bucket, key):
    res = base64.urlsafe_b64encode('{0}:{1}'.format(bucket, key))
    cmd = '{}/{}'.format('delete', res)
    url = '{}/{}'.format(RS_API, cmd)

    timeout = config.get('CDN_TIMEOUT')
    public_key = config.get('CDN_PUBLIC_KEY')
    private_key = config.get('CDN_PRIVATE_KEY')

    auth = ManagerAuth(public_key, private_key)

    cdn_req = get_cdn_requests()
    r = cdn_req.post(url, auth = auth, timeout = timeout)

    return _response_handler(r)



# auth class
from urlparse import urlparse
class ManagerAuth(requests.auth.AuthBase):
    FROM_CONTENT_TYPE = 'application/x-www-form-urlencoded'
    public_key = None
    private_key = None

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def __call__(self, r):
        token = None
        if r.body is not None \
        and r.headers['Content-Type'] == self.FROM_CONTENT_TYPE:
            token = self._authorize(r.url, r.body)
        else:
            token = self._authorize(r.url)
        r.headers['Authorization'] = 'QBox {0}'.format(token)
        return r

    def _authorize(self, url, body = None, content_type = None):
        parsed_url = urlparse(url)
        query = parsed_url.query
        path = parsed_url.path
        data = path
        if query != '':
            data = ''.join([data, '?', query])
        data = ''.join([data, "\n"])

        if body:
            data += body

        sha1 = hmac.new(self.private_key, data, hashlib.sha1)
        private_token = base64.urlsafe_b64encode(sha1.digest())

        return '{0}:{1}'.format(self.public_key, private_token)
