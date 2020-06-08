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
from api.models import Oil
from api.serializers import OilSerializer
from api.util import pickle_redis, to_datetime

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


@router_url('oil')
class OilViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Oil.objects.all()
    serializer_class = OilSerializer
    pagination_class = LimitOffsetPagination


@router_url('weather', basename='weather')
class WeatherViewSet(viewsets.ViewSet):
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "lat",
                required=True,
                location="query",
                schema=coreschema.Number()
            ),
            coreapi.Field(
                "lon",
                required=True,
                location="query",
                schema=coreschema.Number()
            ),
            coreapi.Field(
                "city",
                required=True,
                location="query",
                schema=coreschema.String()
            ),
        ],
        description="""
        lat = 22.631505
        lon = 120.296738
        city = '高雄市'
        """
    )

    def list(self, request, *args, **kwargs):
        now = datetime.datetime.now()

        lat = float(request.query_params.get('lat'))
        lon = float(request.query_params.get('lon'))
        city = request.query_params.get('city')
        location_sortd = lambda x: (abs(float(x['lat']) - lat) ** 2 + abs(float(x['lon']) - lon) ** 2) ** (1 / 2)

        def get_element(loc, key, out_key):
            return list(filter(lambda x: x['elementName'] == key, loc['weatherElement']))[0][out_key]

        def get_weather(lat, lon, city):
            weather = dict(
                temp=None,
                maxT=None,
                minT=None,
                weekMaxT=[],
                weekMinT=[],
                weekWx=[],
            )

            def get_future_list(data, day=True):
                ret = []
                key = '06:00' if day else '18:00'
                for el in data:
                    start = to_datetime(el['startTime'][:-3])
                    if start.date() > now.date() and key in el['startTime']:
                        ret.append(el)
                return ret

            key = 'weather_info'
            data1 = pickle_redis.get_data(key)
            location = data1['records']['location']
            location = sorted(location, key=location_sortd)

            for loc in location:
                temp = float(get_element(loc, key='TEMP', out_key='elementValue'))
                maxT = float(get_element(loc, key='D_TX', out_key='elementValue'))
                minT = float(get_element(loc, key='D_TN', out_key='elementValue'))
                if temp and maxT and minT:
                    weather['temp'] = round(temp)
                    weather['maxT'] = round(maxT)
                    weather['minT'] = round(minT)
                    break
            key = 'weather_week'
            data5 = pickle_redis.get_data(key)
            location = data5['records']['locations'][0]['location']
            location = sorted(location, key=location_sortd)

            for loc in location:
                maxt = get_element(loc, key='MaxT', out_key='time')
                maxt = get_future_list(maxt)
                maxt = list(map(lambda x: dict(
                    startTime=x['startTime'],
                    endTime=x['endTime'],
                    value=x['elementValue'][0]['value']
                ), maxt))
                weather['weekMaxT'] = maxt

                mint = get_element(loc, key='MinT', out_key='time')
                mint = get_future_list(mint, day=False)
                mint = list(map(lambda x: dict(
                    startTime=x['startTime'],
                    endTime=x['endTime'],
                    value=x['elementValue'][0]['value']
                ), mint))
                weather['weekMinT'] = mint

                wx = get_element(loc, key='Wx', out_key='time')
                wx = get_future_list(wx)
                wx = list(map(lambda x: dict(
                    startTime=x['startTime'],
                    endTime=x['endTime'],
                    value=x['elementValue'][0]['value']
                ), wx))
                weather['weekWx'] = wx
            return weather

        def get_aqi(lat, lon, city):
            location_sortd = lambda x: (abs(float(x['Latitude']) - lat) ** 2 + abs(
                float(x['Longitude']) - lon) ** 2) ** (1 / 2)
            aqi = {
                "aqi": None,
                "pm25": None,
                "pm10": None,
                "o3": None,
            }
            key = 'weather_aqi'
            data2 = pickle_redis.get_data(key)
            data2 = sorted(data2, key=location_sortd)
            for el in data2:
                if all([el['AQI'], el['PM2.5'], el['PM10'], el['O3']]):
                    aqi['aqi'] = float(el['AQI'])
                    aqi['pm25'] = float(el['PM2.5'])
                    aqi['pm10'] = float(el['PM10'])
                    aqi['o3'] = float(el['O3'])
                    break
            return aqi

        def get_uvi(lat, lon, city):
            key = 'weather_uv'
            data3 = pickle_redis.get_data(key)
            for el in data3:
                latlist = el['WGS84Lat'].split(',')
                lonlist = el['WGS84Lon'].split(',')
                lat = float(latlist[0]) + float(latlist[1]) / 60 + float(latlist[2]) / 3600
                lon = float(lonlist[0]) + float(lonlist[1]) / 60 + float(lonlist[2]) / 3600
                el['lat'] = lat
                el['lon'] = lon

            data3 = sorted(data3, key=location_sortd)
            for el in data3:
                if el['UVI']:
                    return float(el['UVI'])

        def get_rain(lat, lon, city):
            ret = {
                "pop": None,
            }
            key = 'weather_rain_percent'
            data4 = pickle_redis.get_data(key)
            for el in data4['records']['location']:
                if el['locationName'] == city:
                    ret['pop'] = float(get_element(el, key='PoP', out_key='time')[0]['parameter']['parameterName'])
                    break
            return ret

        def get_desc(lat, lon, city):
            key = 'weather_helper'
            data7 = pickle_redis.get_data(key)
            return list(
                map(lambda x: dict(description=x['parameterValue']),
                    data7[city]['cwbopendata']['dataset']['parameterSet']['parameter']))

        data = {
            'weather': get_weather(lat, lon, city),
            'aqi': get_aqi(lat, lon, city),
            'uvi': get_uvi(lat, lon, city),
            'rain': get_rain(lat, lon, city),
            'descriptions': get_desc(lat, lon, city),
        }

        return Response(data=data)
