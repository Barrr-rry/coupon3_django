from django.views.generic.base import View, TemplateView
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
)
from api import serializers
from api import filters
import json
from crawler import task
from log import logger
import uuid
import time
from api.util import get_time


class BaseView(TemplateView):
    token = str(uuid.uuid4())

    def get_context_data(self, *args, **kwargs):
        return dict(token=self.token)


class TestView(BaseView):
    template_name = 'test.html'


class IndexView(BaseView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        ret = dict(
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data,
            token=self.token,
        )
        return ret


class NotFoundView(BaseView):
    template_name = '404.html'


class StoreCreateView(BaseView):
    template_name = 'store_create.html'

    def get_context_data(self, *args, **kwargs):
        district_list = serializers.DistrictSerializer(many=True, instance=District.objects.all()).data
        county_list = serializers.CountySerializer(many=True, instance=County.objects.all()).data
        district_list_json = json.dumps(district_list)
        county_list_json = json.dumps(county_list)
        county_id = county_list[0]['id']
        district_list = list(filter(lambda x: x['county'] == county_id, district_list))
        ret = dict(
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data,
            district_list=district_list,
            county_list=county_list,
            token=self.token,
            district_list_json=district_list_json,
            county_list_json=county_list_json,
        )
        return ret


class StoreUpdateView(BaseView):
    template_name = 'store_update.html'

    def get_context_data(self, *args, **kwargs):
        district_list = serializers.DistrictSerializer(many=True, instance=District.objects.all()).data
        county_list = serializers.CountySerializer(many=True, instance=County.objects.all()).data
        district_list_json = json.dumps(district_list)
        county_list_json = json.dumps(county_list)
        county_id = county_list[0]['id']
        district_list = list(filter(lambda x: x['county'] == county_id, district_list))
        ret = dict(
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data,
            district_list=district_list,
            county_list=county_list,
            token=self.token,
            district_list_json=district_list_json,
            county_list_json=county_list_json,
        )
        return ret


class ContactView(BaseView):
    template_name = 'contact.html'


class ELI5View(BaseView):
    template_name = 'eli5.html'


class ELI5CountyView(BaseView):
    template_name = 'eli5_county.html'


class ELI5FarmingView(BaseView):
    template_name = 'eli5_farming.html'


class ELI5FunView(BaseView):
    template_name = 'eli5_fun.html'


class ELI5TourView(BaseView):
    template_name = 'eli5_tour.html'


class ELI5TrebleView(BaseView):
    template_name = 'eli5_treble.html'


class ELI5VoucherView(BaseView):
    template_name = 'eli5_voucher.html'


class QAView(BaseView):
    template_name = 'QA.html'


class QAFarmingView(BaseView):
    template_name = 'QA_farming.html'


class QAFunView(BaseView):
    template_name = 'QA_fun.html'


class QATourView(BaseView):
    template_name = 'QA_tour.html'


class QATrebleView(BaseView):
    template_name = 'QA_treble.html'


class QATrebleCashView(BaseView):
    template_name = 'QA_treble_cash.html'


class QATrebleNonCashView(BaseView):
    template_name = 'QA_treble_noncash.html'


class QAVTrebleStoreiew(BaseView):
    template_name = 'QA_treble_store.html'


class StoreIdView(BaseView):
    template_name = 'store_id.html'

    def get_context_data(self, *args, **kwargs):
        instance = Store.objects.get(pk=kwargs.get('store_id'))
        ret = dict(instance=serializers.StoreSerializer(instance=instance).data,
                   token=self.token, )
        lat = instance.latitude
        lon = instance.longitude
        google = f'https://www.google.com.tw/maps/search/{lat},+{lon}/@{lat},{lon},17z?hl=zh-TW'
        ret = dict(
            instance=serializers.StoreSerializer(instance=instance).data,
            google=google
        )
        return ret


class StoreView(BaseView):
    template_name = 'store.html'

    def get_context_data(self, *args, **kwargs):
        st = time.time()
        task_spend = 0
        queryset = Store.objects.prefetch_related('storediscount').prefetch_related('storeimage'). \
            select_related('county'). \
            select_related('district').select_related('store_type').filter(status=1)
        search = self.request.GET.get('search', None)
        district = self.request.GET.get('district', None)
        county = self.request.GET.get('county', 'all')
        store_type = self.request.GET.get('store_type', None)
        order_by = self.request.GET.get('order_by', None)
        storediscount_discount_type = self.request.GET.get('storediscount_discount_type', None)
        ids = self.request.GET.get('ids', None)
        logger.info(f'get search: {search}')

        if search:
            search = search.replace('台', '臺')

        msg = search
        keywords = []
        county_instance = None
        district_instance = None
        # 沒有輸入search lat lon 用本身經緯度
        msg_st = time.time()
        if msg is None or not search:
            lat = float(self.request.COOKIES.get('lat', 23.8523405))
            lon = float(self.request.COOKIES.get('lon', 120.9009427))
        else:

            for el in County.objects.all():
                if el.name in msg:
                    msg = msg.replace(el.name, '')
                    keywords.append(el.name)
                    county_instance = el
                    break

            for el in District.objects.all():
                if el.name in msg:
                    msg = msg.replace(el.name, '')
                    keywords.append(el.name)
                    district_instance = el
                    break

            # 縣市或者區域
            if not msg and keywords:
                search = " ".join(keywords)
                target_instnace = district_instance if district_instance else county_instance
                lat = target_instnace.latitude
                lon = target_instnace.longitude
            else:
                task_st = time.time()
                task_id = task.enqueue_task('get_latlon', search)
                gps = None
                while True:
                    gps = task.get_task_result(task_id)
                    if gps:
                        break
                lat = float(gps[0])
                lon = float(gps[1])
                task_ed = time.time()
                task_spend = task_ed - task_st
        msg_ed = time.time()

        sort = self.request.GET.get('sort', 'distance')
        if sort == 'new':
            order_by = '-created_at'
        if sort == 'old':
            order_by = 'created_at'

        filter_dict = dict([('search', search),
                            ('district', district),
                            ('county', county),
                            ('store_type', store_type),
                            ('order_by', order_by),
                            ('storediscount_discount_type', storediscount_discount_type),
                            ('ids', ids)]
                           )
        queryset = filters.filter_query(filter_dict, queryset)
        if sort == 'new':
            queryset = queryset.order_by('-created_at')
        if sort == 'old':
            queryset = queryset.order_by('created_at')

        storetypes = serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        storetypes.insert(0, dict(id='all', name='全部'))
        district_list = serializers.DistrictSerializer(many=True, instance=District.objects.all()).data
        district_list.insert(0, dict(id='all', name='全部'))
        data_st = time.time()
        data = serializers.StoreSerializer(many=True, instance=queryset).data
        data_ed = time.time()

        if not county:
            county = 'all'

        def distance(x):
            nlat = x['latitude']
            nlon = x['longitude']
            ret = (abs(nlat - lat) ** 2 + abs(nlon - lon) ** 2) ** (1 / 2)
            x['distance'] = ret
            m = ret / 0.00001
            if m > 1000:
                m = str(round(m / 1000, 1)) + '公里'
            else:
                m = str(round(m)) + '公尺'
            x['distance_name'] = m
            return ret

        sort_st = time.time()
        data = sorted(data, key=distance)
        if sort == 'distance':
            data = sorted(data, key=distance)
        if sort == '-distance':
            data = sorted(data, key=distance, reverse=True)
        sort_ed = time.time()
        json_data = json.dumps(data)
        if storediscount_discount_type is not None:
            dtype = storediscount_discount_type.split(',')
        else:
            dtype = []
        if storediscount_discount_type != 'all':
            dtype = list(map(int, dtype))

        split_list = self.request.build_absolute_uri().split('?')
        suffix = ''
        if len(split_list) > 1:
            suffix = f'?{split_list[-1]}'

        ret = dict(
            suffix=suffix,
            search=search if search is not None else '',
            data=data[:6],
            json_data=json_data,
            count=queryset.count(),
            storetypes=storetypes,
            district=district,
            county=county,
            sort=sort,
            store_type=store_type,
            district_list=district_list,
            len_storediscount_discount_type=len(dtype),
            storediscount_discount_type=dtype,
            discounttype=serializers.DiscountTypeSerializer(many=True, instance=DiscountType.objects.all()).data,
            token=self.token,
        )
        ed = time.time()
        logger.info(
            f'search time: {ed - st} task: {task_spend} sort: {sort_ed - sort_st} msg: {msg_ed - msg_st} data: {data_ed - data_st}'
        )
        return ret


class StoreMapView(StoreView):
    template_name = 'store_map.html'


class StoreCountyView(BaseView):
    template_name = 'store_county.html'

    def get_context_data(self, *args, **kwargs):
        queryset = County.objects.all()
        data = serializers.CountySerializer(many=True, instance=queryset).data
        storetypes = serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        storetypes.insert(0, dict(id='all', name='全部'))
        ret = dict(
            data=data,
            token=self.token,
            storetypes=storetypes,
        )
        return ret
