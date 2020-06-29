import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from django.contrib.auth.models import User
from api import serializers
from api.models import StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, Activity
from django.utils import timezone
import datetime
import random
from fake_data import cn_name, en_name, get_random_letters, get_random_number
import json
from django.utils.timezone import make_aware
from munch import Munch

fmt = '%Y-%m-%d %H:%M:%S'
test_email = 'max@conquers.co'


def main(for_test=False, config_data=None):
    generate_super_admin()
    generate_stort_type(5)
    generate_county()
    generate_district()
    generate_discount_type(5)
    generate_store()
    # generate_store_discount()
    # generate_store_image()
    generate_activity(5)


def generate_super_admin():
    from django.contrib.auth.models import User

    # create admin
    if not User.objects.first():
        user = User.objects.create_user('admin', password='1111')
        user.is_superuser = True
        user.is_staff = True
        user.save()


def generate_stort_type(count):
    names = [
        ('美食', 'cutlery.svg', 'cutlery_replace.svg'),
        ('住宿', 'double-bed.svg', 'double-bed_replace.svg'),
        ('娛樂', 'guitar.svg', 'guitar_replace.svg'),
        ('租賃', 'rent-a-car.svg', 'rent-a-car_replace.svg'),
        ('購物', 'shopping-bag.svg', 'shopping-bag_replace.svg'),
        ('旅遊', 'dumbbell.svg', 'dumbbell_replace.svg'),
        ('刷卡', 'cocktail.svg', 'cocktail_replace.svg'),
        ('美妝便利店', 'park.svg', 'park_replace.svg'),
        ('其他', 'other.svg', 'other_replace.svg'),
    ]
    for name, icon, replace_icon in names:
        StoreType.objects.create(
            name=name,
            icon=icon,
            replace_icon=replace_icon,
        )


def generate_county():
    county = ''
    with open('./county.txt') as f:
        county = f.read()
    county = county.split('\n')
    for el in county:
        target = el.split(',')
        County.objects.create(
            name=target[0],
            latitude=target[2],
            longitude=target[1],
            picture='景點照片_劍湖山.jpg'

        )


def generate_district():
    location = ''
    with open('./location.txt') as f:
        location = f.read()
    location = location.split('\n')
    for el in location:
        target = el.split(',')
        countys = County.objects.all()
        for county in countys:
            if county.name == target[0][:3]:
                district = target[0][3:]
                District.objects.create(
                    name=district,
                    county=county,
                    latitude=target[2],
                    longitude=target[1]
                )


def get_json(filename):
    import json

    ret = []
    with open(filename) as f:
        return json.loads(f.read())


def set_json(filename, data):
    import json

    ret = []
    with open(filename, 'w') as f:
        f.write(json.dumps(data))


def site1():
    data = get_json('./site1.json')

    store_type = StoreType.objects.all()
    store_dct = dict()
    for el in store_type:
        print(el.id, el.name)
        store_dct[el.name] = el.id
    store_map = {
        '餐飲美食': '美食',
        '流行時尚': '購物',
        '百貨商城': '購物',
        '美妝保養': '美妝便利店',
        '觀光工廠': '旅遊',
        '旅遊休憩': '旅遊',
        '其他': '其他',
        '': '其他',
        '居家生活': '購物',
    }
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.first()
    county_id = None
    district_id = None
    for el in data:
        addr = el['address']
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break
        instance = Store.objects.create(
            name=el['name'],
            address=el['address'],
            store_type_id=store_dct[store_map[el['store_type']]],
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
            phone='02-88615599 #308'
        )
        if el['storediscount']:
            StoreDiscount.objects.create(
                store=instance,
                # todo 假資料
                discount_type=discount_type,
                name=None,
                description=el['storediscount']
            )


def site2():
    data = get_json('./site2.json')

    storetype = StoreType.objects.filter(name='旅遊').first()
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.first()
    county_id = None
    district_id = None
    for el in data:
        addr = el['address']
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break

        instance = Store.objects.create(
            name=el['name'],
            address=el['address'],
            store_type_id=storetype.id,
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
        )


def from_csv():
    data = get_json('./csv.json')

    storetype = StoreType.objects.filter(name='旅遊').first()
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.first()
    county_id = None
    district_id = None
    for el in data:
        addr = el['address']
        if not addr:
            continue
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break

        instance = Store.objects.create(
            name=el['name'],
            address=el['address'],
            store_type_id=el['store_type'],
            person=el['person'],
            email=el['email'],
            website=el['website'],
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
        )
        if el['discountype'] and el['discount_name']:
            StoreDiscount.objects.create(
                store=instance,
                discount_type_id=el['discountype'],
                name=el['discount_name'],
                description=el['description']
            )


def site3():
    data = get_json('./site3.json')

    storetype = StoreType.objects.filter(name='住宿').first()
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.first()
    county_id = None
    district_id = None
    for el in data:
        addr = el['address']
        if not addr:
            continue
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break

        instance = Store.objects.create(
            store_type_id=storetype.id,
            name=el['title'],
            address=el['address'],
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
        )


def generate_store():
    print('store....')
    # site1()
    pass
    # site1()
    # site2()
    # site3()
    # from_csv()


def generate_discount_type(count):
    discount = ['打折',
                '贈品',
                '買就送',
                '滿減',
                '優惠碼',
                '尊享服務',
                '優惠', ]
    for i in discount:
        DiscountType.objects.create(
            name=i,
        )


def generate_activity(count):
    county_query = County.objects.all()
    for county in county_query:
        activity = Activity.objects.create(
            name=f'{county.name}振興嘉年華',
        )
        activity.county.add(county)
        stores = Store.objects.filter(status=1, county=county).all()
        for s in stores:
            if random.choice([True, False]):
                activity.store.add(s)
        activity.save()


def generate_store_discount():
    stores = Store.objects.all()
    discount_types = DiscountType.objects.all()
    for store in stores:
        StoreDiscount.objects.create(
            store=store,
            discount_type=random.choice(discount_types),
            name='折扣標題',
            description='敘述',
        )


def generate_store_image():
    stores = Store.objects.all()
    for store in stores:
        for pic in ['景點_安平古堡.jpg', '景點照片_劍湖山.jpg', '景點照片_台北心潮飯點.jpg',
                    '景點照片_日月潭.jpg', '景點照片_野柳.jpg', '景點照片_金城武樹.jpg']:
            StoreImage.objects.create(
                store=store,
                picture=pic
            )


if __name__ == '__main__':
    main()
