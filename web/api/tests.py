from rest_framework.test import APITestCase
from .models import *
from . import serializers
from rest_framework.test import APIClient
from django.core.management import call_command
from pprint import pprint
import datetime
import json
from django.db.models import Q
import random
from run_init import main, test_email


class DefaultTestMixin:
    @classmethod
    def setUpTestData(cls):
        main(for_test=True)
        cls.user = APIClient()


class TestCounty(DefaultTestMixin, APITestCase):

    def test_county_list(self):
        url = '/api/county/'
        r = self.user.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.data, list)
        self.assertEqual(set(r.data[0].keys()), {'id', 'name'})


class TestDiscounttype(DefaultTestMixin, APITestCase):

    def test_discounttype_list(self):
        url = '/api/discounttype/'
        r = self.user.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.data, list)
        self.assertEqual(set(r.data[0].keys()), {'id', 'name'})


class TestDistrict(DefaultTestMixin, APITestCase):

    def test_district_list(self):
        url = '/api/district/'
        r = self.user.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.data, list)
        self.assertEqual(set(r.data[0].keys()), {'id', 'name', 'county'})


class TestStore(DefaultTestMixin, APITestCase):

    def test_store_list(self):
        url = '/api/store/'
        r = self.user.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.data, list)
        self.assertEqual(set(r.data[0].keys()),
                         {'id', 'name', 'phone', 'person', 'email', 'website', 'address', 'latitude', 'longitude',
                          'status', 'store_type', 'county', 'district'})

    def test_store_post(self):
        url = '/api/store/'
        data = dict(
            storeimage_data=["test.jpg"],
            storediscount_data=[
                dict(
                    discount_type=1,
                    name='`123',
                    description='`123',
                )
            ],
            name='測試人員',
            phone='0912345678',
            person='contact',
            email='test@gmail.com',
            website='www.test.com',
            address='高雄市',
            latitude='123',
            longitude='123',
            status=1,
            store_type=1,
            county=1,
            district=1
        )
        r = self.user.post(url, data)
        # status 201
        self.assertEqual(r.status_code, 201)
        # response type
        self.assertIsInstance(r.data, dict)


class TestStoretype(DefaultTestMixin, APITestCase):

    def test_storetype_list(self):
        url = '/api/storetype/'
        r = self.user.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.data, list)
        self.assertEqual(set(r.data[0].keys()), {'id', 'name', 'icon'})
