import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify_code
import xlrd
from django.db import transaction
from tools.file_operation import open_excel
import logging
import copy, json


def create_ic():
    qset = []
    for i in range(1, 21):
        a = 10000 + i
        b = f'hdxw{a}'
        ic = Identify_code(identify_code=f'hdxw{a}')
        qset.append(ic)
    Identify_code.objects.bulk_create(qset)



if __name__ == '__main__':
    create_ic()
