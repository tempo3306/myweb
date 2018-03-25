import xlrd

excel = xlrd.open_workbook('yan.xlsx')
sheet = excel.sheet_by_index(0)

answers = sheet.col_values(3)[1:]
questions = sheet.col_values(4)[1:]


from myweb.wsgi import *
from bid.models import Yanzhengma

query_list = []

for i in range(1000):
    query_list.append(Yanzhengma(picture='yan{0}.jpg'.format(i+1),
                                 question=str(questions[i]),
                                 answer=str(int(answers[i])),
                                 ))
Yanzhengma.objects.bulk_create(query_list)