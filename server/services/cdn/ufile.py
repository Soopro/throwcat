# coding=utf-8
from __future__ import absolute_import

import hmac, hashlib, base64, requests


SIGN_KEYS = ['method', 'md5', 'mimetype', 'date', 'x-headers', 'x-resource']

PROXY_SUFFIX = '.ufile.ucloud.cn'

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


def _response_handler(response):
    if response.status_code not in [200, 204, 206]:
        raise Exception(response.json())
    else:
        return True


def _parse_value(org_value):
    if isinstance(org_value, str):
        return org_value
    elif isinstance(org_value, unicode):
        return org_value.encode('utf-8')
    elif isinstance(org_value, list):
        value = None
        list_value = [v for v in org_value if isinstance(v, dict)]
        for item in list_value:
            item_key = item.keys()[0]
            item_str = '{}:{}'.format(item_key.lower(), item[item_key])
            value = '{}\n{}'.format(value, item_str)
        return value
    else:
        return None


def _str2sign(opts):
    sign = None
    for k in SIGN_KEYS:
        if sign:
            value = _parse_value(opts.get(k, ''))
            if value is not None:
                sign = '{}\n{}'.format(sign, value)
        else:
            value = _parse_value(opts.get(k, ''))
            if value is not None:
                sign = value
    return sign


def get_cdn_requests():
    if not cdn_requests_session:
        _init_get_cdn_requests()
    return cdn_requests_session


def gen_api_url(bucket, key, method = None):
    if method.upper() in ['PUT', 'DELETE']:
        return 'http://{0}{1}/{2}'.format(bucket, PROXY_SUFFIX, key)
    else:
        return 'http://{0}{1}/'.format(bucket, PROXY_SUFFIX)


def gen_sign(sign):
    private_key = config.get('CDN_PRIVATE_KEY')
    sha1 = hmac.new(private_key, sign, hashlib.sha1)
    return base64.standard_b64encode(sha1.digest())


def gen_auth(opts):
    public_key = config.get('CDN_PUBLIC_KEY')
    sign_str = _str2sign(opts)
    return '{0} {1}:{2}'.format('UCloud', public_key, gen_sign(sign_str))



def authorize(method, bucket, key, headers = None, mimetype = None):
    if not isinstance(headers, dict):
        headers = dict()
    x_headers = []
    for k,v in headers.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        elif not isinstance(v, str):
            continue
        if k.startswith('X-UCloud'):
            x_headers.append({k.lower(): v})

    data = {
        "method": method.upper(),
        "md5": headers.get('Content-MD5', ''),
        "mimetype": mimetype or headers.get('Content-Type', ''),
        "date": headers.get('Date', ''),
        "x-resource": "/{0}/{1}".format(bucket, key),
        "x-headers": x_headers
    }

    return gen_auth(data)


def upload(bucket, key, data, mimetype = None, headers = None):
    if not isinstance(headers, dict):
        headers = dict()

    if mimetype is None:
        mimetype = 'application/octet-stream'

    headers['Content-Type'] = mimetype
    headers['Authorization'] = authorize('put', bucket, key, headers, mimetype)
    timeout = config.get('CDN_TIMEOUT')
    url = gen_api_url(bucket, key, 'put')

    cdn_req = get_cdn_requests()
    r = cdn_req.put(url, headers = headers, data = data, timeout = timeout)

    return _response_handler(r)


def delete(bucket, key):
    headers = dict()
    headers['Authorization'] = authorize('delete', bucket, key)
    timeout = config.get('CDN_TIMEOUT')
    url = gen_api_url(bucket, key, 'delete')

    cdn_req = get_cdn_requests()
    r = cdn_req.put(url, headers = headers, timeout = timeout)

    return _response_handler(r)
