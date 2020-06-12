from django.db.models import Q, Sum, Count
from rest_framework import filters
from rest_framework.compat import coreapi, coreschema
from django.utils import timezone
from django.utils.timezone import make_aware

or_q = lambda q, other_fn: other_fn if q is None else q | other_fn
and_q = lambda q, other_fn: other_fn if q is None else q & other_fn


def filter_query(filter_dict, queryset):
    q = None
    if filter_dict['search'] is not None:
        for keyword in filter_dict['search'].strip().split():
            q = or_q(q, Q(name__contains=keyword))
            q = or_q(q, Q(storediscount__discount_type__name__contains=keyword))

    filter_dict['district'] = None if filter_dict['district'] == 'all' else filter_dict['district']
    if filter_dict['district'] is not None:
        q = and_q(q, Q(district=filter_dict['district']))

    filter_dict['store_type'] = None if filter_dict['store_type'] == 'all' else filter_dict['store_type']
    if filter_dict['store_type'] is not None:
        q = and_q(q, Q(store_type=filter_dict['store_type']))

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
        return queryset.filter(q)
    else:
        return queryset


class StoreFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search')
        district = request.query_params.get('district', None)
        store_type = request.query_params.get('store_type', None)
        order_by = request.query_params.get('order_by', None)
        storediscount_discount_type = request.query_params.get('storediscount_discount_type', None)
        ids = request.query_params.get('ids', None)
        filter_dict = dict([('search', search),
                            ('district', district),
                            ('store_type', store_type),
                            ('order_by', order_by),
                            ('storediscount_discount_type', storediscount_discount_type),
                            ('ids', ids)]
                           )
        return filter_query(filter_dict, queryset)

    def get_schema_fields(self, view):
        if view.action != 'list':
            return []
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
                name='district',
                required=False,
                location='query',
                schema=coreschema.Number(
                    title='district',
                    description='int: 行政區'
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
