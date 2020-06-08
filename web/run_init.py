import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from django.contrib.auth.models import User
from api import serializers
from django.utils import timezone
import datetime
import random
from fake_data import cn_name, en_name, get_random_letters, get_random_number
from api.models import Oil
import json
from django.utils.timezone import make_aware
from munch import Munch
from api.cron import get_oil, get_traffic, get_api1, get_api2, get_api3, get_api4, get_api5, get_api6, get_api7

fmt = '%Y-%m-%d %H:%M:%S'
test_email = 'max@conquers.co'


def main(for_test=False, config_data=None):
    none_or_text = lambda x: x if x else None
    to_datetime = lambda x: make_aware(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M'))

    instance = Oil.objects.create(
        CPC_oil_92=16.2,
        CPC_oil_95=17.7,
        CPC_oil_98=19.7,
        CPC_diesel_oil=13.2,
        last_updated_at=to_datetime('2020-05-04 00:00')
    )
    instance.created_at = instance.last_updated_at
    instance.save()
    instance = Oil.objects.create(
        CPC_oil_92=18.2,
        CPC_oil_95=19.7,
        CPC_oil_98=21.7,
        CPC_diesel_oil=15.4,
        last_updated_at=to_datetime('2020-05-11 00:00')
    )
    instance.created_at = instance.last_updated_at
    instance.save()
    instance = Oil.objects.create(
        CPC_oil_92=19.1,
        CPC_oil_95=20.6,
        CPC_oil_98=22.6,
        CPC_diesel_oil=16.3,
        last_updated_at=to_datetime('2020-05-18 00:00')
    )
    instance.created_at = instance.last_updated_at
    instance.save()
    instance = Oil.objects.create(
        CPC_oil_92=19.6,
        CPC_oil_95=21.1,
        CPC_oil_98=23.1,
        CPC_diesel_oil=17.1,
        last_updated_at=to_datetime('2020-05-25 00:00')
    )
    instance.created_at = instance.last_updated_at
    instance.save()
    instance = Oil.objects.create(
        CPC_oil_92=20.6,
        CPC_oil_95=22.1,
        CPC_oil_98=24.1,
        CPC_diesel_oil=18.0,
        last_updated_at=to_datetime('2020-06-01 00:00')
    )
    instance.created_at = instance.last_updated_at
    instance.save()
    get_oil()
    get_traffic()
    get_api1()
    get_api2()
    get_api3()
    get_api4()
    get_api5()
    get_api6()
    get_api7()


if __name__ == '__main__':
    main()
