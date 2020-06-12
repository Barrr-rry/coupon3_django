from django.views.generic.base import View, TemplateView
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
)
from api import serializers
from api import filters


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
        ret = dict(
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        )
        return ret


class ContactView(TemplateView):
    template_name = 'contact.html'


class QAView(TemplateView):
    template_name = 'QA.html'


class StoreIdView(TemplateView):
    template_name = 'store_id.html'

    def get_context_data(self, *args, **kwargs):
        instance = Store.objects.get(pk=kwargs.get('store_id'))
        ret = dict(instance=serializers.StoreSerializer(instance=instance).data)
        return ret


class StoreMapView(TemplateView):
    template_name = 'store_map.html'


class StoreView(TemplateView):
    template_name = 'store.html'

    def get_context_data(self, *args, **kwargs):
        queryset = Store.objects.filter(status=1)
        search = self.request.GET.get('search', None)
        district = self.request.GET.get('district', None)
        store_type = self.request.GET.get('store_type', None)
        order_by = self.request.GET.get('order_by', None)
        storediscount_discount_type = self.request.GET.get('storediscount_discount_type', None)
        ids = self.request.GET.get('ids', None)
        filter_dict = dict([('search', search),
                            ('district', district),
                            ('store_type', store_type),
                            ('order_by', order_by),
                            ('storediscount_discount_type', storediscount_discount_type),
                            ('ids', ids)]
                           )
        ret = dict(
            data=serializers.StoreSerializer(many=True, instance=filters.filter_query(filter_dict, queryset)[:6]).data,
            count=filters.filter_query(filter_dict, queryset).count(),
            storetypes=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data,
            district=serializers.DistrictSerializer(many=True, instance=District.objects.all()).data,
            discounttype=serializers.DiscountTypeSerializer(many=True, instance=DiscountType.objects.all()).data,
        )
        return ret
