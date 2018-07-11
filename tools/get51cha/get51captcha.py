import requests
import json
import re
import time

url = 'http://51moni-sh.oss-cn-shanghai.aliyuncs.com/yzm.js'


res = requests.get(url)

res.encoding = 'utf-8'


text = res.text

# text = json.loads(text)

text = re.sub('\s','',text)
text = re.sub('\"','',text)


t1, t2 = text.split('=')

t2 = re.sub('\[', '', t2)
t2 = re.sub('\]', '', t2)


t3 = t2[:-2].split(',')


urls = [t3[i]  for i in range(2, len(t3), 3)]
answers = [t3[i]  for i in range(0, len(t3), 3)]
questions = [t3[i]  for i in range(1, len(t3), 3)]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


newlist = []


num = 0

def saveimg(url, i):
    global num
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        with open('ownpic/yan{0}.jpg'.format(num + 1001), 'wb') as file:
            print(html.text)
            print(html.content)
            time.sleep(0.1)
            if html.status_code == 200:
                file.write(html.content)
            newlist.append((answers[i], questions[i]))
            num += 1





if __name__ == '__main__':
    for i, url in enumerate(urls):
        saveimg(url, i)

    import pickle
    with open('qa.txt', 'wb') as file:
        pickle.dump(newlist, file)
