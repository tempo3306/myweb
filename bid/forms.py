from django import forms
from .models import Bid_action, Bid_auction, Bid_hander
import time

from django.forms import widgets
from datetime import date
import re

#创建一个日期选择的类
class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # create choices for days, months, years
        # example below, the rest snipped for brevity.

        years = [(year, '%d年'%year) for year in range(2016,2025)]
        months = [(month, '%d月'%month) for month in range(1,13)]
        days = [(day, '%d号'%day) for day in range(1,32)]
        _widgets = (
            widgets.Select(attrs=attrs, choices=years),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=days),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            try:
                value.split('-')
                return [value[0], value[1], value[2]]
            except AttributeError:
                return [value.year, value.month, value.day]

        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = date(
                year=int(datelist[0]),
                month=int(datelist[1]),
                day=int(datelist[2]),
            )
        except ValueError:
            return ''
        else:
            return str(D)

#创建标书
class Bid_auctionForm(forms.Form):
    status_data=[(0,"失效"),(1,"正常"),(4,"已被收回"),(3,"激活中"),(6,"已中标")]
    count_num=[(i,"%d次"%i) for i in range(7)]
    description = forms.CharField(label="说明") #描述来源
    auction_name = forms.CharField(label="姓名") #标书姓名
    ID_number = forms.CharField(label="身份证号") #身份证号
    Bid_number = forms.CharField(label="标书号", widget=forms.widgets.NumberInput()) #标书号
    Bid_password = forms.CharField(label="标书密码", widget=forms.widgets.NumberInput()) #密码
    status = forms.IntegerField(label="标书状态", widget=forms.widgets.Select(choices=status_data), initial=(1,"正常")) #标书状态
    count = forms.IntegerField(label="剩余次数", widget=forms.widgets.Select(choices=count_num), initial=(6,6)) #参拍次数
    init_date = date(year=2018, month=1, day=1)
    expired_date = forms.DateField(label="过期时间", widget=DateSelectorWidget(), initial=init_date) #过期时间

    def clean_ID_number(self):
        ID_number = self.cleaned_data['ID_number']
        # e_date = self.cleaned_data['expired_date']
        # print('e_date', e_date)
        pattern = re.compile(r'^\d{17}[0-9|x]$')
        if pattern.match(ID_number):
            pass
        else:
            raise forms.ValidationError("请输入正确的身份证号")
        self.ID_number = ID_number
        return ID_number
         # phone = self.cleaned_data['phone']//获取对应的字段
         #  pattern=re.compile(r"^((\d{3,4}-)?\d{7,8})$|(1[3-9][0-9]{9})")//设置正则验证
         #  if pattern.match(phone)://如果验证失败的话就会返回none
         #     pass
         #  else:
         #      msg=u"请输入正确的机机或座机号码！"
         #      self._errors["phone"] = self.error_class([msg])//设置输入框的告警文字
         #  self.phone=phone
         #  return phone


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

    diff = forms.IntegerField(label="加价幅度", widget=forms.widgets.Select(choices=diff_choices)) #加价幅度
    refer_time = forms.FloatField(label="参考时间", widget=forms.widgets.Select(choices=refer_time_choices)) #加价参考时间
    bid_time = forms.FloatField(label="截止时间", widget=forms.widgets.Select(choices=bid_time_choices)) #截止时间
    delay_time = forms.FloatField(label="延迟时间", widget=forms.widgets.Select(choices=delay_time_choices)) #出价延迟时间
    ahead_price = forms.FloatField(label="提前价格", widget=forms.widgets.Select(choices=ahead_price_choices)) #出价提前价格
    hander_id = forms.IntegerField(label="拍手", widget=forms.Select())
    # hander_id = forms.IntegerField(widget=forms.widgets.Select(choices=user_type_choice,attrs={'class':'form-control'})) #对应拍手
    init_date = date(year=2018, month=1, day=1)
    action_date = forms.DateTimeField(label="拍牌时期", widget=DateSelectorWidget(), initial=init_date) #拍牌时间
    auction_id = forms.IntegerField(label="标书号", widget=forms.Select())
    action_result = forms.CharField(label="结果记录", max_length=128) #结果记录

    def __init__(self, *args, **kwargs):
        super(Bid_actionForm, self).__init__(*args, **kwargs)
        self.fields['hander_id'].widget.choices = Bid_hander.objects.all().values_list('id', 'hander_name')
        self.fields['auction_id'].widget.choices = Bid_auction.objects.all().values_list('id', 'auction_name')

    def clean(self):
        cleaned_data = super(Bid_actionForm, self).clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject and "help" not in subject:
            msg = "Must put 'help' in subject when cc'ing yourself."
            self.add_error('cc_myself', msg)
            self.add_error('subject', msg)

#批量创建策略
class Batch_bid_actionForm(forms.Form):
    file = forms.FileField()

#指创建标书
class Batch_bid_auctionForm(forms.Form):
    file = forms.FileField()


