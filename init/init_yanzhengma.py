import pickle
from myweb.wsgi import *
from bid.models import Bid_hander, Bid_auction, Identify_code, Yanzhengma
import xlrd
from django.db import transaction
from tools.file_operation import open_excel
import logging
import copy, json


def clear_yanzhengma():
    yans = Yanzhengma.objects.all()
    yans.delete()


def init_helong():
    import xlrd
    excel = xlrd.open_workbook('init/yan.xlsx')
    sheet = excel.sheet_by_index(0)

    answers = sheet.col_values(3)[1:]
    questions = sheet.col_values(4)[1:]

    query_list = []

    for i in range(1000):
        if isinstance(answers[i], float):
            answers[i] = int(answers[i])
        query_list.append(Yanzhengma(picture='yan{0}.jpg'.format(i + 1),
                                     question=str(questions[i]),
                                     answer=str(answers[i]),
                                     ))
    Yanzhengma.objects.bulk_create(query_list)

def init_51():
    with open('init/1001.txt', 'rb') as file:
        qa = pickle.load(file)
    query_list = []
    for i in range(500):
        if isinstance(qa[i][0], float):
            qa[i][0] = int(qa[i][0])
        query_list.append(Yanzhengma(picture='yan{0}.jpg'.format(i + 1001),
                                     question=str(qa[i][1]),
                                     answer=str(qa[i][0]),
                                     ))
    Yanzhengma.objects.bulk_create(query_list)

def init_color0_300():
    with open('init/color0_300.pkl', 'rb') as yfile:
        name_qa = pickle.load(yfile)
        print(name_qa)
    query_list = []
    lenth_name_qa = len(name_qa)

    for i in range(lenth_name_qa):
        lenth = len(name_qa[i][1])
        for j in range(lenth):
            query_list.append(Yanzhengma(picture=name_qa[i][0],
                                         question=name_qa[i][1][j][0],
                                         answer=name_qa[i][1][j][1],
                                         ))
    Yanzhengma.objects.bulk_create(query_list)


def init_yan():
    clear_yanzhengma()
    init_helong()
    init_51()
    init_color0_300()

def init_circle():
    with open('init/circle0_100.pkl', 'rb') as yfile:
        name_qa = pickle.load(yfile)
        print(name_qa)
    query_list = []
    lenth_name_qa = len(name_qa)

    for i in range(lenth_name_qa):
        lenth = len(name_qa[i][1])
        for j in range(lenth):
            print(name_qa[i][1][j][0])
            query_list.append(Yanzhengma(picture=name_qa[i][0],
                                         question=name_qa[i][1][j][0],
                                         answer=name_qa[i][1][j][1],
                                         ))
    Yanzhengma.objects.bulk_create(query_list)


if __name__ == '__main__':
    # init_yan()
    init_circle()