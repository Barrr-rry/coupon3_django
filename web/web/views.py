from django.views.generic.base import View, TemplateView
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
)
from api import serializers
from api import filters
import json
from crawler import task
from log import logger


class TestView(TemplateView):
    template_name = 'test.html'


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        ret = dict(
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        )
        return ret


class NotFoundView(TemplateView):
    template_name = '404.html'


class StoreCreateView(TemplateView):
    template_name = 'store_create.html'

    def get_context_data(self, *args, **kwargs):
        district_list = serializers.DistrictSerializer(many=True, instance=District.objects.all()).data
        county_list = serializers.CountySerializer(many=True, instance=County.objects.all()).data
        ret = dict(
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data,
            district_list=district_list,
            county_list=county_list,
        )
        return ret


class ContactView(TemplateView):
    template_name = 'contact.html'


class ELI5View(TemplateView):
    template_name = 'eli5.html'


class QAView(TemplateView):
    template_name = 'QA.html'


class StoreIdView(TemplateView):
    template_name = 'store_id.html'

    def get_context_data(self, *args, **kwargs):
        instance = Store.objects.get(pk=kwargs.get('store_id'))
        ret = dict(instance=serializers.StoreSerializer(instance=instance).data)
        return ret


class StoreView(TemplateView):
    template_name = 'store.html'

    def get_context_data(self, *args, **kwargs):
        queryset = Store.objects.filter(status=1)
        search = self.request.GET.get('search', None)
        district = self.request.GET.get('district', None)
        county = self.request.GET.get('county', 'all')
        store_type = self.request.GET.get('store_type', None)
        order_by = self.request.GET.get('order_by', None)
        storediscount_discount_type = self.request.GET.get('storediscount_discount_type', None)
        ids = self.request.GET.get('ids', None)

        msg = search
        keywords = []
        county_instance = None
        district_instance = None
        # 沒有輸入search lat lon 用本身經緯度
        if msg is None:
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
                task_id = task.enqueue_task('get_latlon', search)
                gps = None
                while True:
                    gps = task.get_task_result(task_id)
                    if gps:
                        break
                logger.info(f'loc=> {search}:{gps}')
                lat = float(gps[0])
                lon = float(gps[1])

        filter_dict = dict([('search', search),
                            ('district', district),
                            ('county', county),
                            ('store_type', store_type),
                            ('order_by', order_by),
                            ('storediscount_discount_type', storediscount_discount_type),
                            ('ids', ids)]
                           )
        sort = self.request.GET.get('sort', 'distance')
        queryset = filters.filter_query(filter_dict, queryset)
        if sort == 'new':
            queryset = queryset.order_by('-created_at')
        if sort == 'old':
            queryset = queryset.order_by('created_at')

        storetypes = serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        storetypes.insert(0, dict(id='all', name='全部'))
        district_list = serializers.DistrictSerializer(many=True, instance=District.objects.all()).data
        district_list.insert(0, dict(id='all', name='全部'))
        data = serializers.StoreSerializer(many=True, instance=queryset).data

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

        data = sorted(data, key=distance)
        if sort == 'distance':
            data = sorted(data, key=distance)
        if sort == '-distance':
            data = sorted(data, key=distance, reverse=True)

        json_data = json.dumps(data)
        if storediscount_discount_type is not None:
            dtype = storediscount_discount_type.split(',')
        else:
            dtype = []
        if storediscount_discount_type != 'all':
            dtype = list(map(int, dtype))

        ret = dict(
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
        )
        return ret


class StoreMapView(StoreView):
    template_name = 'store_map.html'


class StoreCountyView(TemplateView):
    template_name = 'store_county.html'

    def get_context_data(self, *args, **kwargs):
        queryset = County.objects.all()
        data = serializers.CountySerializer(many=True, instance=queryset).data
        ret = dict(
            data=data,
        )
        return ret
