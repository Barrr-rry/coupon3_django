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

    def get_file(self, instance):
        return instance.file.name
