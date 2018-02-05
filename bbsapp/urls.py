from django.conf.urls import url,include
from bbsapp import views as bbsapp_views

urlpatterns = [
    url('^$', bbsapp_views.index, name="index"),
]