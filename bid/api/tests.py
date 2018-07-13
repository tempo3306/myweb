import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from requests.auth import HTTPBasicAuth

from rest_framework import status



class UserLogoutAPIViewTestCase(APITestCase):
    url = reverse("api_bid:ic_mange")

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
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')