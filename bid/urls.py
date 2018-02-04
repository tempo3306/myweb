from django.conf.urls import include,url
from .views import create_bid_action, create_bid_auction

app_name = 'bid'
urlpatterns = [
    url('^create_bid_action/', create_bid_action, name='create_bid_action'),
    url('^create_bid_auction/', create_bid_auction, name='create_bid_auction')
]
