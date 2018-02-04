from django.conf.urls import include,url
from .views import create_bid_action, create_bid_auction


urlpatterns = [
    url('^create_bid_action/', create_bid_action),
    url('^create_bid_auction/', create_bid_auction)
]
