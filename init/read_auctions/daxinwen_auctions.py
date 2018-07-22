'''
倪锦华 310114198005110042 张叶妮 310226198611143224 范卫东 310230197102096976
郁兴 31011319890107571x 鲍红钢 310110196003151655 姚晓艳 310115199408075043
610302198403084560
310108197307204413 刘晓兰 320705196809210101 李之风 342623197603071625
| 54918104 1462 2018-10-31
54977450 1692 2018-11-30 54802308 1947 2018-09-30 54938415 1952 2018-11-30 54842080 1667 2018-09-30
54938613 1332 2018-10-31 55093570 7001 55016122 9646 54973373 7156 2018-10-31 55099783 1527 2018-12-31


'''
import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify
import xlrd
from django.db import transaction
from tools.file_operation import open_excel
import logging




def get_ids(ids):
    idlist = ids.split()
    return idlist


def get_auction(auctions):
    a_list = auctions.split()
    alen = len(a_list)
    bid_number = [a_list[i] for i in range(0, alen, 3)]
    bid_password = [a_list[i] for i in range(1, alen, 3)]
    expired = [a_list[i] for i in range(2, alen, 3)]
    return (bid_number, bid_password, expired)


def deal(ids, auctions):
    d1 = get_ids(ids)
    bid_number, bid_password, expired = get_auction(auctions)
    print(d1)

    ##保存 标书信息
    for i in range(10):
        a = 10001 + i
        ic = f'hdxw{a}'
        identify = Identify.objects.get(identify_code=ic)
        Bid_number = bid_number[i]
        Bid_password = bid_password[i]
        ID_number = d1[i]
        identify.auction.clear()  # 清除所有关系
        auction = Bid_auction.objects.filter(Bid_number=Bid_number)
        if auction:
            auction[0].identify_code = identify
            auction[0].save()
        else:
            Bid_auction.objects.create(Bid_number=Bid_number, Bid_password=Bid_password,
                                       ID_number=ID_number, identify_code=identify)





if __name__ == '__main__':
    ids = '''
310114198005110042  310226198611143224  310230197102096976
31011319890107571x  310110196003151655  310115199408075043
610302198403084560
310108197307204413  320705196809210101  342623197603071625


    '''

    auctions = '''
54918104 1462 2018-10-31
54977450 1692 2018-11-30 54802308 1947 2018-09-30 54938415 1952 2018-11-30 54842080 1667 2018-09-30 
54938613 1332 2018-10-31 55093570 7001 2018-09-30 55016122 9646 2018-09-30 54973373 7156 2018-10-31 
55099783 1527 2018-12-31

    '''

    deal(ids, auctions)
