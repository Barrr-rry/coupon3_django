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

with open('./1111_crawlwer.json') as f:
    ret = json.loads(f.read())


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
                                          u"\U0001F600-\U0001F64F"  # emoticons
                                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                          u"\U0001F1E0-\U0001F1FF"
                                          u"\U00002702-\U000027B0"

                                          # u"\U000024C2-\U0001F251"
                                          u"\U0001f926-\U0001f937"
                                          u"\U00010000-\U0010ffff"
                                          "]+", flags = re.UNICODE)
    text = regrex_pattern.sub(r'',text)
    return text


with transaction.atomic():
    discount_type = DiscountType.objects.filter(name__icontains='優惠').first()
    district_dct = dict()
    for el in District.objects.all():
        district_dct[el.name] = el

    for rett in ret:
        for key in district_dct:
            if key in rett['store']['address']:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break
        try:
            store = Store.objects.create(
                name=rett['store']['name'],
                phone=rett['store']['phone'],
                address=rett['store']['address'],
                website=rett['store']['website'],
                latitude=rett['store'].get('latitude', None),
                longitude=rett['store'].get('longitude', None),
                store_type_id=rett['store']['store_type'],
                google_status=rett['store']['google_status'],
                google_name=rett['store']['google_name'],
                county_id=county_id,
                district_id=district_id,
            )
            rett['storediscount']['description'] = deEmojify(rett['storediscount']['description'])
            StoreDiscount.objects.create(
                store=store,
                name=rett['storediscount']['name'],
                description=rett['storediscount']['description'],
                discount_type=discount_type
            )
            StoreImage.objects.create(
                store=store,
                picture=rett['store_image']['picture']
            )
        except Exception as e:
            print(rett['store']['phone'])


