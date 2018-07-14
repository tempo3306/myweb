import requests
import json

APPID = 'wxf49962809e9326b8'
SECRET = '7ffa250a0ff45bd8de4fc977f8453c14'

url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"

res = requests.get(url)
print(res.status_code)
print(res.text)
token = json.loads(res.text)['access_token']


url2 = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + token

menu = {
    'button': [
        {'name': '沪牌百科', 'sub_button': {
            'list': [
                {'type': 'media_id', 'name': '新手指南', 'media_id': 'slxh5rbFlyROEkz6xPoXg4jmAYMKRVsIBGPReJJ6kRI'},
                {'type': 'media_id', 'name': '沪牌过户', 'media_id': 'slxh5rbFlyROEkz6xPoXgxyvP2rpEHq00I9az1XMEJM'},
                {'type': 'media_id', 'name': '外牌转沪牌', 'media_id': 'slxh5rbFlyROEkz6xPoXgzx5B5BAMW1A_skAJbvzKf8'},
                {'type': 'media_id', 'name': '沪牌选号教程', 'media_id': 'slxh5rbFlyROEkz6xPoXgwrEoEdpLPjyklp-9_F5SHE'}
            ]}},

        {'type': 'media_id', 'name': '7月拍牌',
         'media_id': 'slxh5rbFlyROEkz6xPoXg-WG2zKKsx_9G4awLYf-H0o'},

        {'name': '沪牌一号', 'sub_button': {'list': [
            {'type': 'media_id', 'name': '拍牌软件',
             'media_id': 'slxh5rbFlyROEkz6xPoXg7FidAOuTOrTOvaC0rbiCTg'},
            {'type': 'media_id', 'name': '沪牌一号代拍',
             'media_id': 'slxh5rbFlyROEkz6xPoXgzhIf1VL_f36blDTT7_ch1U'}]}}
    ]
}


res = requests.post(url2, data=menu)

print(res.status_code)
print(res.text )