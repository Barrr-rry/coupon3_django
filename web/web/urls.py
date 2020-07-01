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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.urls import path, include
from .documentation import include_docs_urls
from api.views import get_urls
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
from django.views.generic import TemplateView

DEBUG = os.environ.get('ENV') != 'prod'


def get_view(cls):
    if DEBUG:
        return cls.as_view()
    else:
        return cache_page(60 * 60)(cls.as_view())


sitemaps = {
    'static': StaticViewSitemap,
    'store': StoreSitemap
}

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='media/shorticon_48.svg')),
    path('api/', include(get_urls())),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('backend/conquers/admin/', admin.site.urls),
    path('', get_view(IndexView)),
    path('404/', NotFoundView.as_view()),
    path('store/create/', StoreCreateView.as_view()),
    path('contact/', get_view(ContactView)),
    path('store/<int:store_id>/', get_view(StoreIdView)),
    path('store/<int:store_id>/update/', StoreUpdateView.as_view()),
    path('store_map/', get_view(StoreMapView)),
    path('store/', get_view(StoreView)),
    path('store/county/', get_view(StoreCountyView)),
    path('test/', get_view(TestView)),
    path('qa/', get_view(QAView)),
    path('qa/farming/', get_view(QAFarmingView)),
    path('qa/fun/', get_view(QAFunView)),
    path('qa/tour/', get_view(QATourView)),
    path('qa/treble/', get_view(QATrebleView)),
    path('qa/treble-cash/', get_view(QATrebleCashView)),
    path('qa/treble-non-cash/', get_view(QATrebleNonCashView)),
    path('qa/treble-store/', get_view(QAVTrebleStoreiew)),
    path('eli5/county/', get_view(ELI5CountyView)),
    path('eli5/farming/', get_view(ELI5FarmingView)),
    path('eli5/fun/', get_view(ELI5FunView)),
    path('eli5/tour/', get_view(ELI5TourView)),
    path('eli5/treble/', get_view(ELI5TrebleView)),
    path('eli5/voucher/', get_view(ELI5VoucherView)),
    path('eli5/hakka_tour/', get_view(ELI5HakkaTourView)),
    path('eli5/sport/', get_view(ELI5SportView)),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt/', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

]

if settings.DEBUG:
    urlpatterns += path('docs/',
                        include_docs_urls(title='RESTFUL API', description=docs.doc_desc, authentication_classes=[])),

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
