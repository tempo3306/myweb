import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify
import xlrd
from django.db import transaction
from tools.file_operation import open_excel
import logging

'''
1 2
['整形','175.0']
1 1
['字符串','最后的骑士']
1 2
['浮点型','6.23']
1 3
['日期','42909.6461574']
1 0
['空值','']
1 4
['布尔型','1']
'''


def create_auction(rows):
    # query_list = []
    # 用标书号创建激活码
    for row in rows:
        print(row['激活码'])
        Identify.objects.get_or_create(identify_code='h' + str(row['标书号']))  ## h 开头表示拍手
    try:
        with transaction.atomic():
            for row in rows:
                print(row)
                description = row['标书说明']  # 描述来源
                auction_name = row['姓名']  # 标书姓名
                ID_number = row['身份证号']  # 身份证号
                Bid_number = row['标书号']  # 标书号
                Bid_password = row['标书密码']  # 密码
                status = row['状态']  # 标书状态
                expired_date = row['过期时间']  # 标书状态
                count = int(row['参拍次数'])  # 参拍次数
                identify_code = 'h' + str(row['激活码'])  # 过期时间
                sid = transaction.savepoint()  # 开启SQL事务
                # 查看是否存在
                # Member.objects.update_or_create(defaults={'user':1}, others={'field1':1,'field2':1})
                # 当存在user=1时，则更新，不存在则创建
                #     obj, created = People.objects.update_or_create(...)
                Bid_auction.objects.update_or_create(Bid_number=Bid_number,
                                                     defaults={'description': description,
                                                               'auction_name': auction_name,
                                                               'ID_number': ID_number,
                                                               'Bid_number': Bid_number,
                                                               'Bid_password': Bid_password,
                                                               'status': status,
                                                               'count': count,
                                                               'expired_date': expired_date,
                                                               'identify_code': Identify.objects.get(
                                                                   identify_code=identify_code)})
    except:
        logging.exception("ERROR MESSAGE")
        # with transaction.atomic():
        #     Bid_auction.objects.bulk_create(query_list)


strategy = {
    "0": ["0", 50.0, 700, 0, 0.5, 55.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200,
          0.5,
          56.0,
          56.5],
    "1": ["1", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200,
          0.5,
          56.0,
          56.5],
    "2": ["2", 50.0, 700, 0, 0.5, 55.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200,
          0.5,
          56.0,
          56.5],
    "3": ["3", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200,
          0.5,
          56.0,
          56.5],
    "4": ["4", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200,
          0.5,
          56.0,
          56.5],
    "yanzhengma_scale": True,
    "strategy_description": "单枪  50秒加700截止55秒提前100",
    "strategy_type": "0", "enter_on": True}


def create_identify_code(rows):
    query_list = []
    try:
        for row in rows:
            identify_code = row['激活码']  # 描述来源
            sid = transaction.savepoint()  # 开启SQL事务
            iden = Identify(identify_code=identify_code)
            query_list.append(iden)
    except:
        logging.exception("ERROR")
        print("error")
    with transaction.atomic():
        Identify.objects.bulk_create(query_list)


def init_auction(file):
    rows = open_excel(file)
    create_auction(rows)


if __name__ == '__main__':
    init_auction(r'init/create_auction.xlsx')
