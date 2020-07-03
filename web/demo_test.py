import pandas as pd
import numpy as np
import json
from run_init import *
from django.db import transaction, router
from log import logger


def check_none(data):
    return None if data == 'Null' else data


with transaction.atomic():
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el

    df = pd.read_csv('csv_data.csv')
    df = df.astype(object).replace(np.nan, 'Null')
    district_id = None
    county_id = None
    for index, el in df.iterrows():
        addr = el['ADDRESS']
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break
        else:
            logger.warning(f'not found addr: {addr}')
            continue
        store_type_name = check_none(el['STORE TYPE ID（中文）'])
        if store_type_name:
            store_type = StoreType.objects.filter(
                name=check_none(el['STORE TYPE ID（中文）'])
            ).first()
        else:
            logger.warning(f"not found tore_type: {check_none(el['STORE TYPE ID（中文）'])}")
            continue

        Store.objects.create(
            name=check_none(el['NAME']),
            address=addr,
            store_type=store_type,
            latitude=None,
            longitude=None,
            county_id=county_id,
            district_id=district_id,
            phone=check_none(el['PHONE']),
            email=check_none(el['EMAIL']),
            website=check_none(el['WEBSITE']),
            status=1,
        )
        raise Exception

print(el)
