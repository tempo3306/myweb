from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from model_utils import Choices

import datetime
##------------------------------------------------------------------------------------------
##完成商业场景下的模型搭建
###创建消费者用户
class Consumer(models.Model):
    user_id = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='user_consumers',
                                   null=True, blank=True)
    account = models.CharField(max_length=8, default='1111')  ##邮箱登录
    passwd = models.CharField(max_length=6, default='1111')  ##身份证后6位
    online_status = models.SmallIntegerField(default=0)  ##登录状态，0代表未登录，1代表登录中
    login_IP = models.CharField(max_length=15, blank=True, null=True)  ##登录IP
    login_mac = models.CharField(max_length=20, blank=True, null=True)  ##mac地址
    taobao = models.CharField(max_length=30, default='none')  ##淘宝账号


##购买激活码的订单
class Consumer_software(models.Model):
    order_number = models.CharField(max_length=40)  ##表示订单来源，可以用于找回密码
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name='consumer_softwares', blank=True,
                                 null=True)
    order_date = models.DateField(auto_now_add=True)  ##订单时间



## 激活码直接可用于登录
class Identify_code(models.Model):
    identify_code = models.CharField(max_length=6, unique=True)  # 激活码
    purchase_date = models.DateField()
    expired_date = models.DateField()  # 过期时间,激活开始计算相应的时间
    bid_name = models.CharField(max_length=10, default='one')  # 标书姓名  one表示只有一次使用机会
    ##一个订单可以 生成多个激活码
    consumer_software = models.ForeignKey(Consumer_software, on_delete=models.CASCADE, related_name='identify_codes',
                                          blank=True, null=True) ##空值表示免费试用
    def can_bid(self):
        ##计算是否过期
        import datetime
        today = datetime.date.today()
        time_difference = (self.expired_date - today).days
        if time_difference >= 0:
            return True
        else:
            return False


class Invite_code(models.Model):
    invite_code = models.CharField(max_length=25)  # 邀请码
    offer_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_names')
    type = models.CharField(max_length=1, choices=(('0', '体验'), ('1', '软件折扣'), ('2', '友情价代拍'), ('3', '提成')))


class Consumer_bid(models.Model):
    status = models.CharField(max_length=1, choices=(('0', '未中标结束交易'), ('1', '完成交易'), ('2', '进行中'),
                                                     ('3', '等待客户提供新标书'), ('4', '中标后欠款中')))
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name='consumer_bids')
    order_money = models.PositiveIntegerField()  # 中标之后的应付价格
    compensation = models.PositiveIntegerField()  # 赔偿金额
    bid_number = models.PositiveSmallIntegerField()  # 合同中约定的拍牌次数
    did_number = models.PositiveSmallIntegerField()  # 已经完成的拍牌次数
    order_date = models.DateField(auto_now_add=True)  ##订单时间


##------------------------------------------------------------------------------------------
##代拍管理
## 团队
class Bid_group(models.Model):
    group_name = models.CharField(max_length=15)  ##所属团队


# 拍手
class Bid_hander(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='user_handers', null=True)
    hander_name = models.CharField(max_length=32, default='a')
    hander_passwd = models.CharField(max_length=32, default='123456')
    basic_salary = models.FloatField(default=50)  # 底薪
    extra_bonus = models.FloatField(default=0)  # 奖金
    total_income = models.FloatField(default=0)  # 总收入
    bid_group = models.ForeignKey(Bid_group, on_delete=models.CASCADE, related_name='group_hander', null=True)

    class Meta:
        permissions = (
            ('bid_software', '使用软件'),
            ('bid_edit', '修改'),
            ('bid_search', '搜索'),
            ('bid_create', '发帖'),
            ('bid_delete', '删除'),
            ('bid_control', '管理')
        )

    def __str__(self):
        return self.hander_name


# 标书信息
class Bid_auction(models.Model):
    description = models.TextField()  # 描述来源
    auction_name = models.CharField(max_length=10)  # 标书姓名
    ID_number = models.CharField(max_length=18)  # 身份证号
    Bid_number = models.CharField(max_length=8)  # 标书号
    Bid_password = models.CharField(max_length=4)  # 密码
    status = models.CharField(max_length=8)  # 标书状态
    count = models.IntegerField()  # 参拍次数
    expired_date = models.DateField()  # 过期时间
    ##下单情况
    consumer_bid = models.ForeignKey(Consumer_bid, on_delete=models.CASCADE, related_name='bid_auctions', null=True)
    bid_group = models.ForeignKey(Bid_group, on_delete=models.CASCADE, related_name='group_auctions', null=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = "bid_auction"


##设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder
def query_auction_by_args(params):
    pageSize = int(params.get('pageSize', None))  ##每页数量
    pageNumber = int(params.get('pageNumber'))  # 当前页数
    searchText = params.get('searchText', None)
    sortName = str(params.get('sortName', 'id'))
    sortOrder = str(params.get('sortOrder'))
    print(searchText)
    # django orm '-' -> desc
    if sortOrder == 'desc':
        sortName = '-' + sortName

    queryset = Bid_auction.objects.all()
    total = queryset.count()
    if searchText:
        queryset = queryset.filter(
            Q(id__icontains=searchText) |
            Q(auction_name__icontains=searchText) |
            Q(description__icontains=searchText) |
            Q(ID_number__icontains=searchText) |
            Q(Bid_number__icontains=searchText) |
            Q(Bid_password__icontains=searchText) |
            Q(status__icontains=searchText) |
            Q(count__icontains=searchText) |
            Q(expired_date__icontains=searchText))

    count = queryset.count()
    start = (pageNumber - 1) * pageSize
    queryset = queryset.order_by(sortName)[start:start + pageSize]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }


##根据url参数获取query结果
def query_auction_by_url(params):
    id_list = params.get('id')
    queryset = Bid_auction.objects.filter(id__in=id_list)
    return queryset


# 基础策略
class Bid_action(models.Model):
    diff = models.IntegerField()  # 加价幅度
    refer_time = models.FloatField()  # 加价参考时间
    bid_time = models.FloatField()  # 截止时间
    delay_time = models.FloatField()  # 出价延迟时间
    ahead_price = models.FloatField()  # 出价提前价格
    hander_id = models.ForeignKey(Bid_hander, on_delete=models.CASCADE, related_name='hander_actions')  # 对应拍手
    action_date = models.DateField()  # 拍牌时间
    auction_id = models.ForeignKey(Bid_auction, on_delete=models.CASCADE, related_name='auction_actions')
    action_result = models.CharField(max_length=128, null=True)  # 结果记录
    bid_group = models.ForeignKey(Bid_group, on_delete=models.CASCADE, related_name='group_actions', null=True)

    def __str__(self):
        return '{0}秒加{1}提前{2}延迟{3}秒，截止时间{4}秒'.format(self.refer_time, self.diff, self.ahead_price,
                                                     self.delay_time, self.bid_time)


##设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder
def query_action_by_args(params):
    pageSize = int(params.get('pageSize', None))  ##每页数量
    pageNumber = int(params.get('pageNumber'))  # 当前页数
    searchText = params.get('searchText', None)
    sortName = str(params.get('sortName', 'id'))
    sortOrder = str(params.get('sortOrder'))
    print(params)
    # django orm '-' -> desc
    if sortOrder == 'desc':
        sortName = '-' + sortName

    queryset = Bid_action.objects.all()
    total = queryset.count()
    if searchText:
        queryset = queryset.filter(
            Q(id__icontains=searchText) |
            Q(refer_time__icontains=searchText) |
            Q(bid_time__icontains=searchText) |
            Q(delay_time__icontains=searchText) |
            Q(ahead_price__icontains=searchText) |
            Q(hander_id__icontains=searchText) |
            Q(action_date__icontains=searchText) |
            Q(auction_id__icontains=searchText) |
            Q(action_result__icontains=searchText))

    count = queryset.count()
    start = (pageNumber - 1) * pageSize
    queryset = queryset.order_by(sortName)[start:start + pageSize]
    return {
        'items': queryset,
        'count': count,
        'total': total,
    }


##根据url参数获取query结果
def query_action_by_url(params):
    id_list = params.get('id')
    queryset = Bid_action.objects.filter(id__in=id_list)
    return queryset


# 验证码库
class Yanzhengma(models.Model):
    picture = models.CharField(max_length=30)  # 文件名 始终位于media/code下
    question = models.CharField(max_length=15)  # 问题
    answer = models.CharField(max_length=4)  # 答案
    type = models.CharField(max_length=20)  # 类别s

    # class Meta:
    #     unique_together = ('album', 'order')
    #     ordering = ['order']
