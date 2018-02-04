from django import forms
from .models import Bid_action, Bid_auction, Bid_hander
import time

#创建标书
class Bid_auctionForm(forms.Form):
    status_data=[(0,"失效"),(1,"正常"),(4,"已被收回"),(3,"激活中"),(6,"已中标")]
    count_num=[(i,"%d次"%i) for i in range(7)]
    description = forms.CharField() #描述来源
    auction_name = forms.CharField(max_length=10) #标书姓名
    ID_number = forms.CharField(max_length=18) #身份证号
    Bid_number = forms.CharField(max_length=8) #标书号
    Bid_password = forms.CharField(max_length=4) #密码
    status = forms.IntegerField(widget=forms.widgets.Select(choices=status_data), initial=(1,"正常")) #标书状态
    count = forms.IntegerField(widget=forms.widgets.Select(choices=count_num), initial=(6,6)) #参拍次数
    expired_date = forms.DateTimeField() #过期时间

#创建策略
class Bid_actionForm(forms.Form):
    diff_choices=[(i*100+400,i*100+400) for i in range(12)]
    refer_time_choices=[(i*0.1+40,"%.1f"%(i*0.1+40)) for i in range(151)]
    bid_time_choices=[(i*0.1+40,"%.1f"%(i*0.1+40)) for i in range(171)]
    delay_time_choices=[(i*0.1,"0.%d"%i) for i in range(10)]
    ahead_price_choices=[(i*100,i*100) for i in range(4)]
    date_month=[("2017年%d月"%i,"2017年%d月"%i)  for i in range(8,13)]
    date_month2=[("2018年%d月"%i,"2018年%d月"%i) for i in range(1,13)]
    date_month.extend(date_month2)
    defaultdate_list=time.strftime("%Y %m",time.localtime(time.time())).split()
    defaultdate="%d年%d月"%(int(defaultdate_list[0]),int(defaultdate_list[1]))

    diff = forms.IntegerField(widget=forms.widgets.Select(choices=diff_choices)) #加价幅度
    refer_time = forms.FloatField(widget=forms.widgets.Select(choices=refer_time_choices)) #加价参考时间
    bid_time = forms.FloatField(widget=forms.widgets.Select(choices=bid_time_choices)) #截止时间
    delay_time = forms.FloatField(widget=forms.widgets.Select(choices=delay_time_choices)) #出价延迟时间
    ahead_price = forms.FloatField(widget=forms.widgets.Select(choices=ahead_price_choices)) #出价提前价格
    hander_id = forms.IntegerField(widget=forms.Select())
    # hander_id = forms.IntegerField(widget=forms.widgets.Select(choices=user_type_choice,attrs={'class':'form-control'})) #对应拍手
    action_date = forms.DateTimeField(widget=forms.widgets.Select(choices=ahead_price_choices)) #拍牌时间
    auction_id = forms.IntegerField(widget=forms.Select())
    action_result = forms.CharField(max_length=128) #结果记录

    def __init__(self, *args, **kwargs):
        super(Bid_actionForm, self).__init__(*args, **kwargs)
        self.fields['hander_id'].widget.choices = Bid_hander.objects.all().values_list('id', 'hander_name')
        self.fields['auction_id'].widget.choices = Bid_auction.objects.all().values_list('id', 'auction_name')

#批量创建策略
class Batch_bid_actionForm(forms.Form):
    file = forms.FileField()

#指创建标书
class Batch_bid_auctionForm(forms.Form):
    file = forms.FileField()
