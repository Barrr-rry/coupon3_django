import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from django.contrib.auth.models import User
from api import serializers
from api.models import StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage
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
    generate_store()
    generate_discount_type(5)
    generate_store_discount()
    generate_store_image()


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
        ('美食', 'cutlery.svg'),
        ('住宿', 'double-bed.svg'),
        ('娛樂', 'guitar.svg'),
        ('租賃', 'rent-a-car.svg'),
        ('購物', 'shopping-bag.svg'),
        ('旅遊', 'dumbbell.svg'),
        ('刷卡', 'cocktail.svg'),
        ('美妝便利店', 'park.svg'),
    ]
    for name, icon in names:
        StoreType.objects.create(
            name=name,
            icon=icon,
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


def generate_store():
    store_type = StoreType.objects.all()
    querset = District.objects.all()
    i = 0
    for el in querset:
        i += 1
        county = el.county
        Store.objects.create(
            name=f'商店{i}',
            store_type=random.choice(store_type),
            phone=f'09{get_random_number(8)}',
            website='https://conquers.co/',
            address=f'{county.name}{el.name}{random.randint(1, 999)}號',
            county=county,
            district=el,
            status=random.randint(0, 2),
            latitude=el.latitude+round(random.uniform(0, 1), 6),
            longitude=el.longitude+round(random.uniform(0, 1), 6),
        )


def generate_discount_type(count):
    for i in range(count):
        DiscountType.objects.create(
            name=f'折扣名稱{i}',
        )


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
