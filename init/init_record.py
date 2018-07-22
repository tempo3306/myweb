import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify, Bid_record
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
                records = Bid_record.objects.filter(auction__Bid_number=auction_bid_number, date=date)
                if records:
                    records[0].hander = Bid_hander.objects.get(hander_name=hander_name)
                    records[0].save()
                else:
                    hander = Bid_hander.objects.get(hander_name=hander_name)
                    auction = Bid_auction.objects.get(Bid_number=auction_bid_number)
                    Bid_record.objects.create(
                        auction=auction, date=date, hander=hander
                    )

    except:
        logging.exception("ERROR")


def init_record(file):
    rows = open_excel(file)
    create_record(rows)


if __name__ == '__main__':
    init_record('init/create_record.xlsx')
