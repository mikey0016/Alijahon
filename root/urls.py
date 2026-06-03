from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.views import *
from root import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AlijahonHomeView.as_view(), name='home'),
    path('shop/<int:pk>', CategoryProductsView.as_view(), name='category'),
    path('shop/', CategoryProductsView.as_view(), name='shop'),
    path('account/', AccountView.as_view(), name='account'),
    path('market/', AdminMarketView.as_view(), name='market'),
    path('request/', SorovTemplateView.as_view(), name='request'),
    path('havolalar/', HavolaTemplateView.as_view(), name='havolalar'),
    path('stats/', StatistikaTemplateView.as_view(), name='stats'),
    path('konkurs/', KonkursTemplateView.as_view(), name='konkurs'),
    path('pay/', PayTemplateView.as_view(), name='pay'),
    path('referal/', ReferalTemplateView.as_view(), name='referal'),
    path('settings/', SettingsTemplateView.as_view(), name='settings'),
    # path('login/', LoginTemplateView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
