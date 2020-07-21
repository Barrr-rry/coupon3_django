from run_init import *
import math

"""
之前抓資料用的 現在不用不到了
"""
import random
import re

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from munch import AutoMunch
from google import find_place_id, get_place_info, get_photo
from log import logger

queryset = Store.objects.filter(google_status=0, county__name__contains='臺南')
for el in queryset:
    try:
        place_id = find_place_id(el.name)
        if not place_id:
            logger.warning(f'not found place id: {el.name}')
            continue
        info = get_place_info(place_id)
        if el.county.name not in info['address'] and el.district.name not in info['address']:
            logger.warning(f'google: {info["address"]} address: {el.address}')
            continue
        el.website = info['website']
        el.phone = info['phone']
        el.google_name = info['name']
        for photo in info['photos']:
            ref = photo['photo_reference']
            img = get_photo(ref)
            StoreImage.objects.create(
                store=el,
                picture=img,
            )
            break
        el.google_status = 1
        el.save()
        logger.info(f'success name:{el.name} google_name:{el.google_name} address:{el.address}')
    except Exception as e:
        logger.error(f'fuck dead: {el.name}')

print()
