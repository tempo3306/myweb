import requests
import json

url = "http://localhost:3000/api-token-auth/"

headers = {
    'format': 'json',
}

data = {
    # 'username': 'xiaohao',
    # 'password': 'warzxw6228009'
    'username': 'zs',
    'password': 'Warzxw123;',
}

# response = requests.post(url=url, data=data, headers=headers)
# res = response.content
# res = json.loads(res)
# token = res['token']

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InpzIiwiZX\
hwIjoxNTIyNTc3NzUwLCJlbWFpbCI6IjgxMDkwOTc1M0BxcS5jb20ifQ.BpkbDxAvf2X0wqfY5lz4LgAMrz4oaYQ_8Kdvq7NSKxA'


## {"detail":"Signature has expired."}

headers = {
    'Authorization': 'JWT {0}'.format(token)
}

url = "http://localhost:3000/api/bid/action"
response = requests.get(url=url, headers=headers)


print(response.text)