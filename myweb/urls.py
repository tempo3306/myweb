"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.conf.urls import url, include
#
# urlpatterns = [
#     url('admin/', admin.site.urls),
#     url('^account/', include('account.urls'))

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from django.views.generic.base import TemplateView

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='myweb API')

urlpatterns = [
    url(r'^schema', schema_view),

    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^bid/', include('bid.urls', namespace='bid')),
    url('', include('news.urls')),  # new
    url('^forums/', include('forums.urls')),
    url('^api/user/', include('account.api.urls')),
    url('^api/bid/', include('bid.api.urls', namespace='api_bid')),
    url(r'^api-token-auth/', obtain_jwt_token),  #获取token
    url(r'^api-token-refresh/', refresh_jwt_token), #刷新token
    url(r'^api-token-verify/', verify_jwt_token), #确认token

    url('^hupaiyihao/', include('hupaiyihao.urls')),

    ##前端
    url(r'^manage/', TemplateView.as_view(template_name="index.html"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)