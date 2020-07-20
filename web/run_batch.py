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

"""
from https://drive.google.com/file/d/1scKtTo1VERcRJiQB0HAC_jtMRPUorQy9/view
"""

file_name = '2020觀光工廠振興券與活動優惠彙整(對外).xlsx'
excel = pd.ExcelFile(file_name)
targets = []
for sheet_name in excel.sheet_names:
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    for index, el in df.iterrows():
        desc_list = []
        for idx in [1, 2, 3, 4, 5]:
            to_add = True
            try:
                to_add = not math.isnan(el[idx])
            except Exception as e:
                pass

            if to_add:
                desc_list.append(el[idx])

        targets.append(dict(
            name=el['Name'].strip(),
            desc_list=desc_list,
        ))

with transaction.atomic():
    querset = District.objects.all()
    district_dct = dict()

    discount_type = DiscountType.objects.filter(name='優惠').first()
    store_type = StoreType.objects.filter(name='商圈').first()

    for el in querset:
        district_dct[el.name] = el

    for el in targets:
        place_id = find_place_id(el['name'])
        if not place_id:
            logger.warning(f'not found place id: {el.name}')
            continue
        info = get_place_info(place_id)
        addr = info['address']
        print(addr)
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
                name=el['name'],
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
            for desc in el['desc_list']:
                if len(desc) < 100:
                    store_discount = StoreDiscount.objects.create(
                        store=store,
                        discount_type=discount_type,
                        name=desc
                    )
                else:
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

