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
    generate_store(1000)
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
        ('美食', 'cutlery.png'),
        ('住宿', 'double-bed.png'),
        ('娛樂', 'guitar.png'),
        ('租賃', 'rent-a-car.png'),
        ('購物', 'shopping-bag.png'),
        ('旅遊', 'dumbbell.png'),
        ('刷卡', 'cocktail.png'),
        ('美妝便利店', 'park.png'),
    ]
    for name, icon in names:
        StoreType.objects.create(
            name=name,
            icon=icon,
        )


def generate_county():
    County.objects.create(
        name='高雄市'
    )
    County.objects.create(
        name='台南市'
    )
    County.objects.create(
        name='台北市'
    )


def generate_district():
    countys = County.objects.all()
    for county in countys:
        District.objects.create(
            name='三民區',
            county=county
        )
        District.objects.create(
            name='左營區',
            county=county
        )


def generate_store(count):
    store_type = StoreType.objects.all()
    countys = County.objects.all()
    for i in range(count):
        county = random.choice(countys)
        district = random.choice(District.objects.filter(county=county).all())
        Store.objects.create(
            name=f'商店{i}',
            store_type=random.choice(store_type),
            phone=f'09{get_random_number(8)}',
            website='https://conquers.co/',
            address=f'{county.name}{district.name}6號',
            latitude=f'22.63366{i}7',
            longitude=f'120.29572{i}6',
            county=county,
            district=district,
            status=random.randint(0, 2)
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
        StoreImage.objects.create(
            store=store,
            picture='帳戶資訊.png'
        )


if __name__ == '__main__':
    main()
