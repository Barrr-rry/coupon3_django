from run_init import *
import math

"""
將store 新增資料從google place id 抓
"""
import random
import re

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from munch import AutoMunch
from google import find_place_id, get_place_info, get_photo
from log import logger

queryset = Store.objects.all()
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
