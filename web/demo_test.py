import pandas as pd
import numpy as np
import json
from run_init import *
from django.db import transaction, router
from log import logger
from google import find_place_id, get_place_info, get_photo


def check_none(data):
    return None if data == 'Null' else data


querset = District.objects.all()
district_dct = dict()
for el in querset:
    district_dct[el.name] = el

df = pd.read_csv('csv_data.csv')
df = df.astype(object).replace(np.nan, 'Null')
district_id = None
county_id = None
for index, el in df.iterrows():
    addr = check_none(el['ADDRESS'])
    lat = None
    lon = None
    status = 1
    if not addr:
        addr = '高雄市前金區中正四路148號'
        status = 0
        lat = 23.8523405
        lon = 120.9009427
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
        logger.warning(f"not found store_type: {check_none(el['STORE TYPE ID（中文）'])}")
        continue
    if check_none(el['活動']):
        activity = Activity.objects.filter(name=el['活動']).first()
        if not activity:
            activity = Activity.objects.create(name=el['活動'])
    else:
        activity = None

    store = None
    try:
        store = Store.objects.create(
            name=check_none(el['NAME']),
            address=addr,
            store_type=store_type,
            latitude=lat,
            longitude=lon,
            county_id=county_id,
            district_id=district_id,
            phone=check_none(el['PHONE']),
            email=check_none(el['EMAIL']),
            website=check_none(el['WEBSITE']),
            status=status,
        )
    except Exception as e:
        logger.warning('store error 不過不管了')
        continue

    if activity and not activity.county.filter(id=county_id).first():
        activity.county.add(County.objects.get(pk=county_id))

    for discount_type_name, name, desc in [
        (
                check_none(el['DISCOUNT1 TYPE ID（中文）']),
                check_none(el['DISCOUNT1_NAME']),
                check_none(el['DESCRIPTION1']),
        )
    ]:
        if not discount_type_name:
            continue
        discount_type = DiscountType.objects.filter(name=discount_type_name).first()
        if not discount_type:
            discount_type = DiscountType.objects.create(name=discount_type_name)
            logger.warning(f'not found discount type: {discount_type_name}')
            continue

        StoreDiscount.objects.create(
            store=store,
            discount_type=discount_type,
            name=name,
            description=desc,
        )
    if activity:
        activity.store.add(store)
        activity.save()

    # to google
    el = store
    if status == 0:
        continue
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
        el.status = 0
        el.save()
        logger.error(f'fuck dead: {el.name}')

print(el)
