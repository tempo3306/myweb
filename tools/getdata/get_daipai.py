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
import pickle


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
    # labels = ['代拍费', '买单费', '标书量', '投标情况']
    labels = ['daipaifei', 'maidanfei', 'biaoshuliang', 'toubiaoqingkuang']
    for li in lis:
        bid = {}
        name = li.find('span', 'name')
        bid['name'] = name.string
        bots = li.find_all('span', 'bot')  ##找到代拍费
        for index, bot in enumerate(bots):
            print(bot.string)
            label = labels[index]
            bid[label] = bot.string
            if label == 'toubiaoqingkuang':
                try:
                    bid[label] = int(bid[label])
                    bids.append(bid)
                except:
                    pass
    print(bids)
    return bids


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


@task
def daipaihui_newdata():
    headers = get_headers()
    url = "http://www.daipaihui.com/tasklist/ajaxtask?page=1&view=ajax"
    res = get_res(url, headers)
    data = parse_res(res)
    import pickle
    try:
        with open('daipai.pkl', 'rb') as daipai:
            raw_data = pickle.load(daipai)
            if raw_data != data:
                send_control_email(data)
    except:
        with open('daipai.pkl', 'wb') as daipai:
            pickle.dump(data, daipai)
            send_control_email(data)


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

    print(res.cookies)

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
