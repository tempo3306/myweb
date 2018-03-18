from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from model_utils import Choices


# 拍手
class Bid_hander(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_handers', null=True)
    hander_name = models.CharField(max_length=32, default='a')
    hander_passwd = models.CharField(max_length=32, default='123456')
    basic_salary = models.FloatField(default=50)  # 底薪
    extra_bonus = models.FloatField(default=0)  # 奖金
    total_income = models.FloatField(default=0)  # 总收入

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
            Q(auction_name__icontains = searchText) |
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
            Q(refer_time__icontains = searchText) |
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
