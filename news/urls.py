from django.conf.urls import url
import news.views as views

urlpatterns = [
    url('^$', views.purchase_software, name='home'),
    url('^news$', views.news, name='news'),
    ##软件相关 代拍
    url(r'^purchase_software', views.purchase_software, name='purchase_software'),
    url(r'^purchase_bid', views.purchase_bid, name='purchase_bid'),
    url(r'^course', views.course, name='course'),
    url(r'^course', views.course, name='course'),

]
