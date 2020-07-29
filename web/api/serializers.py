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
from drf_serializer_cache import SerializerCacheMixin
from django.utils.timezone import make_aware
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File, Activity
)
from crawler import task
import re
import time

fmt = '%Y-%m-%d %H:%M:%S'
to_datetime = lambda x: make_aware(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M'))


class FileSerializer(serializers.ModelSerializer):
    # get file name
    filename = serializers.SerializerMethodField()

    class Meta(CommonMeta):
        model = File

    def get_filename(self, instance):
        """
        get file name 得知在media 他可能會被改名字 因為如果重複資料 他會加亂數
        """
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
    desc_safe = serializers.SerializerMethodField()
    desc_edit = serializers.SerializerMethodField()

    class Meta(CommonMeta):
        model = StoreDiscount

    def get_desc_safe(self, instance):
        """
        更新raw desc data 變成前端可以吃得到的html tag
        """
        ret = instance.description
        if not ret:
            return ''
        # 偵測到url 自動加上a tag
        urls = re.findall(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
            ret)
        for url in urls:
            ret = ret.replace(url, f'<a href="{url}">{url}</a>')

        # 更新標題
        replace_data = re.findall('【.+? 】：', ret)
        for raw_text in replace_data:
            replace_text = raw_text.replace('【', '<h5 class="project-title">').replace(' 】：', '</h5>')
            ret = ret.replace(raw_text, replace_text)

        # 更新 * 字樣的文字
        for line in re.findall('＊.+', ret):
            temp = line.strip("\r").strip('＊')
            new_line = f'<p class="dot">{temp}</p>'
            print(new_line)
            ret = ret.replace(line, new_line)

        # 加上 數字li tag
        ret += '\n'
        for line in ret.split('\n'):
            if re.findall(r'（\d+?）', line):
                temp = re.sub(r'（\d+?）', '', line).strip("\r").strip()
                new_line = f'<li>{temp}</li>'
                ret = ret.replace(line + '\n', new_line)
        ret = ret.strip()
        # 判斷所有的li tag 在外層加上ul
        regex = r"(<li>.*?<\/li>)+"
        matches = re.finditer(regex, ret, re.MULTILINE)
        for match in matches:
            ret = ret.replace(match.group(), f'<ul class="num indent">{match.group()}</ul>')
        # ret = ret.replace('\n', '<br/>')
        return ret

    def get_desc_edit(self, instance):
        # 針對 edit 做調整
        ret = instance.description
        if not ret:
            return ''
        return ret.replace('<br>', '\n').replace('<BR>', '\n').strip()


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


class ActivitySerializer(DefaultModelSerializer):
    class Meta:
        model = Activity
        exclude = [
            'created_at',
            'updated_at',
            'deleted_at',
            'deleted_status',
            'store',
            'county'
        ]


class StoreSerializer(SerializerCacheMixin, DefaultModelSerializer):
    storeimage_data = StringListField(required=False, help_text='StoreImage', write_only=True)
    storediscount_data = StoreDiscountWriteSerializer(many=True, required=False, write_only=True,
                                                      help_text='StoreDiscount')
    storediscount = StoreDiscountSerializer(many=True, read_only=True)
    county_name = serializers.CharField(source='county.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    store_type_name = serializers.CharField(source='store_type.name', read_only=True)
    store_type_icon = serializers.CharField(source='store_type.icon', read_only=True)
    images = serializers.SerializerMethodField()
    storediscount_names = serializers.SerializerMethodField()
    image_1 = serializers.SerializerMethodField()
    activity = ActivitySerializer(many=True, required=False)
    phone_2 = serializers.SerializerMethodField(read_only=True)
    distance_name = serializers.SerializerMethodField(read_only=True)

    class Meta(CommonMeta):
        model = Store

    def get_image_1(self, instance, *args, **kwargs):
        """
        判斷有沒有image 沒有就用替代圖
        """
        target = instance.storeimage.first()
        if not target:
            ret = instance.store_type.replace_icon
        else:
            ret = target.picture
        return ret

    def get_distance_name(self, instance, *args, **kwargs):
        """
        更新 距離的文字訊息內容
        看是否會超過公里還是公尺
        """
        if not hasattr(instance, 'distance') or instance.distance is None:
            return ''
        try:
            m = instance.distance * 1000000
        except Exception as e:
            return ''

        if m > 1000:
            m = str(round(m / 1000, 1)) + '公里'
        else:
            m = str(round(m)) + '公尺'
        return m

    def get_phone_2(self, instance, *args, **kwargs):
        """
        phone 格式更改
        """
        phone = instance.phone
        if phone and '#' in phone:
            phone = phone.replace(' #', ',')
        return phone

    def get_storediscount_names(self, instance, *args, **kwargs):
        """
        將所有的折扣訊息 組裝起來給前端
        """
        names = map(lambda x: x.name, instance.storediscount.all())
        names = list(filter(lambda x: x, names))
        if not names:
            return ''
        return ", ".join(names)

    def get_images(self, instance, *args, **kwargs):
        """
        get 所有的store images
        """
        ret = []
        for el in instance.storeimage.all():
            ret.append(el.picture)
        return ret

    def create(self, validated_data):
        """
        overwrite store create 因為有改很多東西 也需要巢狀新增
        """
        # 這個是指 要嘛所有更改全部成功 如果有任何error 就全部不成功
        with transaction.atomic():
            # get store image data
            storeimage_data = self.pull_validate_data(validated_data, 'storeimage_data', [])
            # get store discount data
            storediscount_data = self.pull_validate_data(validated_data, 'storediscount_data', [])
            # 新增 store
            instance = super().create(validated_data)
            if instance.phone and '#' in instance.phone and ' #' not in instance.phone:
                # 修改phone 的格式
                instance.phone = instance.phone.replace('#', ' #')
                instance.save()
            # 新增所有store image
            for pic in storeimage_data:
                StoreImage.objects.create(
                    store=instance,
                    picture=pic
                )
            # 新增所有store discount
            for el in storediscount_data:
                StoreDiscount.objects.create(
                    store=instance,
                    **el
                )
            # 更新gps 位置
            if not (instance.latitude and instance.longitude):
                task_id = task.enqueue_task('get_latlon', instance.address)
                gps = None
                dct = None
                while True:
                    dct = task.get_task_result(task_id)
                    if dct:
                        break
                gps = dct['gps']
                instance.latitude = float(gps[0])
                instance.longitude = float(gps[1])
                instance.save()
            return instance

    def update(self, instance, validated_data):
        """
        overwrite store create 因為有改很多東西 也需要巢狀更改
        """
        # 這個是指 要嘛所有更改全部成功 如果有任何error 就全部不成功
        with transaction.atomic():
            storeimage_data = self.pull_validate_data(validated_data, 'storeimage_data', [])
            storediscount_data = self.pull_validate_data(validated_data, 'storediscount_data', [])
            # 先將舊有的資料刪除
            StoreImage.original_objects.filter(store=instance).delete()
            # 新增新的store image
            for pic in storeimage_data:
                StoreImage.objects.create(
                    store=instance,
                    picture=pic
                )
            # 先將舊有的資料刪除
            StoreDiscount.original_objects.filter(store=instance).delete()
            # 新增新的store discount
            for el in storediscount_data:
                StoreDiscount.objects.create(
                    store=instance,
                    **el
                )
            # 更新store
            try:
                instance = super().update(instance, validated_data)
            except Exception as e:
                print()

            # 更改手機format
            if instance.phone and '#' in instance.phone and ' #' not in instance.phone:
                instance.phone = instance.phone.replace('#', ' #')
                instance.save()
            st_time = time.time()
            lat = None
            lon = None
            # 如果沒有gps 則是更新pgs
            if not (instance.latitude and instance.longitude):
                task_id = task.enqueue_task('get_latlon', instance.address)
                gps = None
                dct = None
                while True:
                    dct = task.get_task_result(task_id)
                    ed_time = time.time()
                    if dct:
                        gps = dct['gps']
                        lat = float(gps[0])
                        lon = float(gps[1])
                        break
                    if ed_time - st_time > 3:
                        # logger.warning(f'not found lat long by task_id: {task_id}')
                        break
                instance.latitude = lat
                instance.longitude = lon
                instance.save()
            return instance


class DistrictSerializer(DefaultModelSerializer):
    class Meta(CommonMeta):
        model = District


class CountySerializer(DefaultModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta(CommonMeta):
        model = County

    def get_count(self, instance, *args, **kwargs):
        """
        store 數量 先filter status = 1 & search_status = 1
        """
        count = Store.objects.filter(county=instance).filter(status=1).filter(search_status=1).count()
        return count


class StoreTypeSerializer(DefaultModelSerializer):
    class Meta(CommonMeta):
        model = StoreType
