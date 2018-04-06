# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2018/2/5 9:23
'''
from myweb.wsgi import *
from django.contrib.auth.models import User, Group
from bid.models import Bid_hander, Bid_auction
from forums.models import Topic, Board, ForumUser
from django.contrib.auth.models import Group, Permission

'''
        permissions = (('read', '阅读'),
                       ('reply', '回复'),
                       ('post', '发帖'),
                       ('delete', '删除'),
                       ('control', '控制'))
        
        permissions = (
            ('bid_edit', '修改'),
            ('bid_search', '搜索'),
            ('bid_create', '发帖'),
            ('bid_delete', '删除'),
        )               
                       
                       
'''
###定义角色对应的权限
role_permissions = {
    ## forums
    'forbidden_user': ['read'],
    'normal_user': ['read', 'reply', 'post'],
    'core_user': ['read', 'reply', 'post'],
    'moderator': ['read', 'reply', 'post', 'delete'],
    'admin': ['read', 'reply', 'post', 'delete', 'control'],
    ## bid
    'bid_leader': ['bid_edit', 'bid_search', 'bid_create', 'bid_delete', 'bid_control', 'bid_software'],
    'bid_admin': ['bid_edit', 'bid_search', 'bid_create', 'bid_delete', 'bid_software'],
    'bid_hander': ['bid_search', 'bid_software'],
}


def init_group(role_name):
    try:
        Group.objects.get(name=role_name)
        print("角色组已经存在")
    except Group.DoesNotExist:
        groups = Group.objects.create(name=role_name)
        pers = role_permissions[role_name]
        for per in pers:
            print(per)
            permission = Permission.objects.get(codename=per)
            groups.permissions.add(permission)


#
def shooter_init():
    name = ['shooter{0}'.format(i) for i in range(1, 100)]
    password = ['xcvbnm{0}'.format(i) for i in range(1, 100)]
    np = zip(name, password)
    nplist = []
    groups = Group.objects.get(name='bid_hander')
    for n, p in np:
        a = User.objects.create_user(username=n, password=p)
        a.groups.add(groups)
        nplist.append(a)
    for i in range(len(nplist)):
        nplist[i].save()
    name = ['shooter{0}'.format(i) for i in range(1, 100)]
    for n in name:
        Bid_hander.objects.get_or_create(hander_name=n, user_id=User.objects.filter(username=n)[0])


def admin_init():
    ##管理员初始化
    groups = Group.objects.get(name='admin')
    groups_bid_admin = Group.objects.get(name='bid_admin')

    name = 'helong'
    email = 'hlcw2619@126.com'
    password = 'helong19890103'
    helong = User.objects.create_user(username=name, password=password, email=email)
    helong.groups.add(groups)
    helong.groups.add(groups_bid_admin)
    ForumUser.objects.create(user=helong)

    name = 'yuanjunkai'
    email = '120953430@qq.com'
    password = 'yuanjunkai1988'
    yuanjunkai = User.objects.create_user(username=name, password=password, email=email)
    yuanjunkai.groups.add(groups)
    yuanjunkai.groups.add(groups_bid_admin)
    ForumUser.objects.create(user=yuanjunkai)


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


def init_yanzhengma():
    import xlrd

    excel = xlrd.open_workbook('yan.xlsx')
    sheet = excel.sheet_by_index(0)

    answers = sheet.col_values(3)[1:]
    questions = sheet.col_values(4)[1:]

    from bid.models import Yanzhengma

    query_list = []

    for i in range(1000):
        query_list.append(Yanzhengma(picture='yan{0}.jpg'.format(i + 1),
                                     question=str(questions[i]),
                                     answer=str(int(answers[i])),
                                     ))
    Yanzhengma.objects.bulk_create(query_list)


if __name__ == '__main__':
    for role, per in role_permissions.items():
        init_group(role)
    shooter_init()
    admin_init()
    board_init()
    init_yanzhengma()
    print("Done!")
