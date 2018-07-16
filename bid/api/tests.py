import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from requests.auth import HTTPBasicAuth

from rest_framework import status



class UserLogoutAPIViewTestCase(APITestCase):
    url = reverse("api_bid: ic_mange")

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.client.auth = HTTPBasicAuth('user', 'pass')
        self.client.headers.update({'x-test': 'true'})


    def test_getic(self):
        datas = {'format': 'json', }
        response = self.client.get(self.url, data=datas)
        csrftoken = response.cookies['csrftoken']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'DabApps')

class guopaiurlAPIViewTestCase(APITestCase):
    get_guopaiurl = reverse("api_bid: get_guopaiurl")
    monitest = reverse("api_bid: monitest")
    get_remotetime = reverse("api_bid: get_remotetime")
    bid_firstprice = reverse("api_bid: bid_firstprice")
    bid_logout = reverse("api_bid: bid_logout")
    bid_keeplogin = reverse("api_bid: bid_keeplogin")

##101.87.221.219