import uuid
import pickle
from django.core.cache import cache
from requests import adapters
import ssl
from urllib3 import poolmanager
import requests
import time
from django.utils.timezone import make_aware
import datetime
from contextlib import contextmanager
"""
此module 要寫爬蟲用的 但這邊用不到
"""


class PickleRedis:
    def __init__(self, r=None):
        self.r = r

    def set_data(self, key, data):
        fkey = f'nuxt:{key}'
        self.r.set(fkey, pickle.dumps(data))

    def remove_data(self, key):
        fkey = f'nuxt:{key}'
        self.r.delete(fkey)

    def get_data(self, key):
        fkey = f'nuxt:{key}'
        data = self.r.get(fkey)
        if data is not None:
            return pickle.loads(data)


pickle_redis = PickleRedis(cache)


class TLSAdapter(adapters.HTTPAdapter):
    """
    這是因為open data 會出現 SSLError
    查詢可以用這個方式解決
    ref: https://github.com/psf/requests/issues/4775
    """

    def init_poolmanager(self, connections, maxsize, block=False, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx)


none_or_text = lambda x: x if x else None
to_datetime = lambda x: make_aware(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M'))
session = requests.session()
session.mount('https://', TLSAdapter())


def get_url(url):
    r = None
    while True:
        try:
            r = session.get(url, timeout=60)
            break
        except Exception as e:
            continue
    return r


@contextmanager
def get_time(logger, msg):
    st = time.time()
    yield
    ed = time.time()
    logger.info(f'{msg}: {ed - st}')
