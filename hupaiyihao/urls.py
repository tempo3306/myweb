from django.conf.urls import url
import hupaiyihao.views as views

urlpatterns = [
    url(r'^$', views.Weixin.as_view(), name='hupaiyihao'),
]