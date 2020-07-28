# queryset 查詢的語法
from django.db.models import Q, Sum, Count
from rest_framework import filters
# rest api 文檔用
from rest_framework.compat import coreapi, coreschema
# django timezone
from django.utils import timezone
from django.utils.timezone import make_aware
# import models
from api.models import County, District, Store, StoreType
# 算距離的module
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

or_q = lambda q, other_fn: other_fn if q is None else q | other_fn
and_q = lambda q, other_fn: other_fn if q is None else q & other_fn


def filter_query(filter_dict, queryset):
    """
    給api filter & web.views 裡面共用function 因為都是一樣的query 方式
    """
    q = None
    p = None
    filter_dict['store_type'] = None if filter_dict['store_type'] == 'all' else filter_dict['store_type']
    if filter_dict['store_type'] is not None:
        store_types = filter_dict['store_type'].split(',')
        for store_type in store_types:
            p = or_q(p, Q(store_type=store_type))
        q = and_q(q, p)

    if filter_dict['search'] is not None:
        search = filter_dict['search'].strip().split()
        if len(search) > 1:
            if len(search[0]) > 2:
                search[0] = search[0][:-1]
            if len(search[1]) > 2:
                search[1] = search[1][:-1]
            county = County.objects.filter(name__icontains=search[0]).all()
            district = District.objects.filter(name__icontains=search[1]).all()
            if (county.count() + district.count()) > 0:
                q = and_q(q, Q(district__name__icontains=search[1]))
                q = and_q(q, Q(county__name__icontains=search[0]))

        else:
            for keyword in search:
                if len(keyword) > 2:
                    keyword = keyword[:-1]
                county_1 = County.objects.filter(name__icontains=keyword).all()
                district_1 = District.objects.filter(name__icontains=keyword).all()
                name = Store.objects.filter(name__icontains=keyword).all()
                if (county_1.count() + district_1.count() + name.count()) > 0:
                    q = or_q(q, Q(county__name__icontains=keyword))
                    q = or_q(q, Q(district__name__icontains=keyword))
                    q = or_q(q, Q(name__icontains=keyword))

    if filter_dict['search_status'] is not None and filter_dict.get('activity', None) is None:
        q = and_q(q, Q(search_status=filter_dict['search_status']))

    if filter_dict['status'] is not None:
        q = and_q(q, Q(status=filter_dict['status']))

    filter_dict['district'] = None if filter_dict['district'] == 'all' else filter_dict['district']
    if filter_dict['district'] is not None:
        q = and_q(q, Q(district=filter_dict['district']))

    filter_dict['county'] = None if filter_dict['county'] == 'all' else filter_dict['county']
    if filter_dict['county'] is not None:
        ctys = filter_dict['county'].split(',')
        qcity = None
        for cty in ctys:
            qcity = or_q(qcity, Q(county=cty))
        if qcity:
            q = and_q(q, qcity)

    if filter_dict.get('activity', None) is not None:
        q = and_q(q,
                  (Q(activity=filter_dict['activity']) & (
                          Q(search_status=1) | Q(search_status=0)
                  ))
                  )

    ref_location = Point(filter_dict['lat'], filter_dict['lon'], srid=4326)
    queryset = queryset.annotate(distance=Distance("location", ref_location))
    # 算距離
    if filter_dict['sort']:
        queryset = queryset.order_by(filter_dict['sort'])

    if filter_dict['order_by']:
        queryset = queryset.order_by(filter_dict['order_by'])

    filter_dict['storediscount_discount_type'] = None if filter_dict['storediscount_discount_type'] == 'all' else \
        filter_dict['storediscount_discount_type']
    if filter_dict['storediscount_discount_type'] is not None:
        for storediscount in filter_dict['storediscount_discount_type'].split(','):
            q = or_q(q, Q(storediscount__discount_type=storediscount))

    if filter_dict['ids']:
        ids = filter_dict['ids'].split(',')
        q = and_q(q, Q(id__in=ids))

    if q:
        queryset = queryset.filter(q)
        return queryset
    else:
        return queryset


class StoreFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        filter 資料前 先對資料做初始化
        """
        search = request.query_params.get('search', None)
        keywords = []
        # 針對search 文字做優化
        if search:
            search = search.replace('台', '臺')
            msg = search
            if len(search) > 2:
                search = search[:-1]
            for county in County.objects.all():
                if county.name[:-1] in search or search in county.name[:-1]:
                    keywords.append(county.name)
                    break

            for el in District.objects.all():
                if len(el.name) > 2:
                    if (el.name[:-1] in search or search in el.name[:-1]) and '縣' not in msg:
                        keywords.append(el.name)
                        break
                else:
                    if (el.name in search or search in el.name) and '縣' not in msg:
                        keywords.append(el.name)
                    break
        search = " ".join(keywords)
        # 取得所有需要用到的參數 並且針對參數做優化調整
        status = request.query_params.get('status', 1)
        search_status = request.query_params.get('search_status', 1)
        district = request.query_params.get('district', None)
        county = request.query_params.get('county', None)
        activity = request.query_params.get('activity', None)
        store_type = request.query_params.get('store_type', None)
        order_by = request.query_params.get('order_by', None)
        storediscount_discount_type = request.query_params.get('storediscount_discount_type', None)
        ids = request.query_params.get('ids', None)
        lat = float(request.query_params.get('lng', request.COOKIES.get('search-lat', 23.8523405)))
        lon = float(request.query_params.get('lng', request.COOKIES.get('search-lon', 120.9009427)))

        sort = request.query_params.get('sort', 'distance')
        # distance \ -distance or down
        if sort == 'new':
            order_by = '-created_at'
        if sort == 'old':
            order_by = 'created_at'
        if sort == 'pop':
            order_by = 'pop'
        if sort == '-pop':
            order_by = '-pop'
        if store_type and store_type != 'all':
            store_types = store_type.split(',')
            for store_type_2 in store_types:
                if store_type_2 in ['7', '8', '11', '12']:
                    search_status = 2
        # filter_query 前組成function 需要的格式
        filter_dict = dict([('search', search),
                            ('district', district),
                            ('county', county),
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
        return filter_query(filter_dict, queryset)

    def get_schema_fields(self, view):
        """
        schema 告訴該api filter 可以帶入什麼參數 做查詢
        """
        # list 資料不需要帶參數
        if view.action != 'list':
            return []
        # 以下資料參數 都是上面會用到的參數
        return (
            coreapi.Field(
                name='ids',
                required=False,
                location='query',
                schema=coreschema.Array(
                    title='ids',
                    description='array: ids'
                )
            ),
            coreapi.Field(
                name='order_by',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='order_by',
                    description='str: 排序'
                )
            ),
            coreapi.Field(
                name='search',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='search',
                    description='str: 請輸入Search'
                )
            ),
            coreapi.Field(
                name='search_status',
                required=False,
                location='query',
                schema=coreschema.Number(
                    title='search_status',
                    description='int: 請輸入Search Status'
                )
            ),
            coreapi.Field(
                name='activity',
                required=False,
                location='query',
                schema=coreschema.Number(
                    title='activity',
                    description='int: 活動'
                )
            ),
            coreapi.Field(
                name='district',
                required=False,
                location='query',
                schema=coreschema.Number(
                    title='district',
                    description='int: 行政區'
                )
            ),
            coreapi.Field(
                name='county',
                required=False,
                location='query',
                schema=coreschema.Number(
                    title='county',
                    description='int: 縣市'
                )
            ),
            coreapi.Field(
                name='store_type',
                required=False,
                location='query',
                schema=coreschema.Number(
                    title='store_type',
                    description='int: 店家類型'
                )
            ),
            coreapi.Field(
                name='storediscount_discount_type',
                required=False,
                location='query',
                schema=coreschema.Number(
                    title='storediscount_discount_type',
                    description='int: 店家折扣'
                )
            ),
        )
