import logging
import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify, Bid_record
import xlrd
from django.db import transaction
from tools.file_operation import open_excel


def create_hander(rows):
    sid = transaction.savepoint()  # 开启SQL事务
    try:
        with transaction.atomic():
            for row in rows:
                hander_name = row['拍手名称']
                basic_salary = row['底薪']
                extra_bonus = row['奖金']
                total_income = row['总收入']
                telephone = row['手机号']
                print("hander_name", hander_name)
                # h = Bid_hander.objects.get(hander_name=hander_name)
                # print(len(h))
                Bid_hander.objects.update_or_create(
                    hander_name=hander_name,
                    defaults={'basic_salary': int(basic_salary),
                             'extra_bonus': int(extra_bonus),
                             'total_income': int(total_income),
                              'telephone': telephone}
                )
    except:
        logging.exception("ERROR MESSAGE")


def init_hander(file):
    rows = open_excel(file)
    create_hander(rows)


if __name__ == '__main__':
    init_hander('init/create_hander.xlsx')
