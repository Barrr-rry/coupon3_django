from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework import serializers
import json
import datetime
from rest_framework.validators import UniqueValidator
from django.http.request import QueryDict
# check admin
from django.utils.functional import cached_property
from rest_framework.utils.serializer_helpers import BindingDict
from django.utils import timezone
from .serialierlib import NestedModelSerializer, DefaultModelSerializer, HiddenField, hiddenfield_factory, CommonMeta, \
    PermissionCommonMeta, UserCommonMeta, CreateCommonMeta
import uuid
from django.contrib.auth.hashers import make_password
from django.core import validators
from api.models import Oil
from django.utils.timezone import make_aware

fmt = '%Y-%m-%d %H:%M:%S'
to_datetime = lambda x: make_aware(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M'))


class MemberHiddenField:
    def set_context(self, serializer_field):
        if not isinstance(serializer_field.context['request'].user, Member):
            raise serializers.ValidationError('操作錯誤')
        self.target = serializer_field.context['request'].user

    def __call__(self, *args, **kwargs):
        return self.target


def serializer_factory(cls_name, cls, fds):
    class Meta(cls.Meta):
        fields = fds

    return type(cls_name, (cls,), dict(Meta=Meta))


def response_time(self, instance, key):
    if getattr(instance, key) is None:
        return None
    else:
        return getattr(instance, key).strftime(fmt)


class OilSerializer(DefaultModelSerializer):
    price_level_92 = serializers.SerializerMethodField(help_text='0: 持平 1: 低 2:高')
    price_level_95 = serializers.SerializerMethodField(help_text='0: 持平 1: 低 2:高')
    price_level_98 = serializers.SerializerMethodField(help_text='0: 持平 1: 低 2:高')
    price_level_disel = serializers.SerializerMethodField(help_text='0: 持平 1: 低 2:高')

    class Meta(CreateCommonMeta):
        model = Oil

    def find_monday(self, date):
        # 0~6
        weekday = date.weekday() + 1
        ret = date
        if weekday > 1:
            over_day = weekday - 1
            ret = date - datetime.timedelta(days=over_day)
        return ret

    def find_monday_list(self, instance, count):
        monday_date = self.find_monday(instance.created_at)
        instance_list = []
        for i in range(1, count + 1):
            d = monday_date - datetime.timedelta(days=7 * i)

            start_date = to_datetime(f'{d.year}-{d.month}-{d.day} 00:00')
            end_date = to_datetime(f'{d.year}-{d.month}-{d.day} 23:59')
            instance = Oil.objects.filter(Q(created_at__gte=start_date) & Q(created_at__lte=end_date)).first()
            if instance:
                instance_list.append(instance)
        return instance_list

    def get_price_level_92(self, instance):
        return self.price_level(instance, key='CPC_oil_92', compare='oil_change')

    def get_price_level_95(self, instance):
        return self.price_level(instance, key='CPC_oil_95', compare='oil_change')

    def get_price_level_98(self, instance):
        return self.price_level(instance, key='CPC_oil_98', compare='oil_change')

    def get_price_level_disel(self, instance):
        return self.price_level(instance, key='CPC_diesel_oil', compare='diesel_change')

    def price_level(self, instance, key, compare):
        """
        0: 持平 1: 低 2:高
        """
        instance_list = self.find_monday_list(instance, 4)
        total = 0
        for ins in instance_list:
            total += getattr(ins, key)
        ret = 0
        if not instance_list:
            return ret
        avg = total / len(instance_list)
        try:
            if getattr(instance, key) + getattr(instance, compare) > avg:
                ret = 2
            if getattr(instance, key) + getattr(instance, compare) < avg:
                ret = 1
        except Exception as e:
            pass

        return ret
