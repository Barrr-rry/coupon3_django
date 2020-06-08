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
from fake_data import cn_name, en_name, get_random_letters, get_random_number, banner_args, categories, brands
from run_init import main, test_email


class DefaultTestMixin:
    @classmethod
    def setUpTestData(cls):
        main(for_test=True)
        cls.anonymous_user = APIClient()
        cls.super_manager = cls.init_manager_apiclient(
            role_manage=2,
            member_manage=2,
            order_manage=2,
            banner_manage=2,
            catalog_manage=2,
            product_manage=2,
            coupon_manage=2,
            highest_permission=True,
        )
        member = Member.objects.get(account=test_email)
        token, created = MemberTokens.objects.get_or_create(user=member)
        cls.member_user = APIClient()
        cls.member_user.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
