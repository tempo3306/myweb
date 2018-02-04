from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import Bid_actionForm, Bid_auctionForm, Batch_bid_actionForm, Batch_bid_auctionForm
from .models import Bid_hander, Bid_action, Bid_auction
from django.db import transaction


#创建策略
def create_bid_action(request):
    if request.method == 'POST':
        form = Bid_actionForm()
        if form.is_valid():
            diff = form.cleaned_data['diff']  # 加价幅度
            refer_time = form.cleaned_data['refer_time']  # 加价参考时间
            bid_time = form.cleaned_data['bid_time']  # 截止时间
            delay_time = form.cleaned_data['delay_time']  # 出价延迟时间
            ahead_price = form.cleaned_data['ahead_price']  # 出价提前价格
            hander_id = form.cleaned_data['hander_id']
            action_date = form.cleaned_data['action_date']  # 拍牌时间
            auction_id = form.cleaned_data['auction_id']
            action_result = form.cleaned_data['action_result']  # 结果记录
            sid = transaction.savepoint()  # 开启SQL事务
            try:
                action = Bid_action(diff=diff, refer_time=refer_time, bid_time=bid_time, delay_time=delay_time,
                                    ahead_price=ahead_price, hander_id=hander_id, action_data=action_date,
                                    auction_id=auction_id, action_result=action_result)
                action.save()
                transaction.savepoint_commit(sid)
            except:
                transaction.savepoint_rollback(sid)

    else:
        form = Bid_actionForm()
    return render(request, 'create_bid_action.html', {'form': form})

#创建策略
def create_bid_auction(request):
    if request.method == 'POST':
        form = Bid_auctionForm()
        if form.is_valid():
            description = form.cleaned_data['description']  # 描述来源
            auction_name = form.cleaned_data['auction_name']  # 标书姓名
            ID_number = form.cleaned_data['ID_number']  # 身份证号
            Bid_number = form.cleaned_data['Bid']  # 标书号
            Bid_password = form.cleaned_data['Bid_password']  # 密码
            status = form.cleaned_data['status']  # 标书状态
            count = form.cleaned_data['count']  # 参拍次数
            expired_date = form.cleaned_data['expired_date']  # 过期时间
            sid = transaction.savepoint()  # 开启SQL事务
            try:
                action = Bid_action(description=description, auction_name=auction_name, ID_number=ID_number,
                                    Bid_number=Bid_number, Bid_password=Bid_password,status=status,
                                    count=count, expired_date=expired_date)
                action.save()
                transaction.savepoint_commit(sid)
            except:
                transaction.savepoint_rollback(sid)

    else:
        form = Bid_auctionForm()
        return render(request, 'create_bid_action.html', {'form': form})
       
