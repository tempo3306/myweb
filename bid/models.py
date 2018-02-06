from django.db import models
from django.contrib.auth.models import User


#拍手
class Bid_hander(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_handers', null=True)
    hander_name = models.CharField(max_length=32)
    basic_salary = models.FloatField(default=50) #底薪
    extra_bonus = models.FloatField(default=0) #奖金
    total_income = models.FloatField(default=0) #总收入
    def __str__(self):
        return self.hander_name


#标书信息
class Bid_auction(models.Model):
    description = models.TextField() #描述来源
    auction_name = models.CharField(max_length=10) #标书姓名
    ID_number = models.CharField(max_length=18) #身份证号
    Bid_number = models.CharField(max_length=8) #标书号
    Bid_password = models.CharField(max_length=4) #密码
    status = models.CharField(max_length=8) #标书状态
    count = models.IntegerField() #参拍次数
    expired_date = models.DateField() #过期时间

    def __str__(self):
        return self.description


#基础策略
class Bid_action(models.Model):
    diff = models.IntegerField() #加价幅度
    refer_time = models.FloatField() #加价参考时间
    bid_time = models.FloatField() #截止时间
    delay_time = models.FloatField() #出价延迟时间
    ahead_price = models.FloatField() #出价提前价格
    hander_id = models.ForeignKey(Bid_hander, on_delete=models.CASCADE, related_name='hander_actions') #对应拍手
    action_date = models.DateField() #拍牌时间
    auction_id = models.ForeignKey(Bid_auction, on_delete=models.CASCADE, related_name='auction_actions')
    action_result = models.CharField(max_length=128, null=True) #结果记录

    def __str__(self):
        return '{0}秒加{1}提前{2}延迟{3}秒，截止时间{4}秒'.format(self.refer_time, self.diff, self.ahead_price,
                                                     self.delay_time, self.bid_time)
