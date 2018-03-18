from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Bid_actionForm, Bid_auctionForm, Batch_bid_actionForm, Batch_bid_auctionForm
from .models import Bid_hander, Bid_action, Bid_auction
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings  #导入setting中的变量
import os,xlrd,json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .models import Bid_hander
from django.http import HttpResponse, Http404
from bid.models import query_auction_by_url, query_auction_by_args
from bid.api.serializers import Bid_auctionSerializer, Bid_actionSerializer
from django import template
from django.template import RequestContext


#创建策略
def bid_login(request):
    if request.method == 'GET':
        import time
        time1 = time.localtime(time.time())
        time2 = time.strftime("%Y%m%d", time1)
        today_date = time2 + "01"
        url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
        url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date

        # url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
        # url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date

        username = request.GET.get('username')
        passwd = request.GET.get('passwd')
        version = request.GET.get('version')
        debug = request.GET.get("debug")
        if version == '5.12s' or debug:
            result = Bid_hander.objects.filter(hander_name=username, hander_passwd=passwd) #验证登录
            if result:
                res = {'result': 'login success',
                                'url_dianxin': url_dianxin,
                                'url_nodianxin': url_nodianxin}
                return HttpResponse(json.dumps(res), content_type="application/json")
            else:
                res = {'result': 'wrong'}
                return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            res = {'result': 'wrong version'}
            return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def create_bid_action(request):
    if request.method == 'POST':
        form = Bid_actionForm(request.POST)
        if form.is_valid():
            diff = form.cleaned_data['diff']  # 加价幅度
            refer_time = form.cleaned_data['refer_time']  # 加价参考时间
            bid_time = form.cleaned_data['bid_time']  # 截止时间
            delay_time = form.cleaned_data['delay_time']  # 出价延迟时间
            ahead_price = form.cleaned_data['ahead_price']  # 出价提前价格
            hander_id = Bid_hander.objects.filter(id=form.cleaned_data['hander_id'])[0]
            action_date = form.cleaned_data['action_date']  # 拍牌时间
            auction_id = Bid_auction.objects.filter(id=form.cleaned_data['auction_id'])[0]
            action_result = form.cleaned_data['action_result']  # 结果记录
            try:
                with transaction.atomic():
                    action = Bid_action(diff=diff, refer_time=refer_time, bid_time=bid_time, delay_time=delay_time,
                                        ahead_price=ahead_price, hander_id=hander_id, action_date=action_date,
                                        auction_id=auction_id, action_result=action_result)
                    action.save()
                    messages.info(request, '创建成功')
                    return render(request, 'bid/create_bid_action.html', {'form': form})
            except:
                messages.error(request, '创建失败', extra_tags='bg-warning text-warning')
        else:
            return render(request, 'bid/create_bid_action.html', {'form': form, 'error': form.errors})
    else:
        form = Bid_actionForm()
    return render(request, 'bid/create_bid_action.html', {'form': form})

#创建策略
@login_required
def create_bid_auction(request):
    if request.method == 'POST':
        form = Bid_auctionForm(request.POST) #验证数据
        if form.is_valid():
            description = form.cleaned_data['description']  # 描述来源
            auction_name = form.cleaned_data['auction_name']  # 标书姓名
            ID_number = form.cleaned_data['ID_number']  # 身份证号
            Bid_number = form.cleaned_data['Bid_number']  # 标书号
            Bid_password = form.cleaned_data['Bid_password']  # 密码
            status = form.cleaned_data['status']  # 标书状态
            count = form.cleaned_data['count']  # 参拍次数
            expired_date = form.cleaned_data['expired_date']  # 过期时间
            try:
                with transaction.atomic():
                    action = Bid_auction(description=description, auction_name=auction_name, ID_number=ID_number,
                                        Bid_number=Bid_number, Bid_password=Bid_password,status=status,
                                        count=count, expired_date=expired_date)
                    action.save()
                    messages.success(request, '创建成功')
                    return render(request, 'bid/create_bid_auction.html', {'form': form})
            except:
                messages.error(request, '创建失败', extra_tags='bg-warning text-warning')
        else:
            return render(request, 'bid/create_bid_auction.html', {'form': form, "error":form.errors})
    else:
        form = Bid_auctionForm()
        return render(request, 'bid/create_bid_auction.html', {'form': form})

#读取EXCEL

# 操作EXCEL
@login_required
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))
def excel_table_byindex(file, colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list  # 返回元素为字典的列表

#批量创建策略
# @transaction.atomic
@login_required
def batch_create_action(request):
    if request.method == "POST":
        form = Batch_bid_actionForm()
        file = request.FILES.get('file', None) #获取上传的文件  默认为None
        if file:
            fname = file.name #获取文件名
            #验证文件扩展名
            filename, extention = os.path.splitext(fname)
            if extention == '.xls' or extention == '.xlsx':
                path = settings.UPLOAD_ROOT +fname  #文件存放路径
                #存储文件
                with open(path, 'wb+') as fil:
                    for chunk in file.chunks():  # 分块写入文件
                        fil.write(chunk)
                tables = excel_table_byindex(file=path)
                action_list = []
                for row in tables:  ## 判断表格式是否对
                    if '加价时间' not in row or \
                            '加价幅度' not in row or \
                            '截止时间' not in row or \
                            '延迟时间' not in row or \
                            '提前价格' not in row or \
                            '日期' not in row or \
                            '标书' not in row or \
                            '拍手' not in row:
                        messages.error(request, "EXCEL格式错误")
                        return render(request, 'bid/batch_create_action.html', {'form': form})
                    else:
                        diff = int(row['加价幅度'])
                        refer_time = float(row['加价时间'])
                        bid_time = float(row['截止时间'])
                        delay_time = float(row['延迟时间'])
                        ahead_price = int(row['提前价格'])
                        hander_id = Bid_hander.objects.filter(hander_name=row['拍手'])[0]
                        auction_id = Bid_auction.objects.filter(auction_name=row['标书'])[0]
                        action_date = row['日期']
                        try:
                            action = Bid_action(diff=diff, refer_time=refer_time, bid_time=bid_time,
                                                delay_time=delay_time,
                                                ahead_price=ahead_price, hander_id=hander_id, action_date=action_date,
                                                auction_id=auction_id)
                            action_list.append(action)
                        except:
                            messages.error(request, '创建失败', extra_tags='bg-warning text-warning')
                            return render(request, 'bid/create_bid_action.html', {'form': form})
                        try:
                            with transaction.atomic():
                                Bid_action.objects.bulk_create(action_list)
                        except:
                            messages.error(request, '创建失败', extra_tags='bg-warning text-warning')
                            return render(request, 'bid/create_bid_action.html', {'form': form})
                messages.info(request, '批量创建成功')
                return render(request, 'bid/create_bid_action.html', {'form': form})
            else:
                messages.error(request, "上传文件格式错误")
                return render(request, 'bid/batch_create_action.html', {'form': form})
        else:
            messages.error(request, "上传文件格式错误")
            return render(request, 'bid/batch_create_action.html', {'form': form})
    else:
        form = Batch_bid_actionForm()
        return render(request, 'bid/batch_create_action.html', {'form': form})

@login_required
def batch_create_auction(request):
    if request.method == "POST":
        form = Batch_bid_auctionForm()
        file = request.FILES.get('file', None)  # 获取上传的文件  默认为None
        if file:
            fname = file.name  # 获取文件名
            # 验证文件扩展名
            filename, extention = os.path.splitext(fname)
            if extention == '.xls' or extention == '.xlsx':
                path = settings.UPLOAD_ROOT + fname  # 文件存放路径
                # 存储文件
                with open(path, 'wb+') as fil:
                    for chunk in file.chunks():  # 分块写入文件
                        fil.write(chunk)

                tables = excel_table_byindex(file=path)
                auction_list = []
                for row in tables:  ## 判断表格式是否对
                    if '标书说明' not in row or \
                            '姓名' not in row or \
                            '身份证号' not in row or \
                            '标书号' not in row or \
                            '标书密码' not in row or \
                            '状态' not in row or \
                            '参拍次数' not in row or \
                            '到期时间' not in row:
                        messages.error(request, "EXCEL格式错误")
                        return render(request, 'bid/batch_create_auction.html', {'form': form})
                    else:
                        description = row['标书说明']  # 描述来源
                        auction_name = row['姓名']  # 标书姓名
                        ID_number = row['身份证号']  # 身份证号
                        Bid_number = row['标书号']  # 标书号
                        Bid_password = row['标书密码']  # 密码
                        status = row['状态']  # 标书状态
                        count = int(row['参拍次数'])  # 参拍次数
                        expired_date = row['到期时间']  # 过期时间
                        sid = transaction.savepoint()  # 开启SQL事务
                        try:
                            auction = Bid_auction(description=description, auction_name=auction_name,
                                                 ID_number=ID_number,
                                                 Bid_number=Bid_number, Bid_password=Bid_password, status=status,
                                                 count=count, expired_date=expired_date)
                            auction_list.append(auction)
                        except:
                            messages.error(request, '创建失败', extra_tags='bg-warning text-warning')
                            return render(request, 'bid/batch_create_auction.html', {'form': form})
                        try:
                            with transaction.atomic():
                                Bid_auction.objects.bulk_create(auction_list)
                        except:
                            messages.error(request, '创建失败', extra_tags='bg-warning text-warning')
                            return render(request, 'bid/create_bid_auction.html', {'form': form})
                messages.info(request, '批量创建成功')
                return render(request, 'bid/batch_create_auction.html', {'form': form})
            else:
                messages.error(request, "上传文件格式错误")
                return render(request, 'bid/batch_create_auction.html', {'form': form})
        else:
            messages.error(request, "上传文件格式错误")
            return render(request, 'bid/batch_create_auction.html', {'form': form})
    else:
        form = Batch_bid_auctionForm()
        return render(request, 'bid/batch_create_auction.html', {'form': form})

@login_required
def bid_manage(request):

    return render(request, 'bid/bid_manage.html')



@login_required
def Bid_auction_manage(request):
    """
    Retrieve, update or delete a code snippet. """
    if request.method == 'GET':
        query_auction_by_args(request.GET)
        try:
            auctions = query_auction_by_args(request.GET)
            serializer = Bid_auctionSerializer(auctions['items'], many=True)
            result = dict()
            result['rows'] = serializer.data
            result['total'] = auctions['total']
            return HttpResponse(json.dumps(result), content_type="application/json")
        except:
            return HttpResponse(status=404)
    elif request.method == 'PUT':
        data = request.GET
        print(data)
        try:
            pk = data.get('id')
            serializer = Bid_auction.objects.get(pk=pk)
            serializer = Bid_auctionSerializer(serializer, data=data)
            if serializer.is_valid():
                serializer.save()
            return HttpResponse(status=204)
        except :
            return HttpResponse(status=404)
    elif request.method == 'DELETE':
        print(request.GET)
        try:
            data = request.GET.get('data')
            data = json.loads(data)  ##转json
            print(data)
            auctions = query_auction_by_url(data)
            auctions.delete()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=404)
    elif request.method == 'POST':
        data = request.POST
        serializer = Bid_auctionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)
