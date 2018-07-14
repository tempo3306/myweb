from wechatpy import WeChatClient

from wechatpy import WeChatClient

from hupaiyihao.consts import APPID, SECRET
import requests, json

url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
res = requests.get(url)
keys = json.loads(res.text)

access_token = keys['access_token']
print(access_token)

client = WeChatClient(APPID, SECRET)


def create_menu():
    client = WeChatClient(APPID, SECRET)

    menu_info = client.menu.get_menu_info()
    print(menu_info)

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

    client = WeChatClient(APPID, SECRET)
    client.menu.create(menu)


from wechatpy.client.api import WeChatMaterial

# 需要传递的POST的三个参数:
# {
#     "type":TYPE,      (可以选择输入 image(图片),video(视频),voice(语音),news(图文))
#     "offset":OFFSET, (输入数字,输入0表示第一个素材)
#     "count":COUNT  (返回素材数量)
# }


if __name__ == '__main__':
    # material = WeChatMaterial(client)
    create_menu()
    # material.batchget('news', offset=0, count=20)
