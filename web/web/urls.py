"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .documentation import include_docs_urls
from api.views import get_urls, webhook
from api import views
from django.conf import settings
from django.conf.urls.static import static
from api import docs
from .views import *
from django.views.generic.base import RedirectView
from django.views.decorators.cache import cache_page
import os
from api.sitemaps import StaticViewSitemap, StoreSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from . import views
from django.views.generic import TemplateView

DEBUG = os.environ.get('ENV') != 'prod'


def get_view(cls):
    if DEBUG:
        return cls.as_view()
    else:
        # return cache_page(60 * 60)(cls.as_view())
        return cls.as_view()


sitemaps = {
    'static': StaticViewSitemap,
    'store': StoreSitemap
}

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='media/shorticon_48.svg')),
    path('api/', include(get_urls())),
    path("webhook/", webhook, name="webhook"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('backend/conquers/admin/', admin.site.urls),
    path('', get_view(IndexView)),
    path('404/', NotFoundView.as_view(), name='404'),
    path('store/create/', StoreCreateView.as_view(), name='store/create'),
    path('contact/', get_view(ContactView), name='contact'),
    path('store/<int:store_id>/', get_view(StoreIdView)),
    path('store/<int:store_id>/update/', StoreUpdateView.as_view()),
    path('store_map/', get_view(StoreMapView), name='store_map'),
    path('store_activity/', get_view(StoreActivityView), name='store_activity'),
    path('store/', get_view(StoreView), name='store'),
    path('store/county/', get_view(StoreCountyView), name='store/county'),
    path('test/', get_view(TestView)),
    path('qa/', get_view(QAView), name='qa'),
    path('qa/farming/', get_view(QAFarmingView), name='qa/farming'),
    path('qa/fun/', get_view(QAFunView), name='qa/fun'),
    path('qa/tour/', get_view(QATourView), name='qa/tour'),
    path('qa/treble/', get_view(QATrebleView), name='qa/treble'),
    path('qa/treble-cash/', get_view(QATrebleCashView), name='qa/treble-cash'),
    path('qa/treble-non-cash/', get_view(QATrebleNonCashView), name='qa/treble-non-cash'),
    path('qa/treble-store/', get_view(QAVTrebleStoreiew), name='qa/treble-store'),
    path('eli5/county/', get_view(ELI5CountyView), name='eli5/county'),
    path('eli5/farming/', get_view(ELI5FarmingView), name='eli5/farming'),
    path('eli5/fun/', get_view(ELI5FunView), name='eli5/fun'),
    path('eli5/tour/', get_view(ELI5TourView), name='eli5/tour'),
    path('eli5/treble/', get_view(ELI5TrebleView), name='eli5/treble'),
    path('eli5/voucher/', get_view(ELI5VoucherView), name='eli5/voucher'),
    path('eli5/hakka_tour/', get_view(ELI5HakkaTourView), name='eli5/hakka_tour'),
    path('eli5/sport/', get_view(ELI5SportView), name='eli5/sport'),
    path('blog/', get_view(BlogView), name='blog'),
    path('blog/blog-single/', get_view(BlogSingleView), name='blog-single'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain'), name='ads.txt'),

]

if settings.DEBUG:
    urlpatterns += path('docs/',
                        include_docs_urls(title='RESTFUL API', description=docs.doc_desc, authentication_classes=[])),

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
