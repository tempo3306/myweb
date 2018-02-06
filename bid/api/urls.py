# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/6 9:45
'''
from django.conf.urls import url, include
from rest_framework import routers
from .views import Bid_handerViewSet, Bid_actionViewSet, Bid_auctionViewSet

hander_router =  routers.DefaultRouter()
hander_router.register(r'', Bid_handerViewSet)
action_router =  routers.DefaultRouter()
action_router.register(r'', Bid_actionViewSet)
auction_router =  routers.DefaultRouter()
auction_router.register(r'', Bid_auctionViewSet)


urlpatterns = [
    url('^hander', include(hander_router.urls)),
    url('^action', include(action_router.urls)),
    url('^auction', include(auction_router.urls)),
]