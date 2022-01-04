from django.test import TestCase
from rest_framework import request
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from polls import apiviews

# Create your tests here.
class TestPoll(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = apiviews.PollViewSet.as_view({'get':'list'})
        self.url = '/polls/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
    @staticmethod
    def setup_user():
        user = get_user_model()
        return user.objects.create_user(
            'test', 
            email="test@test.com",
            password='test'
        )

    def test_list(self):
        request = self.factory.get(self.url, HTTP_AUTHORIZATION="token {}".format(self.token.key))
        request.user = self.user
        res = self.view(request)
        self.assertEqual(res.status_code, 200, 'Expected Response Code 200, recived {0} instead'.format(res.status_code))

    def test_list2(self):
        self.client.login(username="test", password="test")
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200, 'Expected Response code 200, received {0} insted'.format(resp.status_code))

    def test_create(self):
        self.client.login(username="test", password="test")
        params = {
            "question":"How are you?",
            "create_by":1
        }
        res = self.client.post(self.url, params)
        self.assertEqual(res.status_code, 201, 'Expected Response COde 201, received {0} instead'.format(res.status_code))