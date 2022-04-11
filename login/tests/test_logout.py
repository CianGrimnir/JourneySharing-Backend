from django.test import TestCase
from rest_framework.test import APIRequestFactory
from login.views import user_logout
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from unittest.mock import patch
import services
import logging

services.logger.setLevel(logging.ERROR)


class UserLogoutTest(TestCase):
    proper_logout_body = {'email_address': 'asd@dsa.com', 'token': 'testmocktoken'}
    mismatch_email_logout_body = {'email_address': 'asd@dsa.co', 'token': 'testmocktoken'}
    mock_token_api_call = b'asd@dsa.com'

    @patch('services.redis.Redis.delete_values')
    @patch('services.redis.Redis.get_values')
    def test_proper_user_login(self, mock_get_items, mock_redis_delete_values, mock_api_call=mock_token_api_call):
        mock_redis_delete_values.return_value = True
        mock_get_items.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/session/logout/', self.proper_logout_body)
        response = user_logout(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @patch('services.redis.Redis.delete_values')
    @patch('services.redis.Redis.get_values')
    def test_wrong_password_user_logout(self, mock_get_items, mock_redis_delete_values, mock_api_call=mock_token_api_call):
        mock_redis_delete_values.return_value = None
        mock_get_items.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/session/logout/', self.mismatch_email_logout_body)
        response = user_logout(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.redis.Redis.delete_values')
    @patch('services.redis.Redis.get_values')
    def test_error_delete_logout(self, mock_get_items, mock_redis_delete_values, mock_api_call=mock_token_api_call):
        mock_redis_delete_values.return_value = False
        mock_get_items.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/session/logout/', self.proper_logout_body)
        response = user_logout(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
