import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify_code
import xlrd
from django.db import transaction
from tools.file_operation import open_excel
import logging
import copy, json

strategy = {
    "0": ["0", 50.0, 700, 0, 0.5, 55.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "1": ["1", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "2": ["2", 50.0, 700, 0, 0.5, 55.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "3": ["3", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "4": ["4", 40.0, 500, 0, 0.5, 48.0, True, True, 50.0, 700, 100, 0.5, 56.0, True, 0, 0, 54.0, 100, 0.6, 55, 200, 0.5,
          56.0,
          56.5],
    "yanzhengma_scale": True,
    "strategy_description": "单枪  50秒加700截止55秒提前100",
    "strategy_type": "0", "enter_on": True}


# one_time1	one_price	one_diff	one_delay	one_time2	force1	auto_price	second_time1	second_price
# second_diff	second_delay	second_time2	force2
# price1	delay1	time1	price2	delay2	time2	price3	delay3	time3	finaltime
def change_strategy(row):
    temp_strategy = copy.deepcopy(strategy)
    type = row['类型']
    templist = [
        type,
        float(row['one_time1']), int(row['one_price']), int(row['one_diff']), float(row['one_delay']),
        float(row['one_time2']), bool(row['force1']), bool(row['auto_price']),
        float(row['second_time1']), int(row['second_price']), int(row['second_diff']), float(row['second_delay']),
        float(row['second_time2']), bool(row['force1']), bool(row['auto_price']),
        float(row['price1']), float(row['delay1']), float(row['time1']),
        float(row['price2']), float(row['delay2']), float(row['time2']),
        float(row['price3']), float(row['delay3']), float(row['time3']), float(row['finaltime'])
    ]
    temp_strategy[type] = templist
    temp_strategy["strategy_type"] = type
    return temp_strategy


def update_strategy(file):
    rows = open_excel(file)
    print(rows)
    try:
        for row in rows:
            new_strategy = change_strategy(row)
            idenc = Identify_code.objects.get(auction__Bid_number=row['标书号'])
            idenc.strategy_dick = json.dumps(new_strategy)
            idenc.save()
    except:
        logging.exception("ERROR MESSAGE")


if __name__ == '__main__':
    update_strategy(r'init/create_strategy.xlsx')
