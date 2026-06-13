from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.views import AlijahonHomeView, CategoryProductsView, AccountView, AdminMarketView, SorovTemplateView, \
    HavolaTemplateView, StatistikaTemplateView, PayTemplateView, KonkursTemplateView, ReferalTemplateView, \
    SettingsTemplateView, LoginFormView, RegisterView, LogOut, ProductDetailView, StreamCreateView, \
    HavolaDeleteView, district_view, success_accept, WishListView, check_wishlist_status, WishListToggleView
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
    path('login', LoginFormView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogOut.as_view(), name='logout'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('market/<int:pk>', AdminMarketView.as_view(), name='market_category'),
    path('stream', StreamCreateView.as_view(), name='oqim'),
    path('stream/delete/<int:pk>', HavolaDeleteView.as_view(), name='delete'),
    path('district', district_view, name='district'),
    path('success-accept', success_accept, name='success_accept'),

    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('wishlist/toggle/', WishListToggleView.as_view(), name='wish-list-toggle'),
    path('wishlist/check/', check_wishlist_status, name='check-wishlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)