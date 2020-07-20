from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Store


class StaticViewSitemap(Sitemap):
    """給google 做sitemap"""

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['store',
                '404',
                'store/create',
                'contact',
                'store_map',
                'store/county',
                'qa',
                'qa/farming',
                'qa/fun',
                'qa/tour',
                'qa/treble',
                'qa/treble-cash',
                'qa/treble-non-cash',
                'qa/treble-store',
                'eli5/county',
                'eli5/farming',
                'eli5/fun',
                'eli5/tour',
                'eli5/treble',
                'eli5/voucher',
                'eli5/hakka_tour',
                'eli5/sport',
                'robots.txt',
                'ads.txt']

    def location(self, item):
        return reverse(item)


class StoreSitemap(Sitemap):

    def items(self):
        """只讓他查詢 status=1 的store"""
        return Store.objects.filter(status=1)
