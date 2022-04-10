from decimal import Decimal
from botocore.exceptions import ClientError
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from login.views import user_login
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST)
from unittest.mock import patch
from services.service import Service
import services
import logging

services.logger.setLevel(logging.ERROR)


class UserLoginTest(TestCase):
    proper_login_body = {'email_address': 'asd@dsa.com', 'password': 'asddsa'}
    wrong_password_login_body = {'email_address': 'asd@dsa.com', 'password': 'asddsaa'}
    wrong_login_body = {'email_address': '123@321.com', 'password': '123'}
    proper_mock_api_call = Service.build_ok_response(**{
        'item': {'password': 'asddsa', 'user_id': 'asdffsda', 'last_name': 'dsa123', 'first_name': 'asd', 'phone_number': Decimal('123544586765'), 'email': 'asd@dsa.com',
                 'country': 'ireland', 'age': Decimal('33')}})
    wrong_login_mock_api_call = Service.build_ok_response(**{'item': None})
    getItem_clientError = ClientError({'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Not Found'}}, 'GetItem')
    bad_mock_getItem_call = Service.build_error_response(getItem_clientError)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.set_values')
    def test_proper_user_login(self, mock_redis_set_values, mock_get_items, mock_api_call=proper_mock_api_call):
        mock_redis_set_values.return_value = None
        mock_get_items.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/login/login/', self.proper_login_body)
        response = user_login(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.set_values')
    def test_wrong_password_user_login(self, mock_redis_set_values, mock_set_items, mock_api_call=proper_mock_api_call):
        mock_redis_set_values.return_value = None
        mock_set_items.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/login/login/', self.wrong_password_login_body)
        response = user_login(request)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.set_values')
    def test_wrong_body_user_login(self, mock_redis_set_values, mock_set_items, mock_api_call=wrong_login_mock_api_call):
        mock_redis_set_values.return_value = None
        mock_set_items.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/login/', self.wrong_login_body)
        response = user_login(request)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.set_values')
    def test_issue_with_dynamodb(self, mock_redis_set_values, mock_get_items, mock_api_call=bad_mock_getItem_call):
        mock_redis_set_values.return_value = None
        mock_get_items.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/login/login/', self.proper_login_body)
        response = user_login(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
