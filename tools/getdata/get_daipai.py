import requests
import re
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.template import Context, loader
from django.core.mail import EmailMultiAlternatives
from myweb.settings import EMAIL_HOST_USER
from celery import task, Task
from myweb.wsgi import *
import json
import re
import collections
from myweb import celery_app
import copy
from celery.utils.log import get_task_logger
import pymongo



def update_daipai(client, data: dict) -> bool:
    try:
        print(data)
        db = client.daipaihui
        db.drop_collection('daipai') #清空
        db.daipai.insert_one(data)
        print(data)
        print('ok')
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        client.close()

def get_daipai(client) -> dict:
    try:
        db = client.daipaihui
        data = db.daipai.find_one()
        print(data)
        print(type(data))
        return data['data']
    except:
        return {}



logger = get_task_logger(__name__)

EMAIL_FROM = '810909753@qq.com'

raw_headers = '''
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Connection: keep-alive
Cookie: XSRF-TOKEN=eyJpdiI6IjNQVUVTSERPSGlGa3hYQ250TW5ZZWc9PSIsInZhbHVlIjoiXC8ySGFHOTJ3cUZqNjUrYVU2TGFWNmlzNG1Yd0dhZkZCV\
mluZFJzV0c3anpBNmxhRUhiMHFMRTdLb0NndWdRUExzd283dkVibkNqNjlQM2ZGR2g5Z0lBPT0iLCJtYWMiOiI3MTQ4NjliNTI3Njk3NzI2ZDU3NzEyNDk5N\
zNlM2I5MjM5YzJhOTE0MDZmZTJjNzlkOGQ4MTU1NjczMWUzOTJhIn0%3D; laravel_session=eyJpdiI6ImF5dlZucEx3d3lcL294RVo4XC84bVRuUT09I\
iwidmFsdWUiOiJcL0JUR2JxUFhHUWRvbG5kK3JpUUlMRVllK1ZDTjVzaVwvOG1BTFhCWkdma0ZDblorNjQwM0lwbGRDeGo3VzRLd0JSWnZwZnpwMlByWmtHa\
jhNNWZKTFd3PT0iLCJtYWMiOiJjNDkyNjQxMTJmOWFkN2FjNDk2MmZhMDU0NjM1YjZmZWE1NzY5MjJlMzA4MTg0YWFkMWZkZGI1MTcxNTc1NTZlIn0%3D
Host: www.daipaihui.com
Referer: http://www.daipaihui.com/tasklist
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
X-Requested-With: XMLHttpRequest
'''


def trans_headers(raw_headers):
    headers = raw_headers.replace(' ', '')
    headers = headers.strip().split('\n')
    headers = {x.split(':')[0]: x.split(':')[1] for x in headers}
    return headers


def get_res(url, headers):
    res = requests.get(url, headers=headers)
    print(res.status_code)
    return res


def parse_res(res):
    soup = BeautifulSoup(res.text, 'lxml')
    ul = soup.find('ul', 'renwu-wrapper')
    lis = ul.find_all('li')

    bids = []
    bids2 = []
    # labels = ['代拍费', '买单费', '标书量', '投标情况']
    labels = ['daipaifei', 'maidanfei', 'biaoshuliang', 'toubiaoqingkuang']
    for li in lis:
        print(len(lis))
        bid = {}
        name = li.find('span', 'name')
        bid['name'] = name.string
        bots = li.find_all('span', 'bot')  ##找到代拍费
        print(len(bots))
        for index, bot in enumerate(bots):
            label = labels[index]
            bid[label] = bot.string
            if label == 'toubiaoqingkuang':
                try:
                    bid[label] = int(bid[label])
                    bids2.append(bid) #带人数的
                    temp = copy.copy(bid)
                    del temp[label]
                    bids.append(temp)
                except:
                    pass
    print(bids, bids2)
    return (bids, bids2)


# 发送邮件
def send_control_email(data, **kwargs):
    email_title = "注意"
    email_template_name = 'email/daipaihui.html'
    context = {'data': data}
    html_content = loader.render_to_string(email_template_name, context)
    # 发送邮件
    subject, from_email, to = email_title, EMAIL_HOST_USER, (EMAIL_HOST_USER,)
    msg = EmailMultiAlternatives(subject, html_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@celery_app.task(ignore_result=True)
def daipaihui_newdata():
    headers = get_headers()
    url = "http://www.daipaihui.com/tasklist/ajaxtask?page=1&view=ajax"
    res = get_res(url, headers)
    data, data2 = parse_res(res)  ##data2带投标人数
    client = pymongo.MongoClient(host='localhost', port=27017)
    try:
        raw_data = get_daipai(client)
        if data == raw_data:
            pass
        else:
            send_control_email(data2)
            update_daipai(client, {'data': data})
    except:
        update_daipai(client, {'data': data})
        send_control_email(data2)


def get_headers():
    headers = '''
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Host: www.daipaihui.com
Proxy-Connection: keep-alive
Referer: http://www.daipaihui.com/
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
    '''
    headers = trans_headers(headers)

    url = "http://www.daipaihui.com/tasklist"  # 任务大厅
    res = requests.get(url, headers)
    cookie = res.headers['Set-Cookie']


    xsrf = res.cookies['XSRF-TOKEN']
    session = res.cookies['laravel_session']

    new_Cookie = {'XSRF-TOKEN': xsrf,
                  'laravel_session': session}

    Cookie = f'XSRF-TOKEN={new_Cookie["XSRF-TOKEN"]};laravel_session={new_Cookie["laravel_session"]}'

    headers = trans_headers(raw_headers)
    headers['Cookie'] = Cookie

    return headers


if __name__ == '__main__':
    # daipaihui_newdata()
    daipaihui_newdata()
