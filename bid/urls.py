from django.conf.urls import include,url
from .views import create_bid_action, create_bid_auction, batch_create_action, batch_create_auction, bid_login
from .views import bid_manage

app_name = 'bid'
urlpatterns = [
    url('^create_bid_action/', create_bid_action, name='create_bid_action'),
    url('^create_bid_auction/', create_bid_auction, name='create_bid_auction'),
    url('^batch_create_action/', batch_create_action, name='batch_create_action'),
    url('^batch_create_auction/', batch_create_auction, name='batch_create_auction'),
    url('^bid_login/', bid_login, name='bid_login'),
    url('^bid_manage', bid_manage, name='bid_manage')
]
