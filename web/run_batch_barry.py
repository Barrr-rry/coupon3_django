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

stores = Store.objects.filter(address__icontains='高雄市前金區中正四路148號').all()
al = stores.count()
nw = 0
logger_location = logger.bind(name="location")
for store in stores:
    logger.info(f'{round((nw/al)*100, 3)}%')
    place_id = find_place_id(store.name)
    info = get_place_info(place_id)
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    if info:
        try:
            county_id = None
            district_id = None
            for key in district_dct:
                if key in info.get('address', store.address):
                    district_id = district_dct[key].id
                    county_id = district_dct[key].county_id
                    break
            store.google_name = info.get('name', store.name)
            store.address = info.get('address', store.address)
            store.phone = info.get('phone', store.phone)
            store.website = info.get('website', store.website)
            if len(store.website) >= 512:
                store.website = None
            store.latitude = info.get('lat', store.latitude)
            store.longitude = info.get('lon', store.longitude)
            store.county_id = county_id
            store.district_id = district_id
            store.google_status = 1
            store.status = 0
            store.save()

            for photo in info['photos']:
                ref = photo['photo_reference']
                img = get_photo(ref)
                StoreImage.objects.create(
                    store=store,
                    picture=img,
                )
                break
            logger.info(f'suc store_id:{store.id}')
        except Exception as e:
            logger.error(f'fil store_id:{store.id}')
            logger_location.error(f'fal store_id:{store.id}')
            for msg in e.args:
                logger_location.error(f'fal msg:{msg}')
    nw += 1






