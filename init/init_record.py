import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify_code, Bid_record
import xlrd
from django.db import transaction
from tools.file_operation import open_excel
import logging


def create_record(rows):
    query_list = []
    try:
        sid = transaction.savepoint()  # 开启SQL事务
        with transaction.atomic():
            for row in rows:
                auction_bid_number = row['标书号']
                hander_name = row['拍手']
                date = row['日期']
                record, created = Bid_record.objects.create_or_update(
                    default={'auction': Bid_auction.objects.get(Bid_number=auction_bid_number), 'date': date},
                    others={'hander': Bid_hander.objects.get(hander_name=hander_name)}
                )

    except:
        logging.exception("ERROR")
def init_record(file):
    rows = open_excel(file)
    create_record(rows)



if __name__ == '__main__':
    init_record('init/create_record.xlsx')