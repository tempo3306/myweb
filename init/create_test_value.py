# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/5 9:23
'''
from myweb.wsgi import *
from django.contrib.auth.models import User, Group
from bid.models import Bid_hander, Bid_auction, Identify
from forums.models import Topic, Board, ForumUser
from django.contrib.auth.models import Group, Permission

from tools.utils import random_str

'''
identify_code = models.CharField(max_length=6, unique=True)  # 激活码
purchase_date = models.DateField()
expired_date = models.DateField()  # 过期时间,激活开始计算相应的时间
bid_name = models.CharField(max_length=10, default='one')  # 标书姓名  one表示只有一次使用机会
'''



def generate_fake(count=100):
    from random import seed
    for i in range(count):
        identify = Identify(identify_code=random_str(6), purchase_date="2018-5-22",
                                 expired_date="2018-9-22", bid_name=random_str(6))

        identify.save()

if __name__ == '__main__':
    generate_fake()


