# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/6 9:45
'''
from django.conf.urls import url, include
from rest_framework import routers
from .views import *
import bid.api.views as views

consumer_router = routers.DefaultRouter()
consumer_router.register(r'', ConsumerViewSet)
consumer_software_router = routers.DefaultRouter()
consumer_software_router.register(r'', Consumer_softwareViewSet)
consumer_bid_router = routers.DefaultRouter()
consumer_bid_router.register(r'', Consumer_bidViewSet)
identify_code_router = routers.DefaultRouter()
identify_code_router.register(r'', Identify_codeViewSet)
invite_code_router = routers.DefaultRouter()
invite_code_router.register(r'', Invite_codeViewSet)

group_router = routers.DefaultRouter()
group_router.register(r'', Bid_groupViewSet)
hander_router = routers.DefaultRouter()
hander_router.register(r'', Bid_handerViewSet)
action_router = routers.DefaultRouter()
action_router.register(r'', Bid_actionViewSet)
auction_router = routers.DefaultRouter()
auction_router.register(r'', Bid_auctionViewSet)
auction_serverside_router = routers.DefaultRouter()
auction_serverside_router.register(r'', Bid_auction_serversideViewSet)

urlpatterns = [
    url('^consumer', include(consumer_router.urls)),
    url('^consumer_software', include(consumer_software_router.urls)),
    url('^consumer_bid', include(consumer_bid_router.urls)),
    url('^identify_code', include(identify_code_router.urls)),
    url('^invite_code', include(invite_code_router.urls)),

    url('^group', include(group_router.urls)),
    url('^hander', include(hander_router.urls)),
    url('^action', include(action_router.urls)),
    url('^auction', include(auction_router.urls)),
    url('^auction_serverside', include(auction_serverside_router.urls)),
    url('^bid_auction_manage/$', views.Bid_auction_manage, name='api_bid_auction_manage'),
]
