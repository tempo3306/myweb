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
from tools.tasks import reset_identify_code
from tools.utils import init_variable
from tools.utils import random_str
from django.core import serializers

import logging

logger = logging.getLogger(__name__)


class Hander_serversideViewSet(viewsets.ViewSet):
    queryset = Bid_hander.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    #
    def list(self, request):
        try:
            print("fdsfsfsfsfs")
            data = request.query_params
            handers = query_hander_by_args(data)  # 带参数查询
            serializer = Bid_handerSerializer(handers['items'], many=True)
            result = dict()
            result['rows'] = serializer.data
            result['count'] = handers['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def retrieve(self, request, pk=None):
        queryset = Bid_hander.objects.all()
        hander = get_object_or_404(queryset, pk=pk)
        serializer = Bid_handerSerializer(hander)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            hander = Bid_hander.objects.get(pk=pk)
            hander.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            data = request.data
            hander = Bid_hander.objects.get(pk=pk)
            hander_name = data['hander_name']
            basic_salary = data['basic_salary']
            total_income = data['total_income']
            hander.hander_name = hander_name
            hander.basic_salary = basic_salary
            hander.total_income = total_income
            hander.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            data = request.data
            hander = Bid_hander.objects.get(pk=pk)
            hander_name = data['hander_name']
            basic_salary = data['basic_salary']
            total_income = data['total_income']
            hander.hander_name = hander_name
            hander.basic_salary = basic_salary
            hander.total_income = total_income
            hander.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            hander_name = data['hander_name']
            basic_salary = data['basic_salary']
            total_income = data['total_income']
            hander = Bid_hander(hander_name=hander_name, basic_salary=basic_salary, total_income=total_income)
            hander.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Auction_serversideViewSet(viewsets.ViewSet):
    queryset = Bid_hander.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    #
    def list(self, request):
        try:
            data = request.query_params
            ##带available 表示 是创建激活码 SELECT下拉表单所用
            available = data.get('available', None)
            if not available or available == '0':
                auctions = query_auction_by_args(data)  # 带参数查询
                serializer = Bid_auctionSerializer(auctions['items'], many=True)
                result = dict()
                result['rows'] = serializer.data
                print(auctions)
                result['count'] = auctions['count']
                return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            else:
                auctions = query_available_auction()
                serializer = Bid_auctionAvailableSerializer(auctions['items'], many=True)
                result = serializer.data
                return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def retrieve(self, request, pk=None):
        queryset = Bid_auction.objects.all()
        auction = get_object_or_404(queryset, pk=pk)
        serializer = Bid_auctionSerializer(auction)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            auction = Bid_auction.objects.get(pk=pk)
            auction.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            auction = Bid_auction.objects.get(pk=pk)
            serializer = Bid_auctionSerializer(auction, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            auction = Bid_auction.objects.get(pk=pk)
            serializer = Bid_auctionSerializer(auction, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = Bid_auctionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print(serializer.error_messages)
                print(serializer.errors)
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAdmin]
    #     return [permission() for permission in permission_classes]


class Action_serversideViewSet(viewsets.ViewSet):
    queryset = Bid_hander.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    #
    def list(self, request):
        try:
            data = request.query_params
            auctions = query_auction_by_args(data)  # 带参数查询
            serializer = Bid_auctionSerializer(auctions['items'], many=True)
            result = dict()
            result['rows'] = serializer.data
            result['count'] = auctions['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def retrieve(self, request, pk=None):
        queryset = Bid_auction.objects.all()
        auction = get_object_or_404(queryset, pk=pk)
        serializer = Bid_auctionSerializer(auction)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            auction = Bid_auction.objects.get(pk=pk)
            auction.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            data = request.data
            auction = Bid_auction.objects.get(pk=pk)
            auction_name = data['auction_name']
            basic_salary = data['basic_salary']
            total_income = data['total_income']
            auction.auction_name = auction_name
            auction.basic_salary = basic_salary
            auction.total_income = total_income
            auction.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            data = request.data
            auction = Bid_auction.objects.get(pk=pk)
            auction_name = data['auction_name']
            basic_salary = data['basic_salary']
            total_income = data['total_income']
            auction.auction_name = auction_name
            auction.basic_salary = basic_salary
            auction.total_income = total_income
            auction.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            auction_name = data['auction_name']
            basic_salary = data['basic_salary']
            total_income = data['total_income']
            auction = Bid_auction(auction_name=auction_name, basic_salary=basic_salary, total_income=total_income)
            auction.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Identify_serversideViewSet(viewsets.ViewSet):
    queryset = Identify.objects.all()
    # serializer_class = IdentifySerializer
    permission_classes = (permissions.IsAuthenticated,)

    #
    def list(self, request):
        try:
            data = request.query_params
            identify_codes = query_identify_code_by_args(data)  # 带参数查询
            serializer = IdentifySerializer(identify_codes['items'], many=True)
            result = dict()
            result['rows'] = serializer.data
            result['count'] = identify_codes['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            logger.exception("ERROR MESSAGE")
            return Response(status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def retrieve(self, request, pk=None):
        queryset = Identify.objects.all()
        identify_code = get_object_or_404(queryset, pk=pk)
        serializer = IdentifySerializer(identify_code)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            identify_code = Identify.objects.get(pk=pk)
            identify_code.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            data = request.data
            identify_code = Identify.objects.get(pk=pk)
            purchase_date = data['purchase_date_str']  # 购买时间
            expired_date = data['expired_date_str']  # 过期时间
            bid_name = data['bid_name']  # 标书姓名
            change_identify_code = data['change_identify_code']
            identify_code.purchase_date = purchase_date
            identify_code.expired_date = expired_date
            identify_code.bid_name = bid_name
            if change_identify_code == 'true':
                new_iden_code = random_str(6)  # 创建更新
                identify_code['new_iden_code'] = new_iden_code
            identify_code.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            data = request.data['data']
            data = json.loads(data)
            print(data['strategy'])
            strategy = data['strategy']

            identify_code = Identify.objects.get(pk=pk)
            purchase_date = data['purchase_date_str']  # 购买时间
            expired_date = data['expired_date_str']  # 过期时间
            bid_name = data['bid_name']  # 标书姓名
            change_identify_code = data['change_identify_code']
            identify_code.purchase_date = purchase_date
            identify_code.expired_date = expired_date
            identify_code.bid_name = bid_name
            ##处理策略
            strategy_dick = json.loads(identify_code.strategy_dick)
            strategy_dick[strategy[0]] = strategy
            identify_code.strategy_dick = json.dumps(strategy_dick)
            if change_identify_code == 'true':
                new_iden_code = random_str(6)  # 创建更新
                identify_code['new_iden_code'] = new_iden_code
            if data['changeauction'] == 'true':
                auction = Bid_auction.objects.get(pk=data['auction_name'])  ##用ID查找
                if identify_code.auction:
                    identify_code.auction.clear()  # 清除所有关系
                auction.identify_code = identify_code
                auction.save()
            identify_code.save()
            return Response(status=status.HTTP_200_OK)
        except:
            logger.exception("ERROR MESSAGE")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            data = request.data
            identify_code = random_str(6)
            ic = Identify(identify_code=identify_code, expired_date=data['expired_date'],
                               purchase_date=data['purchase_date'],
                               bid_name=data['bid_name'])
            auction = Bid_auction.objects.get(pk=data['auction_name'])
            auction.identify_code = ic
            ic.save()
            auction.save()
            return Response(status=status.HTTP_200_OK)
        except:
            logger.exception('error message')
            return Response(status=status.HTTP_404_NOT_FOUND)


class Record_serversideViewset(viewsets.ViewSet):
    query_set = Bid_record.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request):
        try:
            data = request.query_params
            records = query_record_by_args(data)  # 带参数查询
            print(records)

            serializer = Bid_recordSerializer(records['items'], many=True)
            result = dict()
            result['rows'] = serializer.data
            result['count'] = records['count']

            print(result)


            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def retrieve(self, request, pk=None):
        queryset = Bid_record.objects.all()
        record = get_object_or_404(queryset, pk=pk)
        serializer = Bid_recordSerializer(record)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            record = Bid_record.objects.get(pk=pk)
            record.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            data = request.data
            record = Bid_record.objects.get(pk=pk)
            purchase_date = data['purchase_date_str']  # 购买时间
            expired_date = data['expired_date_str']  # 过期时间
            bid_name = data['bid_name']  # 标书姓名
            change_record = data['change_record']
            print("change_record", change_record)
            record.purchase_date = purchase_date
            record.expired_date = expired_date
            record.bid_name = bid_name
            if change_record == 'true':
                new_iden_code = random_str(6)  # 创建更新
                record['new_iden_code'] = new_iden_code
            record.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            data = request.data['data']
            data = json.loads(data)
            print(data['strategy'])
            strategy = data['strategy']

            record = Bid_record.objects.get(pk=pk)
            purchase_date = data['purchase_date_str']  # 购买时间
            expired_date = data['expired_date_str']  # 过期时间
            bid_name = data['bid_name']  # 标书姓名
            change_record = data['change_record']
            record.purchase_date = purchase_date
            record.expired_date = expired_date
            record.bid_name = bid_name
            ##处理策略
            strategy_dick = json.loads(record.strategy_dick)
            strategy_dick[strategy[0]] = strategy
            record.strategy_dick = json.dumps(strategy_dick)
            if change_record == 'true':
                new_iden_code = random_str(6)  # 创建更新
                record['new_iden_code'] = new_iden_code
            if data['changeauction'] == 'true':
                auction = Bid_auction.objects.get(pk=data['auction_name'])  ##用ID查找
                if record.auction:
                    record.auction.clear()  # 清除所有关系
                auction.record = record
                auction.save()
            record.save()
            return Response(status=status.HTTP_200_OK)
        except:
            logger.exception("ERROR MESSAGE")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            data = request.data
            record = random_str(6)
            ic = record(record=record, expired_date=data['expired_date'],
                               purchase_date=data['purchase_date'],
                               bid_name=data['bid_name'])
            auction = Bid_auction.objects.get(pk=data['auction_name'])
            auction.record = ic
            ic.save()
            auction.save()
            return Response(status=status.HTTP_200_OK)
        except:
            logger.exception('error message')
            return Response(status=status.HTTP_404_NOT_FOUND)

## ----------------------------------------------------------------------------
# 软件控制
##登录
@api_view(['GET'])
def get_guopaiurl(request):
    try:
        type = request.GET['type']
        if type == 'identify_code':
            identify_code = request.GET['identify_code']
            identify = get_object_or_404( Identify, identify_code=identify_code)
            if identify.can_bid:
                diskid = request.GET['diskid']
                uuuid = identify.uuuid
                if uuuid == 'none' or diskid == uuuid:
                    ip_address = request.META.get("REMOTE_ADDR", None)
                    if identify_code != '12345678':
                        identify.uuuid = diskid
                        identify.save()  # 更新uuuid
                        reset_identify_code.delay(identify_code)  ##异步更新数据库
                    version = request.GET.get('version', None)
                    debug = request.GET.get('debug', None)
                    time1 = time.localtime(time.time())
                    time2 = time.strftime("%Y%m%d", time1)
                    today_date = time2 + "01"
                    url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
                    url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date
                    # url_dianxin = "http://51hupai.org/moni"
                    # url_nodianxin = "http://51hupai.org/moni"

                    data = init_variable()  ##初始化数据

                    ##返回标书信息
                    auction = identify.auction.all()  ##获取标书实例
                    if auction:
                        auction = auction[0]
                        account = {'account': auction.Bid_number,
                                   'password': auction.Bid_password,
                                   'idcard': auction.ID_number}
                    else:
                        account = None

                    strategy_dick = identify.strategy_dick
                    if identify_code == '12345678':
                        res = {'result': 'login success',
                               'url_dianxin': "http://51hupai.org/moni",
                               'url_nodianxin': "http://51hupai.org/moni",
                               'ip_address': ip_address,
                               'data': data,
                               'account': account,
                               'test': True,
                               'strategy_dick': strategy_dick,
                               }
                        return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
                    else:
                        res = {'result': 'login success',
                               'url_dianxin': url_dianxin,
                               'url_nodianxin': url_nodianxin,
                               'ip_address': ip_address,
                               'data': data,
                               'test': False,
                               'account': account,
                               'strategy_dick': strategy_dick,
                               }
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
        logger.exception("ERROR MESSAGE")
        return Response(status=status.HTTP_404_NOT_FOUND)


##免费模拟登录
# @api_view(['GET'])
# def monitest(request):
#     ip_address = request.META.get("REMOTE_ADDR", None)
#     version = request.GET.get('version', None)
#     debug = request.GET.get('debug', None)
#     time1 = time.localtime(time.time())
#     time2 = time.strftime("%Y%m%d", time1)
#     today_date = time2 + "01"
#     url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
#     url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date
#     data = init_variable()  ##初始化数据
#     res = {'result': 'moni success',
#            'url_dianxin': url_dianxin,
#            'url_nodianxin': url_nodianxin,
#            'ip_address': ip_address,
#            'data': data,
#            'test': False,
#            }
#     return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)


'''
[pid: 28162|app: 0|req: 6372/25180] 124.192.220.251 () {38 vars in 2473 bytes} 
[Sat Jul 21 11:17:11 2018] GET /api/bid/bid_logout/?type=Null&identify_code=0&diskid=Null&strategy_dick=%7B%220%22:%20[1,%       
2040.0,%20500,%200,%200.5,%2048,%20true,%20true,%2050,%20700,%20100,%200.5,%2056,%20true,%200,%200,%2054,%20100,%200.6,%2055,%20200,%200.5,%2056,%2056.5],
%20%221%22:%20[1,%2040.0,%20500,%200,%200.5,%20       48,%20true,%20true,%2050,%20700,%20100,%200.5,%2056,%20true,%200,%200,%2054,%20100,%200.6,%2055,%20200,
%200.5,%2056,%2056.5],%20%222%22:%20[1,%2040.0,%20500,%200,%200.5,%2048,%20true,%20true,%2050,%207       00,%20100,%200.5,%2056,%20true,%200,%200,%2054,%20100,
%200.6,%2055,%20200,%200.5,%2056,%2056.5],%20%223%22:%20[1,%2040.0,%20500,%200,%200.5,%2048,%20true,%20true,%2050,%20700,%20100,%200.5,%2056,%20tru       
e,%200,%200,%2054,%20100,%200.6,%2055,%20200,%200.5,%2056,%2056.5],%20%224%22:%20[4,%2048.0,%20700],%20%22yanzhengma_scale%22:%20true,%20%22strategy_description
%22:%20%22%5Cu5355%5Cu67aa%20%2040.0%5Cu7       9d2%5Cu52a0500%20%5Cu51fa%5Cu4ef7%22,%20%22strategy_type%22:%20%220%22,%20%22enter_on%22:%20true%7D&account=null => 
generated 0 bytes in 1 msecs (HTTP/1.1 404) 4 headers in 117 bytes (3 switches on cor       e 99)

'''


##登出
@api_view(['GET'])
def bid_logout(request):
    try:
        type = request.GET['type']
        if type == 'identify_code':
            identify_code = request.GET['identify_code']
            identify = get_object_or_404( Identify, identify_code=identify_code)
            identify.uuuid = 'none'
            identify.strategy_dick = request.GET['strategy_dick']
            ##保存 标书信息
            account = request.GET['account']
            account = json.loads(account)
            if account:
                Bid_number = account['account']
                Bid_password = account['password']
                ID_number = account['idcard']

                print(Bid_number)

                identify.auction.clear()  # 清除所有关系
                auction = Bid_auction.objects.filter(Bid_number=Bid_number)
                if auction:
                    auction[0].identify_code = identify
                    auction[0].Bid_password = Bid_password
                    auction[0].ID_number = ID_number
                    auction[0].save()
                    print(auction[0])
                else:
                    Bid_auction.objects.create(Bid_number=Bid_number, Bid_password=Bid_password,
                                               ID_number=ID_number, identify_code=identify)
            identify.save()
            res = {'result': 'logout success'}
            return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        logger.exception("ERROR MESSAGE")
        return Response(status=status.HTTP_404_NOT_FOUND)


##保持登录状态  传递数据
@api_view(['GET'])
def bid_keeplogin(request):
    try:
        type = request.GET['type']
        if type == 'identify_code':
            identify_code = request.GET['identify_code']
            identify = get_object_or_404( Identify, identify_code=identify_code)
            diskid = request.GET['diskid']
            uuuid = identify.uuuid
            if diskid == uuuid:
                res = {'result': 'keep success'}
                reset_identify_code.delay(identify_code)  ##异步还原identify_code
                identify.strategy_dick = request.GET['strategy_dick']
            elif uuuid == 'none':
                if identify_code == '12345678':
                    identify.uuuid = diskid
                    identify.strategy_dick = request.GET['strategy_dick']
                res = {'result': 'keep success'}
            ##保存 标书信息
            account = request.GET['account']
            if account:
                account = json.loads(account)
                Bid_number = account['account']
                Bid_password = account['password']
                ID_number = account['idcard']
                identify.auction.clear()  # 清除所有关系
                auction = Bid_auction.objects.filter(Bid_number=Bid_number)
                if auction:
                    auction[0].identify_code = identify
                else:
                    Bid_auction.objects.create(Bid_number=Bid_number, Bid_password=Bid_password,
                                                      ID_number=ID_number, identify_code=identify)
            identify.save()
        else:
            res = {'result': 'keep failure'}
        return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


##确认第一次出价成功
@api_view(['GET'])
def bid_firstprice(request):
    try:
        type = request.GET['type']
        if type == 'identify_code':
            bid_number = request.GET['bid_number']
            auction = Bid_auction.objects.get(Bid_number=bid_number)
            date = datetime.date.today()
            record = Bid_record.objects.get(auction=auction, date=date)
            record.firstprice = True
            record.save()
            res = {'result': 'firstprice success'}
        else:
            res = {'result': 'error'}
        return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except:
        logger.exception("ERROR MESSAGE")
        res = {'result': 'error'}
        return Response(res, status=status.HTTP_404_NOT_FOUND)

##返回时间
@api_view(['GET'])
def get_remotetime(request):
    try:
        currenttime = time.time()
        res = {'currenttime': currenttime}
        return Response(res, status=status.HTTP_200_OK, template_name=None, content_type=None)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


##-------------------------------------------------------------------------------------------------------
#### 电商自动化
@api_view(['GET'])
def create_identify_code(request):
    try:
        pass
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
