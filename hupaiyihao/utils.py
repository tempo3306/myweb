#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from wechatpy import WeChatComponent
from django.conf import settings
from django.core.cache import caches

from bid.models import Identify_code
from tools.utils import random_str

def get_component():
    """
    获取开放平台API对象
    """
    component = WeChatComponent(
        settings.COMPONENT_APP_ID,
        settings.COMPONENT_APP_SECRET,
        settings.COMPONENT_APP_TOKEN,
        settings.COMPONENT_ENCODINGAESKEY,
        session=caches['wechat']
    )
    return component

##创建 微信公众号用户
def create_hupaiyihaouser(userid):
    from hupaiyihao.models import HupaiyihaoUser
    identify_code = create_free_ic()
    HupaiyihaoUser.objects.create(identify_code=identify_code, free_identify_code=True, useropenid=userid)
    return identify_code.identify_code



##创建激活码
def create_free_ic():
    ic = random_str(randomlength=8)
    identify_code = Identify_code.objects.create(identify_code=ic, bid_name='免费用户')
    return identify_code