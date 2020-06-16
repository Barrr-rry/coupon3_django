from rest_framework import viewsets
from functools import partial
from functools import wraps
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import \
    (CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_nested import routers
from rest_framework.parsers import MultiPartParser, FormParser
from . import permissions
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .viewlib import (List2RetrieveMixin, NestedViewSetBase)
from collections import OrderedDict
import datetime
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.http import QueryDict
from django.db.models import Q
from rest_framework.compat import coreapi, coreschema, distinct
from rest_framework import exceptions
from rest_framework.pagination import LimitOffsetPagination
import datetime
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from . import docs
from . import filters
from django.db.models import Prefetch
from . import permissions
import json
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
import os
from pyquery import PyQuery as pq
import requests
from log import logger
from rest_framework.schemas import ManualSchema, AutoSchema
from django.utils.decorators import method_decorator
from django.db.models import Q, F
from django.db.models import Max, Min
from collections import defaultdict
import pandas as pd
import uuid
from api.util import pickle_redis, to_datetime
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
)

router = routers.DefaultRouter()
nested_routers = []
orderdct = OrderedDict()


class UpdateCache:
    prefix_key = None

    def update(self, *args, **kwargs):
        self.cache_process()
        return super().update(*args, **kwargs)

    def create(self, *args, **kwargs):
        self.cache_process()
        return super().create(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        self.cache_process()
        return super().destroy(*args, **kwargs)

    def cache_process(self):
        if not self.prefix_key:
            return
        data = pickle_redis.get_data('cache')
        if not data:
            data = dict()
            cache_list = ['coupon', 'product', 'banner', 'caetegory', 'tag', 'price', 'configsetting']
            for key in cache_list:
                data[key] = str(uuid.uuid4())
        else:
            data[self.prefix_key] = str(uuid.uuid4())
        pickle_redis.set_data('cache', data)


class UpdateModelMixin:
    """
    客製化Update 不要有partial_update
    """

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class MyMixin(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin,
              viewsets.GenericViewSet):
    pass


def router_url(url, prefix=None, *args, **kwargs):
    def decorator(cls):
        if not prefix:
            router.register(url, cls, *args, **kwargs)
        else:
            prefix_router = orderdct.get(prefix, router)
            nested_router = routers.NestedDefaultRouter(prefix_router, prefix, lookup=prefix)
            nested_router.register(url, cls, *args, **kwargs)
            orderdct[url] = nested_router
            nested_routers.append(nested_router)

        @wraps(cls)
        def warp(*args, **kwargs):
            return cls(*args, **kwargs)

        return warp

    return decorator


def get_urls():
    urls = router.get_urls()
    for nested_router in nested_routers:
        urls += nested_router.get_urls()
    return urls


@router_url('file')
class FileViewSet(MyMixin):
    queryset = File.objects.all()
    serializer_class = serializers.FileSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = []
    permission_classes = []


@router_url('store')
class StoreViewSet(MyMixin):
    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.StoreFilter,)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = Store.objects.filter(status=1)
        return queryset


@router_url('district')
class DistrictViewSet(MyMixin):
    queryset = District.objects.all()
    serializer_class = serializers.DistrictSerializer


@router_url('discounttype')
class DiscountTypeViewSet(MyMixin):
    queryset = DiscountType.objects.all()
    serializer_class = serializers.DiscountTypeSerializer


@router_url('county')
class CountyViewSet(MyMixin):
    queryset = County.objects.all()
    serializer_class = serializers.CountySerializer


@router_url('storetype')
class StoreTypeViewSet(MyMixin):
    queryset = StoreType.objects.all()
    serializer_class = serializers.StoreTypeSerializer


@router_url('contact', basename='contact')
class ContactView(viewsets.ViewSet):
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "email",
                required=True,
                location="form",
                schema=coreschema.String()
            ),
            coreapi.Field(
                "name",
                required=True,
                location="form",
                schema=coreschema.String()
            ),
            coreapi.Field(
                "phone",
                required=True,
                location="form",
                schema=coreschema.String()
            ),
            coreapi.Field(
                "contact_type",
                required=True,
                location="form",
                schema=coreschema.String()
            ),
            coreapi.Field(
                "content",
                required=True,
                location="form",
                schema=coreschema.String()
            ),
        ],
        description="""
        目前無說明
        """
    )

    def create(self, request, *args, **kwargs):
        from api.mail import send_mail
        email = request.data.get('email')
        name = request.data.get('name')
        phone = request.data.get('phone')
        contact_type = request.data.get('contact_type')
        content = request.data.get('content')
        msg = f'''
        email: {email}
        聯絡人: {name} 手機: {phone}
        類型: {contact_type}
        內容:{content}
        '''
        send_mail('Contact Us', msg)
        return Response(data=dict(msg='ok'))


@router_url('location', basename='location')
class LocationView(viewsets.ViewSet):
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "task_type",
                required=True,
                location="query",
                schema=coreschema.Number()
            ),
            coreapi.Field(
                "msg",
                required=True,
                location="query",
                schema=coreschema.String()
            ),
        ]
    )

    def list(self, request, *args, **kwargs):
        """
        1: get_latlon 2: get_addr
        """
        from crawler import task
        task_type = int(request.query_params.get('task_type'))
        msg = request.query_params.get('msg')
        fn_mapping = {
            1: 'get_latlon',
            2: 'get_addr'
        }
        task_id = task.enqueue_task(fn_mapping[task_type], msg)
        ret = None
        while True:
            ret = task.get_task_result(task_id)
            if ret:
                break
        logger.info(f'loc=> {msg}:{ret}')
        return Response(dict(data=ret))
