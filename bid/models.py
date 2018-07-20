from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from model_utils import Choices

import datetime
from tools.utils import random_str
## 激活码直接可用于登录

strategy = {
    "0": ["0", 50.0, 700, 0, 0.5, 55.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "1": ["1", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "2": ["2", 50.0, 700, 0, 0.5, 55.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "3": ["3", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "4": ["4", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "yanzhengma_scale": True,
    "strategy_description": "单枪  50秒加700截止55秒提前100",
    "strategy_type": "0", "enter_on": True}
import json


class Identify_code(models.Model):
    identify_code = models.CharField(max_length=10, unique=True)  # 激活码   用标书号代替
    purchase_date = models.DateField(default=datetime.date.today())
    expired_date = models.DateField(default=datetime.date.today()+datetime.timedelta(days=28))  # 过期时间,激活开始计算相应的时间
    bid_name = models.CharField(max_length=10, default='沪牌一号')  # 标书姓名  one表示只有一次使用机会
    uuuid_type = models.CharField(max_length=15, default='diskid')
    uuuid = models.CharField(max_length=40, default='none', blank=True)  ###确认标识码
    last_uuuid = models.CharField(max_length=40, default='none', blank=True)  ###最近的一个确认标识码
    # login_status = models.SmallIntegerField(default=0, blank=True)   ##登录状态 默认为0 代表未登录  代表登录
    strategy_dick = models.TextField(default=json.dumps(strategy), blank=True)  ##保存用户设置的策略

    @property
    def can_bid(self):
        ##计算是否过期
        import datetime
        today = datetime.date.today()
        time_difference = (self.expired_date - today).days
        if time_difference >= 0:
            return True
        else:
            return False

    def __str__(self):
        return self.identify_code


class Strategy(models.Model):
    strategytype = models.CharField(max_length=1, unique=True)
    chujia_time1 = models.FloatField()
    chujia_price1 = models.PositiveIntegerField()
    tijiao_diff = models.PositiveIntegerField()
    tijiao_time1 = models.FloatField()
    tijiao_yanchi1 = models.FloatField()
    forcetijiao1 = models.BooleanField()
    # // 补枪
    autoprice = models.BooleanField()
    # // 第二枪
    chujia_time2 = models.FloatField()
    chujia_price2 = models.PositiveIntegerField()
    tijiao_diff2 = models.PositiveIntegerField()
    tijiao_time2 = models.FloatField()
    tijiao_yanchi2 = models.FloatField()
    forcetijiao2 = models.BooleanField()
    # // 动态
    smart_diff1 = models.PositiveIntegerField()
    smart_yanchi1 = models.FloatField()
    smart_time1 = models.FloatField()
    smart_diff2 = models.PositiveIntegerField()
    smart_yanchi2 = models.FloatField()
    smart_time2 = models.FloatField()
    smart_diff3 = models.PositiveIntegerField()
    smart_yanchi3 = models.FloatField()
    smart_time3 = models.FloatField()
    smart_time = models.FloatField()


def query_identify_code_by_args(params):
    pageSize = int(params.get('limit', None))  ##每页数量
    pageNumber = int(params.get('page', None))  # 当前页数
    searchText = params.get('search', None)
    sortName = str(params.get('sort', 'id'))

    # sortOrder = str(params.get('sortOrder'))
    # django orm '-' -> desc

    queryset = Identify_code.objects.all()
    # total = queryset.count()
    if searchText:
        queryset = queryset.filter(
            Q(id__icontains=searchText) |
            Q(bid_name__icontains=searchText) |
            Q(identify_code__icontains=searchText))

    count = queryset.count()
    print("count=", count)

    start = (pageNumber - 1) * pageSize
    queryset = queryset.order_by(sortName)[start:start + pageSize]
    return {
        'items': queryset,
        'count': count,
    }


##------------------------------------------------------------------------------------------
##完成商业场景下的模型搭建
###创建消费者用户
class Consumer(models.Model):
    user_slug = models.CharField(max_length=10, unique=True, verbose_name="用户描述", default="12345")
    taobao = models.CharField(max_length=30, default='none', blank=True)  ##淘宝账号
    telephone = models.CharField(max_length=11, unique=True, default='12345678901')
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return "{0} 手机号: {1}".format(self.user_slug, self.telephone)


class Invite_code(models.Model):
    invite_code = models.CharField(max_length=25)  # 邀请码
    offer_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offer_names')
    type = models.CharField(max_length=1, choices=(('0', '体验'), ('1', '软件折扣'), ('2', '友情价代拍'), ('3', '提成')))


##代拍-----------------------------------------------------
##定单
class Consumer_bid(models.Model):
    status_choices = (('0', '未中标结束交易'), ('1', '完成交易'), ('2', '进行中'),
                      ('3', '等待客户提供新标书'), ('4', '中标后欠款中'),
                      ('11', '软件正常'), ('12', '软件过期'))

    status = models.CharField(max_length=2, choices=status_choices)  ##软件的定单
    ##软件订单才有的
    order_money = models.PositiveIntegerField(default=0, blank=True)  # 中标之后的应付价格
    compensation = models.PositiveIntegerField(default=0, blank=True)  # 赔偿金额
    bid_number = models.PositiveSmallIntegerField(default=0, blank=True)  # 合同中约定的拍牌次数
    did_number = models.PositiveSmallIntegerField(default=0, blank=True)  # 已经完成的拍牌次数
    ##都有
    order_date = models.DateField(auto_now_add=True)  ##订单时间
    order_str = models.CharField(max_length=50, blank=True, default='hupaiyihao')
    ##用户信息
    user_slug = models.CharField(max_length=10, unique=True, verbose_name="用户描述", default="hupaiyihao", blank=True)
    telephone = models.CharField(max_length=11, unique=True, default='', null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    # 外键
    identify_code = models.ForeignKey(Identify_code, on_delete=models.CASCADE, related_name='consumer_bids',
                                      null=True, blank=True)

    def __str__(self):
        return "{0} {1} 订单时间{2}".format(self.user_slug, self.get_status_display(), self.order_date)


##------------------------------------------------------------------------------------------
##代拍管理
# ## 团队
# class Bid_group(models.Model):
#     group_name = models.CharField(max_length=15)  ##所属团队


# 拍手
class Bid_hander(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='user_handers', null=True)
    hander_name = models.CharField(max_length=6, default=random_str(4), unique=True)
    hander_passwd = models.CharField(max_length=32, default='123456')
    basic_salary = models.FloatField(default=50)  # 底薪
    extra_bonus = models.FloatField(default=500)  # 奖金
    total_income = models.FloatField(default=0)  # 总收入
    telephone = models.CharField(max_length=11, null=True, blank=True)


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


def query_hander_by_args(params):
    pageSize = int(params.get('limit', None))  ##每页数量
    pageNumber = int(params.get('page', None))  # 当前页数
    searchText = params.get('search', None)
    sortName = str(params.get('sort', 'id'))
    # sortOrder = str(params.get('sortOrder'))
    # django orm '-' -> desc

    queryset = Bid_hander.objects.all()
    # total = queryset.count()
    if searchText:
        queryset = queryset.filter(
            Q(hander_name__icontains=searchText))

    count = queryset.count()
    print("count=", count)

    start = (pageNumber - 1) * pageSize
    queryset = queryset.order_by(sortName)[start:start + pageSize]
    return {
        'items': queryset,
        'count': count,
    }


# 标书信息
class Bid_auction(models.Model):
    description = models.TextField()  # 描述来源
    auction_name = models.CharField(max_length=10, default='temp')  # 标书姓名   temp代表软件用户
    ID_number = models.CharField(max_length=18)  # 身份证号
    Bid_number = models.CharField(max_length=8, unique=True)  # 标书号
    Bid_password = models.CharField(max_length=4)  # 密码
    # (('0', '未中标结束交易'), ('1', '中标完成交易'), ('2', '正常进行中'),
    # ('3', '标书失效'), ('4', '中标未完成交易') ， ('14', '软件用户使用')
    status = models.CharField(max_length=8, default='软件用户使用')  # 标书状态
    count = models.IntegerField(default=0)  # 参拍次数
    expired_date = models.DateField(default=datetime.datetime.now() + datetime.timedelta(days=120))  # 过期时间
    ##绑定的激活码
    identify_code = models.ForeignKey(Identify_code, on_delete=models.CASCADE, related_name='auction',
                                      blank=True, null=True, unique=True)

    def __str__(self):
        return self.description

    class Meta:
        db_table = "bid_auction"


##设置为undefined可以获取pageNumber，pageSize，searchText，sortName，sortOrder
def query_auction_by_args(params):
    pageSize = int(params.get('limit', None))  ##每页数量
    pageNumber = int(params.get('page', None))  # 当前页数
    searchText = params.get('search', None)
    sortName = str(params.get('sort', 'id'))

    queryset = Bid_auction.objects.all()
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
    }


def query_available_auction() -> object:
    # users_without_reports = User.objects.filter(report__isnull=True)
    # users_with_reports = User.objects.filter(report__isnull=False).distinct()

    queryset = Bid_auction.objects.all()
    queryset = queryset.filter(identify_code__isnull=True)

    return {
        'items': queryset
    }


# ##根据url参数获取query结果
# def query_auction_by_url(params):
#     id_list = params.get('id')
#     queryset = Bid_auction.objects.filter(id__in=id_list)
#     return queryset

##拍牌前一周完成这周拍牌的记录
##绑定 人员与标书，激活码
class Bid_record(models.Model):
    auction = models.ForeignKey(Bid_auction, on_delete=models.CASCADE, related_name='records')
    # auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
    # auto_now_add为添加时的时间，更新对象时不会有变动。
    date = models.DateField()
    hander = models.ForeignKey(Bid_hander, on_delete=models.CASCADE, related_name='records')
    strategy_dick = models.TextField(default=json.dumps(strategy), blank=True)  ##此次的策略信息
    result = models.CharField(max_length=100, verbose_name='结果说明', default='等待拍牌')
    firstprice = models.BooleanField(default=False)  #由拍手在软件上确认


    def __str__(self):
        return f"{self.date} {self.auction.Bid_number}"

def query_record_by_args(params):
    pageSize = int(params.get('limit', None))  ##每页数量
    pageNumber = int(params.get('page', None))  # 当前页数
    searchText = params.get('search', None)
    sortName = str(params.get('sort', 'id'))

    queryset = Bid_record.objects.all()
    if searchText:
        queryset = queryset.filter(
            Q(id__icontains=searchText) |
            Q(result__icontains=searchText) |
            Q(date__icontains=searchText))
    if sortName == 'firstprice':
        queryset = queryset.filter(firstprice=True)
    elif sortName == '-firstprice':
        queryset = queryset.filter(firstprice=False)
    else:
        queryset = queryset.order_by(sortName)
    count = queryset.count()
    start = (pageNumber - 1) * pageSize
    queryset = queryset[start:start + pageSize]
    return {
        'items': queryset,
        'count': count,
    }


# 基础策略
class Bid_action(models.Model):
    diff = models.IntegerField()  # 加价幅度
    refer_time = models.FloatField()  # 加价参考时间
    bid_time = models.FloatField()  # 截止时间
    delay_time = models.FloatField()  # 出价延迟时间
    ahead_price = models.FloatField()  # 出价提前价格
    action_date = models.DateField()  # 拍牌时间
    action_result = models.CharField(max_length=128, null=True, blank=True)  # 结果记录

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
    answer = models.CharField(max_length=6)  # 答案
    type = models.CharField(max_length=20)  # 类别s

    # class Meta:
    #     unique_together = ('album', 'order')
    #     ordering = ['order']
