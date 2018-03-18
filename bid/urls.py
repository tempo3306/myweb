from django.conf.urls import include,url
from .views import create_bid_action, create_bid_auction, batch_create_action, batch_create_auction, bid_login
import bid.views as views

app_name = 'bid'
urlpatterns = [
    url('^create_bid_action/', create_bid_action, name='create_bid_action'),
    url('^create_bid_auction/', create_bid_auction, name='create_bid_auction'),
    url('^batch_create_action/', batch_create_action, name='batch_create_action'),
    url('^batch_create_auction/', batch_create_auction, name='batch_create_auction'),
    url('^bid_login/', bid_login, name='bid_login'),
    url('^manage_bid_auction', views.manage_bid_auction, name='manage_bid_auction'),
    url('^manage_bid_action', views.manage_bid_action, name='manage_bid_action'),
    url('^manage_bid_hander', views.manage_bid_hander, name='manage_bid_hander'),
    url(r'^bid_auction_manage/$', views.Bid_auction_manage, name='Bid_auction_manage'),
    url(r'^bid_action_manage/$', views.Bid_action_manage, name='Bid_action_manage'),
]
