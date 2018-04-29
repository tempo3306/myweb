from django.conf.urls import url
import wx_zhuoqiuzhibo.views as views

urlpatterns = [
    url(r'^$', views.weixin),
]