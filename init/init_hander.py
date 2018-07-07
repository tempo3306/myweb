import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify_code, Bid_record
import xlrd
from django.db import transaction
from tools.file_operation import open_excel


def create_hander(rows):
    query_list = []
    print(rows)
    for row in rows:
        hander_name = row['拍手名称']
        basic_salary = row['底薪']
        extra_bonus = row['奖金']
        total_income = row['总收入']

        sid = transaction.savepoint()  # 开启SQL事务
        try:
            record = Bid_hander(
                hander_name=hander_name, basic_salary=int(basic_salary),
                extra_bonus=int(extra_bonus), total_income=int(total_income)
            )
            query_list.append(record)
        except:
            print('error')
        print(len(query_list))
    with transaction.atomic():
        Bid_hander.objects.bulk_create(query_list)


def init_hander(file):
    rows = open_excel(file)
    create_hander(rows)


if __name__ == '__main__':
    init_hander('init/create_hander.xlsx')
