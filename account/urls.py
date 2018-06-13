from django.conf.urls import url
from django.contrib.auth.views import login
# With django 1.10 I need to pass the callable instead of
# url(r'^login/$', 'django.contrib.auth.views.login', name='login')

from django.contrib.auth.views import logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete
from . import views

from .views import *


handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error

urlpatterns = [
    # post views
    # url(r'^login/$', views.user_login, name='login'),

    # login logout
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    # change password
    url(r'^password-change$', views.change_password, name='password_change'),

    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
    # reset password
    ## restore password urls
    url(r'^password-reset/$',
        views.reset_password,
        name='password_reset'),
    url(r'^reset_getcode/$', views.reset_getcode, name='reset_getcode'),
    url(r'^password-reset/done/$',
        password_reset_done,
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        password_reset_complete,
        name='password_reset_complete'),
    url(r'^$', views.dashboard, name='dashboard'),  # 登录成功之后的界面
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name="user_active"),  # 提取出active后的所有字符赋给active_code
    url(r'^test_email', views.test_email),
    url(r'^active_failure', views.ActiveFailView.as_view(), name="active_fail"),
    url(r'^reactive_email/$', views.ReActiveEmailView.as_view(), name="reactive_email"), #重新发邮件

    ## 获取
    url(r'^get-token/$', get_csrf_token)


]
