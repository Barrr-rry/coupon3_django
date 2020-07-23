from run_init import *

import math
from django.db import transaction

"""
db 調整 不需要就可以刪掉了
"""
import random
import re

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from munch import AutoMunch
from google import find_place_id, get_place_info, get_photo
from log import logger

instance = Activity.original_objects.get(name='高雄振興購物嘉年華')
for el in instance.store.all():
    if el.storediscount.count() == 1:
        print('高雄振興購物嘉年華')
        el.search_status = 0
        el.save()

instance = Activity.original_objects.get(name='鐵定貼心')
for el in instance.store.all():
    if el.storediscount.count() == 1:
        print('鐵定貼心')
        el.search_status = 0
        el.save()

instance = Activity.original_objects.get(name='住台南百萬抽大獎')
for el in instance.store.all():
    if el.storediscount.count() == 3:
        print('住台南百萬抽大獎')
        el.search_status = 0
        el.save()

instance = Activity.original_objects.get(name='住宿抽豐田汽車')
for el in instance.store.all():
    if el.storediscount.count() == 1:
        print('住宿抽豐田汽車')
        el.search_status = 0
        el.save()

instance = Activity.original_objects.get(name='安心旅宿 X 雙層觀巴')
for el in instance.store.all():
    if el.storediscount.count() == 1:
        print('安心旅宿 X 雙層觀巴')
        el.search_status = 0
        el.save()

instance = Activity.original_objects.get(name='桃園電子旅遊券')
for el in instance.store.all():
    if el.storediscount.count() == 1:
        print('桃園電子旅遊券')
        el.search_status = 0
        el.save()

instance = Activity.original_objects.get(name='高雄振興國旅方案')
for el in instance.store.all():
    if el.storediscount.count() == 1:
        print('高雄振興國旅方案')
        el.search_status = 0
        el.save()

instance = Activity.original_objects.get(name='安心旅遊補助')
for el in instance.store.all():
    if el.storediscount.count() == 2:
        print('安心旅遊補助')
        el.search_status = 0
        el.save()

print()
