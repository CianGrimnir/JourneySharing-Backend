from django.test import TestCase
from rest_framework.test import APIRequestFactory
from login.views import user_login
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED)


# TODO: try to mock the aws api response.
# TODO: OR mock a dynamodbService method for covering BAD_REQUEST

class UserLoginTest(TestCase):
    proper_login_body = {'email_address': 'asd@dsa.com', 'password': 'asddsa'}
    wrong_password_login_body = {'email_address': 'asd@dsa.com', 'password': 'asddsaa'}
    wrong_login_body = {'email_address': '123@321.com', 'password': '123'}

    def test_proper_user_login(self):
        factory = APIRequestFactory()
        request = factory.post('/login/login/', self.proper_login_body)
        response = user_login(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_wrong_password_login(self):
        factory = APIRequestFactory()
        request = factory.post('/login/login/', self.wrong_password_login_body)
        response = user_login(request)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_wrong_login_body(self):
        factory = APIRequestFactory()
        request = factory.post('/login/', self.wrong_login_body)
        response = user_login(request)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)