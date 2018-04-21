# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/6 9:45
'''

from rest_framework import viewsets, status
from bid.api.serializers import *
from bid.models import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from bid.api.permissions import CanBid
from django.shortcuts import get_object_or_404
import time
from django.contrib.auth import login, authenticate
from tools.tasks import reset_identify_code

class ConsumerViewSet(viewsets.ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    permission_classes = (permissions.IsAuthenticated,)  # permissions.AllowAny  注册设置为这个


class Consumer_softwareViewSet(viewsets.ModelViewSet):
    queryset = Consumer_software.objects.all()
    serializer_class = Consumer_softwareSerializer
    permissions_class = (permissions.IsAuthenticated,)


class Consumer_bidViewSet(viewsets.ModelViewSet):
    queryset = Consumer_bid.objects.all()
    serializer_class = Consumer_bidSerializer
    permissions_class = (permissions.IsAuthenticated,)


class Identify_codeViewSet(viewsets.ModelViewSet):
    queryset = Identify_code.objects.all()
    serializer_class = Identify_codeSerializer
    permissions_class = (permissions.IsAuthenticated,)


class Invite_codeViewSet(viewsets.ModelViewSet):
    queryset = Invite_code.objects.all()
    serializer_class = Invite_codeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class Bid_groupViewSet(viewsets.ModelViewSet):
    queryset = Bid_group.objects.all()
    serializer_class = Bid_groupSerializer
    permission_classes = (permissions.IsAuthenticated,)  # permissions.AllowAny  注册设置为这个


class Bid_handerViewSet(viewsets.ModelViewSet):
    queryset = Bid_hander.objects.all()
    serializer_class = Bid_handerSerializer
    permission_classes = (permissions.IsAuthenticated,)  # permissions.AllowAny  注册设置为这个


class Bid_actionViewSet(viewsets.ModelViewSet):
    queryset = Bid_action.objects.all()
    serializer_class = Bid_actionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('diff', 'ahead_price')


class Bid_auctionViewSet(viewsets.ModelViewSet):
    queryset = Bid_auction.objects.all()  # pk = id
    serializer_class = Bid_auctionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('auction_name', 'ID_number')


##serverside查询
class Bid_auction_serversideViewSet(viewsets.ModelViewSet):
    queryset = Bid_auction.objects.all()
    serializer_class = Bid_auctionSerializer

    ##用GET来实现批量删除
    def list(self, request, **kwargs):
        try:
            deleteorget = request.GET.get('data', None)
            if deleteorget == None:
                auctions = query_auction_by_args(request.GET)
                serializer = Bid_auctionSerializer(auctions['items'], many=True)
                result = dict()
                result['rows'] = serializer.data
                result['total'] = auctions['total']
                return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            else:
                data = json.loads(deleteorget)  ##转json
                auctions = query_auction_by_url(data)
                auctions.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            auction = Bid_auction.objects.get(pk=data['pk'])
            description = data['description']  # 描述来源
            auction_name = data['auction_name']  # 标书姓名
            ID_number = data['ID_number']  # 身份证号
            Bid_number = data['Bid_number']  # 标书号
            Bid_password = data['Bid_password']  # 密码
            status_ = data['status']  # 标书状态  避免重名
            count = data['count']  # 参拍次数
            expired_date = data['expired_date']  # 过期时间
            auction.update(description=description, auction_name=auction_name, ID_number=ID_number,
                           Bid_number=Bid_number, Bid_password=Bid_password, status=status_,
                           count=count, expired_date=expired_date)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def Bid_auction_manage(request):
    """
    Retrieve, update or delete a code snippet. """
    if request.method == 'GET':
        try:
            auctions = query_auction_by_args(request.GET)
            serializer = Bid_auctionSerializer(auctions['items'], many=True)
            result = dict()
            result['rows'] = serializer.data
            result['total'] = auctions['total']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
    elif request.method == 'PUT':
        try:
            data = request.GET
            pk = data.get('id')
            serializer = Bid_auction.objects.get(pk=pk)
            serializer = Bid_auctionSerializer(serializer, data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        try:
            data = request.GET.get('data')
            data = json.loads(data)  ##转json
            auctions = query_auction_by_url(data)
            auctions.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        try:
            data = request.POST
            serializer = Bid_auctionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)



##
@api_view(['GET'])
def get_guopaiurl(request):
    try:
        type = request.GET['type']
        if type == 'identify_code':
            identify_code = request.GET['identify_code']
            identify = get_object_or_404(Identify_code, identify_code=identify_code)
            if identify.can_bid():
                diskid = request.GET['diskid']
                uuuid = identify.uuuid
                # if  uuuid == 'none' or diskid == uuuid:
                if  1:
                    identify.uuuid = diskid
                    identify.save()  #更新uuuid
                    # reset_identify_code(identify_code)   ##异步更新数据库
                    version = request.GET.get('version', None)
                    debug = request.GET.get('debug', None)
                    time1 = time.localtime(time.time())
                    time2 = time.strftime("%Y%m%d", time1)
                    today_date = time2 + "01"
                    url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
                    url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date
                    if identify_code == '123456':
                        res = {'result': 'login success',
                               'url_dianxin': url_dianxin,
                               'url_nodianxin': url_nodianxin}
                        return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
                    else:
                        res = {'result': 'login success',
                               'url_nodianxin': url_dianxin,
                               'url_dianxin': url_nodianxin}
                        return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
                    # else:
                    #     res = {'result': 'wrong version'}
                    #     return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
                else:
                    res = {'result': 'repeat'}
                    return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
            else:
                res = {'result': 'expired date'}
                return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def bid_logout(request):
    try:
        type = request.GET['type']
        if type == 'identify_code':
            identify_code = request.GET['identify_code']
            identify = get_object_or_404(Identify_code, identify_code=identify_code)
            identify.uuuid = 'none'
            identify.save()
            res = {'result': 'logout success'}
            return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def bid_keeplogin(request):
    try:
        type = request.GET['type']
        if type == 'identify_code':
            identify_code = request.GET['identify_code']
            identify = get_object_or_404(Identify_code, identify_code=identify_code)
            diskid = request.GET['diskid']
            uuuid = identify.uuuid
            if diskid == uuuid:
                res = {'result': 'keep success'}
                reset_identify_code(identify_code)  ##异步还原identify_code
                return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
            elif uuuid == 'none':
                identify.uuuid = diskid
                identify.save()
                res = {'result': 'keep success'}
                return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
            else:
                res = {'result': 'keep failure'}
                return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)





# @permission_classes((IsAuthenticated, CanBid))
# @api_view(['GET'])
# def bid_login(request):
#     try:
#         username = request.GET['username']
#         password = request.GET['password']
#         version = request.GET['version']
#         debug = request.GET['debug']
#
#         user = authenticate(username=username, password=password)
#         if user:
#             time1 = time.localtime(time.time())
#             time2 = time.strftime("%Y%m%d", time1)
#             today_date = time2 + "01"
#             url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
#             url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date
#             if version == '5.12s' or debug:
#                 res = {'result': 'login success',
#                        'url_dianxin': url_dianxin,
#                        'url_nodianxin': url_nodianxin}
#                 return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
#             else:
#                 res = {'result': 'wrong version'}
#                 return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
#         else:
#             res = {'result': 'wrong account'}
#             return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)





##返回时间
@api_view(['GET'])
def get_remotetime(request):
    try:
        currenttime = time.time()
        res = {'currenttime': currenttime}
        return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)



#### 电商自动化
@api_view(['GET'])
def create_identify_code(request):
    try:
        pass
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

