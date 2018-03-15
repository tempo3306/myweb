# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/5 9:23
'''
from myweb.wsgi import *
from django.contrib.auth.models import User
from bid.models import Bid_hander
from forums.models import Topic, Board

#
def main1():
    name = ['shooter{0}'.format(i) for i in range(1,100)]
    password = ['xcvbnm{0}'.format(i) for i in range(1,100)]
    np = zip(name, password)
    nplist = []
    for n,p in np:
        a = User.objects.create_user(username=n, password=p)
        nplist.append(a)
    for i in range(len(nplist)):
        nplist[i].save()

def main2():
    name = ['shooter{0}'.format(i) for i in range(1, 100)]
    for n in name:
        Bid_hander.objects.get_or_create(hander_name=n, user_id=User.objects.filter(username=n)[0])


# def init_post():
#     name = ['主题{0}'.format(i) for i in range(1, 100)]
#     for n in name:
#         Topic.objects.get_or_create(subject=n, board=Board.objects.filter(name='斯诺克')[0],
#                                     starter=User.objects.filter(username='zs')[0])


if __name__ == '__main__':
    main1()
    main2()
    # init_post()
    print("Done!")