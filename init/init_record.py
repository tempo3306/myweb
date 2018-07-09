import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify_code, Bid_record
import xlrd
from django.db import transaction
from tools.file_operation import open_excel
import logging


def create_record(rows):
    query_list = []
    for row in rows:
        auction_bid_number = row['标书号']
        hander_name = row['拍手']
        date = row['日期']

        sid = transaction.savepoint()  # 开启SQL事务
        try:
            record = Bid_record(auction=Bid_auction.objects.get(Bid_number=auction_bid_number),
                                hander=Bid_hander.objects.get(hander_name=hander_name),
                                date=date)
            query_list.append(record)
        except:
            logging.exception("ERROR")
    with transaction.atomic():
        Bid_record.objects.bulk_create(query_list)

def init_record(file):
    rows = open_excel(file)
    create_record(rows)



if __name__ == '__main__':
    init_record('init/create_record.xlsx')