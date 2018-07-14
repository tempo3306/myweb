from wechatpy.client.api import WeChatMaterial

# 需要传递的POST的三个参数:
# {
#     "type":TYPE,      (可以选择输入 image(图片),video(视频),voice(语音),news(图文))
#     "offset":OFFSET, (输入数字,输入0表示第一个素材)
#     "count":COUNT  (返回素材数量)
# }

client = WeChatMaterial('')

client.batchget('news', offset=0, count=20)