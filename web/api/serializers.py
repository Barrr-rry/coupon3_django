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
from django.utils.timezone import make_aware
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
)

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


class FileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta(CommonMeta):
        model = File

    def get_filename(self, instance):
        return instance.file.name


class StoreImageSerializer(serializers.ModelSerializer):
    class Meta(CommonMeta):
        model = StoreImage


class StringListField(serializers.ListField):
    child = serializers.CharField()


class DiscountTypeSerializer(DefaultModelSerializer):
    class Meta(CommonMeta):
        model = DiscountType


class StoreDiscountSerializer(serializers.ModelSerializer):
    discount_type = DiscountTypeSerializer(many=False)

    class Meta(CommonMeta):
        model = StoreDiscount


class StoreDiscountWriteSerializer(serializers.ModelSerializer):
    class Meta(CommonMeta):
        model = StoreDiscount
        exclude = [
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted_status',
            'store'
        ]


class StoreSerializer(DefaultModelSerializer):
    storeimage_data = StringListField(required=False, help_text='StoreImage', write_only=True)
    storediscount_data = StoreDiscountWriteSerializer(many=True, required=False, write_only=True,
                                                      help_text='StoreDiscount')
    storediscount = StoreDiscountSerializer(many=True)
    county_name = serializers.CharField(source='county.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    store_type_name = serializers.CharField(source='store_type.name', read_only=True)
    images = serializers.SerializerMethodField()
    storediscount_names = serializers.SerializerMethodField()
    image_1 = serializers.SerializerMethodField()

    class Meta(CommonMeta):
        model = Store

    def get_image_1(self, instance, *args, **kwargs):
        target = instance.storeimage.first()
        return '' if not target else target.picture

    def get_storediscount_names(self, instance, *args, **kwargs):
        names = map(lambda x: x.name, instance.storediscount.all())
        return ", ".join(names)

    def get_images(self, instance, *args, **kwargs):
        ret = []
        for el in instance.storeimage.all():
            ret.append(el.picture)
        return ret

    def create(self, validated_data):
        with transaction.atomic():
            storeimage_data = self.pull_validate_data(validated_data, 'storeimage_data', [])
            storediscount_data = self.pull_validate_data(validated_data, 'storediscount_data', [])
            instance = super().create(validated_data)
            for pic in storeimage_data:
                StoreImage.objects.create(
                    store=instance,
                    picture=pic
                )
            for el in storediscount_data:
                StoreDiscount.objects.create(
                    store=instance,
                    **el
                )
            return instance


class DistrictSerializer(DefaultModelSerializer):
    class Meta(CommonMeta):
        model = District


class CountySerializer(DefaultModelSerializer):
    class Meta(CommonMeta):
        model = County


class StoreTypeSerializer(DefaultModelSerializer):
    class Meta(CommonMeta):
        model = StoreType
