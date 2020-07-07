from django.views.generic.base import View, TemplateView
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File, Activity
)
from api import serializers
from api import filters
import json
from crawler import task, reids_wraper
from log import logger
import uuid
import time
from api.util import get_time
import json
from munch import AutoMunch
import re
from django.views.decorators.cache import cache_page
from crawler import reids_wraper
import traceback

city_re = None
site_re = None
road_re = None
road_dict = dict()


class BaseView(TemplateView):
    token = str(uuid.uuid4())

    def get_context_data(self, *args, **kwargs):
        return dict(token=self.token)


class TestView(BaseView):
    template_name = 'test.html'


class IndexView(BaseView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        instances = serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        orders = ['美食', '住宿', '購物', '娛樂旅遊', '其他', '夜市商圈', '連鎖店電商', '刷卡電子支付']
        store_type = []
        for order in orders:
            for instance in instances:
                if instance['name'] == order:
                    store_type.append(instance)
        for store in store_type:
            store['name'] = store['name'].replace('夜市商圈', '夜市<br/>商圈')
            store['name'] = store['name'].replace('連鎖店電商', '連鎖店<br/>電商')
            store['name'] = store['name'].replace('刷卡電子支付', '刷卡<br/>電子支付')
        ret = dict(
            store_type=store_type,
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
        instance = Store.objects.get(pk=kwargs.get('store_id'))
        district_list = serializers.DistrictSerializer(many=True, instance=District.objects.all()).data
        county_list = serializers.CountySerializer(many=True, instance=County.objects.all()).data
        district_list_json = json.dumps(district_list)
        county_list_json = json.dumps(county_list)
        district_list = list(filter(lambda x: x['county'] == instance.county.id, district_list))
        storediscount = serializers.StoreDiscountSerializer(many=True, instance=instance.storediscount.all()).data
        discounttype = serializers.DiscountTypeSerializer(many=True, instance=DiscountType.objects.all()).data
        storeimages = serializers.StoreImageSerializer(many=True, instance=instance.storeimage).data
        ret = dict(
            storediscount=storediscount,
            discounttype=discounttype,
            instance=instance,
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data,
            district_list=district_list,
            county_list=county_list,
            token=self.token,
            district_list_json=district_list_json,
            county_list_json=county_list_json,
            storeimages=storeimages,
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


class ELI5HakkaTourView(BaseView):
    template_name = 'eli5_hakka_tour.html'


class ELI5SportView(BaseView):
    template_name = 'eli5_sport.html'


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
        instance = Store.objects.prefetch_related('storediscount').prefetch_related('storeimage'). \
            select_related('county').prefetch_related('activity'). \
            select_related('district').select_related('store_type').get(pk=kwargs.get('store_id'))
        lat = instance.latitude
        lon = instance.longitude
        google = f'https://www.google.com.tw/maps/search/{lat},+{lon}/@{lat},{lon},17z?hl=zh-TW'
        ret = dict(
            instance=serializers.StoreSerializer(instance=instance).data,
            google=google
        )
        return ret


def distance(x):
    # 更新後目前用不到 但是先把算式留著
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


class StoreView(BaseView):
    template_name = 'store.html'

    def get_all_store_cache(self):
        key = 'store:cache'
        data = reids_wraper.get(key)
        if not data:
            queryset = Store.objects.all()
            data = json.dumps(serializers.StoreSerializer(many=True, instance=queryset).data)
            reids_wraper.set(key, data)
        return data

    def check_re(self):
        global city_re, site_re, road_re, road_dict
        if city_re is None or site_re is None or road_re is None:
            location_data = []
            with open('./location.json') as f:
                location_data = json.loads(f.read())
            city_list = []
            site_list = []
            road_list = []
            for el in location_data:
                raw_data = AutoMunch(el['raw_data'])
                if el['lat'] is None or el['lon'] is None:
                    continue
                if raw_data.city not in city_list:
                    city_list.append(raw_data.city)
                site = raw_data.site_id.replace(raw_data.city, '')
                if raw_data.road not in road_list:
                    road_list.append(raw_data.road)
                    road_dict[raw_data.road] = dict(lat=float(el['lat']), lon=float(el['lon']))

            city_list = []
            for el in County.objects.all():
                city_list.append(el.name)

            site_list = []
            for el in District.objects.all():
                site_list.append(el.name)

            city_re = r"|".join(city_list)
            site_re = r"|".join(site_list)
            road_re = r"|".join(road_list)

    def get_context_data(self, *args, **kwargs):
        try:
            ret = self._get_context_data(*args, **kwargs)
            return ret
        except Exception as ex:
            logger.error(traceback.format_exc())
            logger.error(ex, exc_info=True)

    def _get_context_data(self, *args, **kwargs):
        global city_re, site_re, road_re, road_dict
        self.check_re()
        st = time.time()
        task_spend = 0
        status = self.request.GET.get('status', 1)
        queryset = Store.objects.prefetch_related('storediscount').prefetch_related('storeimage'). \
            prefetch_related('activity').select_related('county'). \
            select_related('district').select_related('store_type').filter(status=status)
        search = self.request.GET.get('search', None)
        activity = self.request.GET.get('activity', None)
        district = self.request.GET.get('district', None)
        county = self.request.GET.get('county', 'all')
        store_type = self.request.GET.get('store_type', None)
        order_by = self.request.GET.get('order_by', None)
        search_status = self.request.GET.get('search_status', 1)
        storediscount_discount_type = self.request.GET.get('storediscount_discount_type', None)
        ids = self.request.GET.get('ids', None)
        logger.info(f'get search: {search}')

        if search:
            search = search.replace('台', '臺')

        # get all county
        county_dct = dict()
        for el in County.objects.all():
            county_dct[el.name] = dict(id=el.id, instance=el)

        msg = search
        keywords = []
        county_instance = None
        district_instance = None
        # 沒有輸入search lat lon 用本身經緯度
        msg_st = time.time()
        lat = None
        lon = None
        msg_2 = msg
        if msg is None or not search:
            # 如果沒有輸入地址取得經緯度的方法
            el = None
            if county and county != 'all':
                el = County.objects.get(pk=county)
            elif district and district != 'all':
                el = District.objects.get(pk=district)
            elif activity:
                el = Activity.objects.get(pk=activity)
                el = el.county.first()
            if el:
                lat = el.latitude
                lon = el.longitude
            else:
                lat = float(self.request.COOKIES.get('lat', 23.8523405))
                lon = float(self.request.COOKIES.get('lon', 120.9009427))
        else:
            if len(msg) > 2:
                msg = msg[:-1]
            for county_name in county_dct:
                county = county_dct[county_name]['instance']
                if county_name[:-1] in msg or msg in county_name[:-1]:
                    msg = msg.replace(county_name, '')
                    keywords.append(county_name)
                    county_instance = county
                    break

            for el in District.objects.all():
                if len(el.name) > 2:
                    if (el.name[:-1] in msg or msg in el.name[:-1]) and '縣' not in msg_2:
                        msg = msg.replace(el.name, '')
                        keywords.append(el.name)
                        district_instance = el
                        break
                else:
                    if (el.name in msg or msg in el.name) and '縣' not in msg_2:
                        msg = msg.replace(el.name, '')
                        keywords.append(el.name)
                        district_instance = el
                        break
            search = " ".join(keywords)
            # 屬於縣市或者區域找經緯度
            if not msg and keywords:
                target_instnace = district_instance if district_instance else county_instance
                lat = target_instnace.latitude
                lon = target_instnace.longitude
            # 自行輸入地址找經緯度
            else:
                # 先試試看map 裡面有沒有
                task_st = time.time()
                lat = None
                lon = None
                # 確定store name
                if lat is None or lon is None:
                    target = Store.objects.filter(name=search).first()
                    if target:
                        lat = target.latitude
                        lon = target.longitude
                        logger.info(f'get map from store: {search}')
                # 確定road
                if lat is None or lon is None:
                    target = re.findall(road_re, search)
                    if target:
                        dct = road_dict[target[0]]
                        lat = dct['lat']
                        lon = dct['lon']
                        logger.info(f'get map from road: {search}')
                # 確定site
                if lat is None or lon is None:
                    target = re.findall(site_re, search)
                    if target:
                        target = District.objects.filter(name=target[0]).first()
                        if target:
                            lat = target.latitude
                            lon = target.longitude
                            logger.info(f'get map from site: {search}')

                # 確定county
                if lat is None or lon is None:
                    target = re.findall(city_re, search)
                    if target:
                        target = County.objects.filter(name=target[0]).first()
                        if target:
                            lat = target.latitude
                            lon = target.longitude
                            logger.info(f'get map from county: {search}')

                # 真的要定位
                if lat is None or lon is None:
                    task_id = task.enqueue_task('get_latlon', search or msg
                                                )
                    gps = None
                    gps_st = time.time()
                    while True:
                        gps_ed = time.time()
                        gps = task.get_task_result(task_id)
                        # 找不到
                        if gps_ed - gps_st > 3:
                            logger.warning(f'not found gps: {search} {msg}')
                            lat = float(self.request.COOKIES.get('lat', 23.8523405))
                            lon = float(self.request.COOKIES.get('lon', 120.9009427))
                            gps = [lat, lon]
                            break
                        if gps:
                            break
                    lat = float(gps[0])
                    lon = float(gps[1])
                    task_ed = time.time()
                    task_spend = task_ed - task_st
                    logger.info(f'get map from selenium: {msg}')

        msg_ed = time.time()

        activity_list = []
        if not keywords and activity:
            el = Activity.objects.get(pk=activity)
            keywords.append(el.county.first().name)
        for keyword in keywords:
            if county_dct.get(keyword):
                el = county_dct[keyword]['instance']
                activity_list = serializers.ActivitySerializer(many=True, instance=el.activity).data

        sort = self.request.GET.get('sort', 'distance')
        # distance \ -distance or down
        if sort == 'new':
            order_by = '-created_at'
        if sort == 'old':
            order_by = 'created_at'
        if store_type in ['7', '8']:
            search_status = 2

        filter_dict = dict([('search', search),
                            ('district', district),
                            ('lat', lat),
                            ('lon', lon),
                            ('search_status', search_status),
                            ('activity', activity),
                            ('status', status),
                            ('sort', sort),
                            ('store_type', store_type),
                            ('order_by', order_by),
                            ('storediscount_discount_type', storediscount_discount_type),
                            ('ids', ids)]
                           )
        if filter_dict['search'] == '':
            filter_dict['search'] = msg_2
        data_st = time.time()
        queryset = filters.filter_query(filter_dict, queryset)
        data = serializers.StoreSerializer(many=True, instance=queryset[:6]).data
        data_ed = time.time()

        storetypes = serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        storetypes.insert(0, dict(id='all', name='全部'))
        district_list = serializers.DistrictSerializer(many=True, instance=District.objects.all()).data
        district_list.insert(0, dict(id='all', name='全部'))

        if not county:
            county = 'all'
        if isinstance(county, County):
            county = county.id

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

        activity_instance = Activity.objects.filter(pk=activity).first()
        activity_name = activity_instance.name if activity_instance else ''
        ret = dict(
            all_store_cache=self.get_all_store_cache(),
            lat=lat,
            lon=lon,
            activity=activity,
            activity_name=activity_name,
            activity_list=activity_list,
            suffix=suffix,
            search=search if search is not None else '',
            data=data[:6],
            json_data=json.dumps(data[:6]),
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
            f'search time: {ed - st} task: {task_spend}  msg: {msg_ed - msg_st} data: {data_ed - data_st}'
        )
        return ret

    def render_to_response(self, context, **response_kwargs):
        ret = super().render_to_response(context, **response_kwargs)

        ret.set_cookie('search-lat', context.get('lat'))
        ret.set_cookie('search-lon', context.get('lon'))
        return ret


class StoreActivityView(StoreView):
    template_name = 'store_activity.html'


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
