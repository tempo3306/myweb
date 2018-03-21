# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/5 9:23
'''
from myweb.wsgi import *
from django.contrib.auth.models import User
from bid.models import Bid_hander, Bid_auction
from forums.models import Topic, Board


#
def main1():
    name = ['shooter{0}'.format(i) for i in range(1, 100)]
    password = ['xcvbnm{0}'.format(i) for i in range(1, 100)]
    np = zip(name, password)
    nplist = []
    for n, p in np:
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
def bid_auction_test():
    description = 'test'  # 描述来源
    auction_name = ['袁何{0}号'.format(i) for i in range(100)]  # 标书姓名
    ID_number = [str(111111111111111111 + i * 100) for i in range(100)]  # 身份证号
    Bid_number = [str(11111111 + i) for i in range(100)]  # 标书号
    Bid_password = '1234'  # 密码
    status_ = '正常'  # 标书状态  避免重名
    count = 0  # 参拍次数
    expired_date = '2019-01-01'
    for i in range(100):
        Bid_auction.objects.get_or_create(
            description=description,  # 描述来源
            auction_name=auction_name[i],  # 标书姓名
            ID_number=ID_number[i],  # 身份证号
            Bid_number=Bid_number[i],  # 标书号
            Bid_password=Bid_password,  # 密码
            status=status_,  # 标书状态  避免重名
            count=count,  # 参拍次数
            expired_date=expired_date,  # 过期时间
        )


def board_init():
    a = Board(name='斯诺克', description="斯诺克（Snooker）的意思是“阻碍、障碍”，所以斯诺克台球有时也被称为障碍台球。",
              board_headimage='user_image/1.bmp')
    b = Board(name='九球', description="九球，起源于美国的一种台球运动的玩法。基本玩法是双方按照球号顺序依次将球击入袋中，"
                                     "率先将九号球击落袋中者获胜。",
              board_headimage='user_image/2.bmp')
    c = Board(name='中式八球', description="中式八球是有中国特色的一种新式八球，和美式普尔八球规则一样，参赛者为两人，"
                                     "台面上有花色和单色球（全色球或者实球）",
              board_headimage='user_image/3.bmp')
    a.save()
    b.save()
    c.save()



if __name__ == '__main__':
    # bid_auction_test()
    # main1()
    # main2()
    board_init()
    # init_post()
    print("Done!")
