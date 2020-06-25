import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
import datetime
import random
import json
import time
from munch import AutoMunch
from crawler import *

fmt = '%Y-%m-%d %H:%M:%S'
test_email = 'max@conquers.co'


def demo():
    from strsimpy.damerau import Damerau
    damerau = Damerau()
    data = []
    with open('./location.json') as f:
        data = json.loads(f.read())
    target = []
    dct = dict()
    for el in data:
        raw_data = AutoMunch(el['raw_data'])
        site_id = raw_data.site_id.replace(raw_data.city, '')
        print(site_id)
        dct[raw_data.road] = el
        dct[f'{raw_data.city}{raw_data.road}'] = el
        dct[f'{raw_data.site_id}{raw_data.road}'] = el
    keys = list(dct.keys())
    results = []
    msg = '高雄市 文昌路3巷10號'
    st = time.time()
    for key in keys:
        results.append((damerau.distance(key, msg), key))
    results = sorted(results, key=lambda x: x[0])
    ed = time.time()
    print(ed - st)
    print()


def main():
    data = []
    with open('./location.json') as f:
        data = json.loads(f.read())
    target = []
    dct = dict()
    for el in data:
        road = el['raw_data']['road']
        if road not in target:
            target.append(road)
        else:
            print(el['raw_data'])
    exit()
    for el in data:
        el = AutoMunch(el)
        raw_data = AutoMunch(el.raw_data)
        loc = f'{raw_data.site_id}{raw_data.road}'
        ret = [el.lat, el.lon]
        task_id = f'get_latlon{loc}'
        print(loc, ret)
        task.set_task_response(task_id, ret)


if __name__ == '__main__':
    demo()
    # main()
