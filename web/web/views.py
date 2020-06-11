from django.views.generic.base import View, TemplateView
from api.models import (
    StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, File
)
from api import serializers


class TestView(TemplateView):
    template_name = 'test.html'


class IndexView(TemplateView):
    template_name = 'index.html'


class NotFoundView(TemplateView):
    template_name = '404.html'


class AddlistingView(TemplateView):
    template_name = 'addlisting.html'


class StoreCreateView(TemplateView):
    template_name = 'store_create.html'

    def get_context_data(self, *args, **kwargs):
        ret = dict(
            store_type=serializers.StoreTypeSerializer(many=True, instance=StoreType.objects.all()).data
        )
        return ret


class BlogView(TemplateView):
    template_name = 'blog.html'


class BlogSingleView(TemplateView):
    template_name = 'blog-single.html'


class ComingsoonView(TemplateView):
    template_name = 'comingsoon.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class StoreIdView(TemplateView):
    template_name = 'store_id.html'

    def get_context_data(self, *args, **kwargs):
        instance = Store.objects.get(pk=kwargs.get('store_id'))
        ret = dict(instance=serializers.StoreSerializer(instance=instance).data)
        return ret


class ExploreV1View(TemplateView):
    template_name = 'explore-v1.html'


class ExploreV2View(TemplateView):
    template_name = 'explore-v2.html'


class ExploreV3View(TemplateView):
    template_name = 'explore-v3.html'


class StoreView(TemplateView):
    template_name = 'store.html'


class ExploreV5View(TemplateView):
    template_name = 'explore-v5.html'


class Index2View(TemplateView):
    template_name = 'index2.html'


class IndexCopyView(TemplateView):
    template_name = 'index拷貝.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class PriceView(TemplateView):
    template_name = 'price.html'


class RegisterView(TemplateView):
    template_name = 'register.html'
