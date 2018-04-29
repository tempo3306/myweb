from django.conf.urls import url
import wx_zhuoqiuzhibo.views as views

url_patterns = [
    url(r'^weixin/', views.weixin)
]