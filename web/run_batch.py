import pandas as pd
import numpy as np
import json
from run_init import *
from django.db import transaction, router
from log import logger
from google import find_place_id, get_place_info, get_photo

import re
import pandas as pd
import numpy as np
from google import find_place_id, get_place_info, get_photo
import math
from collections import defaultdict

"""
每一次批次更新資料  用這個
"""

file_name = '市場攤商優惠統計7.16.(對外).xlsx'
excel = pd.ExcelFile(file_name)
targets = defaultdict(str)

for sheet_name in excel.sheet_names:
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    for index, el in df.iterrows():
        # targets.append(dict(
        #     name=el['Name'].strip(),
        #     desc_list=desc_list,
        # ))
        desc = targets[el['市場名稱']]
        if not desc:
            desc = '＊參與商家\n'
        phone_str = ''
        if el['電話']:
            phone_str = f'（電話）{el["電話"]} '
        other = el['其他']
        is_nan = False
        try:
            is_nan = math.isnan(other)
        except Exception as e:
            pass

        if is_nan:
            other = ''
            if el['折數'] != el['其他']:
                other = f'持三倍券消費 {el["折數"]}優待'

        desc += f'（1）{el["店家"]} {phone_str}{other}\n'
        targets[el['市場名稱']] = desc
with transaction.atomic():
    querset = District.objects.all()
    discount_type = DiscountType.objects.filter(name='優惠').first()
    district_dct = dict()

    store_type = StoreType.objects.filter(name='商圈').first()

    for el in querset:
        district_dct[el.name] = el

    for name in targets:
        desc = targets[name]

        place_id = find_place_id(name)
        info = dict(
            address=None,
            phone=None,
            website=None,
            name=None,
            lat=None,
            lon=None,
            photos=[],
        )
        if not place_id:
            logger.warning(f'not found place id: {el.name}')
            info = get_place_info(place_id)
            continue
        addr = info['address']
        print(name, addr)
        lat = None
        lon = None
        find_addr = 1
        if not addr:
            find_addr = 0
            addr = '高雄市前金區中正四路148號'
            lat = 23.8523405
            lon = 120.9009427
        district_id = None
        county_id = None
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break
        else:
            logger.warning(f'not found addr: {addr}')
            continue

        try:
            store = Store.objects.create(
                name=name,
                address=addr,
                store_type=store_type,
                latitude=info['lat'],
                longitude=info['lon'],
                county_id=county_id,
                district_id=district_id,
                phone=info['phone'],
                email=None,
                website=info['website'],
                status=0,
                pop=0,
                google_name=info['name'],
                google_status=1,
            )
            store_discount = StoreDiscount.objects.create(
                store=store,
                discount_type=discount_type,
                description=desc
            )

        except Exception as e:
            logger.warning('store error 不過不管了')
            continue
        try:
            # el.latitude = info['lat']
            # el.longitude = info['lon']
            for photo in info['photos']:
                ref = photo['photo_reference']
                img = get_photo(ref)
                StoreImage.objects.create(
                    store=store,
                    picture=img,
                )
                break
        except Exception as e:
            logger.error(f'fuck dead: {el.name}')

print()
