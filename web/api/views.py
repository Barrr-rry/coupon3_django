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
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from PIL import Image

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

    # def create(self, request, *args, **kwargs):
    #     ret = super().create(request, *args, **kwargs)
    #     img_full_name = ret.data['filename']
    #     img_name = img_full_name.replace(f'.{img_full_name.split(".")[-1]}', '')  # 檔名稱
    #     output = img_name + ".webp"  # 輸出檔名稱
    #     im = Image.open(os.path.join('media', img_full_name))  # 讀入檔案
    #     im.save(os.path.join('media', output))  # 儲存
    #     ret.data['filename'] = output
    #     return ret


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

    def filter_queryset(self, queryset):
        if self.action in ['list', 'latlng']:
            for backend in list(self.filter_backends):
                queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    @action(methods=['GET'], detail=False, permission_classes=[], authentication_classes=[])
    def latlng(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(latitude__isnull=False, longitude__isnull=False)
        queryset = queryset[:50]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
        content = request.data.get('content').split('\r\n')
        new_content = ''
        for i in content:
            i += '<br>'
            new_content += i
        msg = f'''
        類型： {contact_type}<br><br>
        姓名： {name}<br><br>
        信箱： {email}<br><br>
        電話： {phone}<br><br>
        內容： <br>{new_content}
        '''
        send_mail(f'【{contact_type}】來自{name}的訊息', msg)
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

    @action(methods=['GET'], detail=False, permission_classes=[], authentication_classes=[])
    def temp(self, request, *args, **kwargs):
        """
                1: get_latlon 2: get_addr
                """
        from crawler import task
        import random
        task_type = int(request.query_params.get('task_type', 1))
        msg = request.query_params.get('msg')
        lat = f'24.{random.randint(100000, 999999)}'
        lon = f'121.{random.randint(100000, 999999)}'
        msg = f'{lat},{lon}'
        fn_mapping = {
            1: 'get_latlon',
            2: 'get_addr'
        }
        task_id = task.enqueue_task(fn_mapping[task_type], msg)
        dct = None
        while True:
            dct = task.get_task_result(task_id)
            if dct:
                break
        return Response(dict(data=dct))

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
        dct = None
        while True:
            dct = task.get_task_result(task_id)
            if dct:
                break
        return Response(dict(data=dct))


from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage, TemplateSendMessage, URIAction, \
    MessageAction, PostbackAction, CarouselColumn, CarouselTemplate

secret = '8207acee5ae83ea617f5a2f6b1e2ad5e'
token = 'Me6okVNBI6dZ1tWLD2krySeisJvtfYwsbS8k2R7GnsrGxYnIWASwPJq8JurNnC/zh7tFN5RhTUjaJ754Hn2so8zUboJQjVm2vifUOI/KwQzs83atLWb/vIMZIaXy0CAFC2PVd5nghZKTY/DaIqUq2wdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(token)
handler = WebhookHandler(secret)

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.http.response import HttpResponse, HttpResponseBadRequest


@csrf_exempt
@require_POST
def webhook(request):
    signature = request.headers["X-Line-Signature"]
    body = request.body.decode()
    logger.info('get webook')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        messages = (
            "Invalid signature. Please check your channel access token/channel secret."
        )
        logger.error(messages)
        return HttpResponseBadRequest(messages)
    return HttpResponse("OK")


def to_column(el):
    text = ''
    n = 0
    for e in el.storediscount.all():
        if n < 3 and e.name:
            text += f'- {e.name}\n'
        n += 1
    image = el.storeimage.first()
    if image:
        url = f'https://3coupon.info/media/{image.picture}'
    else:
        url = f'https://3coupon.info/media/{el.county.name}.jpg'
    logger.warning(f'to col url: {url}')
    name = el.name
    logger.info(f'title: {name} text: {text} url: {url}')
    return CarouselColumn(
        thumbnail_image_url=url,
        title=name,
        text=text,
        actions=[
            URIAction(
                label='test',
                uri=uri
            )
        ]
    )


def get_carouseltemplate(gps=None, store_name=None):
    queryset = Store.objects.filter(status=1).prefetch_related('storeimage')
    columns = []
    if gps:
        ref_location = Point(gps[0], gps[1], srid=4326)
        queryset = queryset.annotate(distance=Distance("location", ref_location))
        queryset = queryset.filter(latitude__isnull=False, longitude__isnull=False)
        queryset = queryset.order_by('distance')
        for el in queryset[:10]:
            columns.append(
                to_column(el)
            )

    if store_name:
        el = queryset.filter(name__icontains=store_name).all()
        if el:
            for ell in el[:10]:
                columns.append(
                    to_column(ell)
                )

    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=columns
        )
    )
    logger.info(f'columens len: {len(columns)} {columns}')
    if len(columns) < 1:
        logger.info(f'line text columen < 1 : store_name: {store_name} gps: {gps}')
        no_store_text = '找不到相關的商家，再重新試試看吧😊\n\n' \
                        '或是試試其他方法：\n\n' \
                        '【１】以 LINE 送出定位點查詢附近商家優惠\n\n' \
                        '【２】輸入店名找商家優惠，如「六福村」\n\n' \
                        '【３】前往網頁好查版：https://3coupon.info/store/county/'
        return TextSendMessage(text=no_store_text)

    return carousel_template_message


@handler.add(event=MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    logger.info(f'line from text: {event.message.text}')
    message = get_carouseltemplate(store_name=event.message.text)
    data = [msg.as_json_dict() for msg in message]
    logger.info(f'last data: {data}')
    import json
    logger.info(f'last data json: {json.dumps(data)}')
    logger.info(f'line from text success: {event.message.text}')
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        # messages=TextSendMessage(text=event.message.text)
        messages=message,
    )


@handler.add(event=MessageEvent, message=LocationMessage)
def handle_message(event: MessageEvent):
    lat = event.message.latitude
    lon = event.message.longitude
    logger.info(f'line from gps: {lat}, {lon}')
    message = get_carouseltemplate(gps=(lat, lon))
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=message,
    )
