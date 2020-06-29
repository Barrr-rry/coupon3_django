from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Store


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['store', '404', 'store/create', 'store_map', 'store/county', 'qa',
                'qa/farming', 'qa/fun', 'qa/tour', 'qa/treble', 'qa/treble-cash',
                'qa/treble-non-cash', 'qa/treble-store', 'eli5/county', 'eli5/farming',
                'eli5/fun', 'eli5/tour', 'eli5/treble', 'eli5/voucher']

    def location(self, item):
        return reversed(item)


class StoreSitemap(Sitemap):

    def items(self):
        return Store.objects.all()
