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
from django.views.decorators.csrf import csrf_exempt

# consumer_router = routers.DefaultRouter()
# consumer_router.register(r'', ConsumerViewSet)
#
# consumer_bid_router = routers.DefaultRouter()
# consumer_bid_router.register(r'', Consumer_bidViewSet)
# identify_code_router = routers.DefaultRouter()
# identify_code_router.register(r'', Identify_codeViewSet)
# invite_code_router = routers.DefaultRouter()
# invite_code_router.register(r'', Invite_codeViewSet)
#
# group_router = routers.DefaultRouter()
# hander_router = routers.DefaultRouter()
# hander_router.register(r'', Bid_handerViewSet)
# action_router = routers.DefaultRouter()
# action_router.register(r'', Bid_actionViewSet)
# auction_router = routers.DefaultRouter()
# auction_router.register(r'', Bid_auctionViewSet)
# auction_serverside_router = routers.DefaultRouter()
# auction_serverside_router.register(r'', Bid_auction_serversideViewSet)

# identify_code_serverside_router = routers.DefaultRouter()
# identify_code_serverside_router.register(r'', Identify_code_serversideViewSet)

# identify_code_list = Identify_code_serversideViewSet.as_view({'get': 'list', 'post': 'create'})
# identify_code_detail = Identify_code_serversideViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update',
#                                                                 'put': 'update', 'delete': 'destroy'})
identify_code_serverside_router = routers.DefaultRouter()
identify_code_serverside_router.register(r'', Identify_code_serversideViewSet)


hander_list = Hander_serversideViewSet.as_view({'get': 'list', 'post': 'create'})
hander_detail = Hander_serversideViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update',
                                                                'put': 'update', 'delete': 'destroy'})

auction_list = Auction_serversideViewSet.as_view({'get': 'list', 'post': 'create'})
auction_detail = Auction_serversideViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update',
                                                                'put': 'update', 'delete': 'destroy'})

record_list = Record_serversideViewset.as_view({'get': 'list', 'post': 'create'})
record_detail = Record_serversideViewset.as_view({'get': 'retrieve', 'patch': 'partial_update',
                                                                'put': 'update', 'delete': 'destroy'})





urlpatterns = [
    ##登录
    url('^get_guopaiurl/$', views.get_guopaiurl, name='get_guopaiurl'),
    url('^monitest/$', views.monitest, name='monitest'),
    url('^get_remotetime/$', views.get_remotetime, name='get_remotetime'),
    url('^bid_firstprice/$', views.bid_firstprice, name='bid_firstprice'),
    url('^bid_logout/$', views.bid_logout, name='bid_logout'),
    url('^bid_keeplogin/$', views.bid_keeplogin, name='bid_keeplogin'),
    ##管理操作
    url(r'^ic_manage/$', include(identify_code_serverside_router.urls)),
    #  url(r'^ic_manage/$', identify_code_list),
    # url(r'^ic_manage/(?P<pk>[0-9]+)/', identify_code_detail),
    url(r'^hd_manage/$', hander_list),
    url(r'^hd_manage/(?P<pk>[0-9]+)/', hander_detail),
    url(r'^au_manage/$', auction_list),
    url(r'^au_manage/(?P<pk>[0-9]+)/', auction_detail),
    url(r'^rc_manage/$', record_list),
    url(r'^rc_manage/(?P<pk>[0-9]+)/', record_detail),


    # url('^identify_code_manage/$', include(identify_code_serverside_router.urls)),
    # url('^identify_code_manage', csrf_exempt(Identify_code_serversideViewSet.as_view({'get':'list', 'put': 'update',
    #
    #                     'patch': 'partial_update', 'delete': 'destroy'})),
]
