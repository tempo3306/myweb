# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/6 9:45
'''

from rest_framework import viewsets
from .serializers import Bid_actionSerializer, Bid_handerSerializer, Bid_auctionSerializer
from ..models import Bid_action, Bid_auction, Bid_hander
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
import django_filters


class Bid_handerViewSet(viewsets.ModelViewSet):
    queryset = Bid_hander.objects.all()
    serializer_class = Bid_handerSerializer
    permission_classes = (permissions.IsAuthenticated,)  #permissions.AllowAny  注册设置为这个


class Bid_actionViewSet(viewsets.ModelViewSet):
    queryset = Bid_action.objects.all()
    serializer_class = Bid_actionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('diff', 'ahead_price')




class Bid_auctionViewSet(viewsets.ModelViewSet):
    queryset = Bid_auction.objects.all()  #pk = id
    serializer_class = Bid_auctionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('auction_name', 'ID_number')

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
