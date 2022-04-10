from decimal import Decimal
from botocore.exceptions import ClientError
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from user.views import get_user_profile
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from unittest.mock import patch
from services.service import Service
import services
import logging

services.logger.setLevel(logging.ERROR)


class GetUserProfileTest(TestCase):
    proper_login_body = {'email_address': 'asd@dsa.com', 'token': 'testmocktoken'}
    mismatch_email_login_body = {'email_address': 'asd@dsa.co', 'token': 'testmocktoken'}
    missing_token_login_body = {'email_address': 'asd@dsa.com'}
    wrong_user_email_body = {'email_address': 'asd@dsa.co'}
    proper_mock_api_call = Service.build_ok_response(**{
        'item': {'password': 'asddsa', 'user_id': 'asdffsda', 'last_name': 'dsa123', 'first_name': 'asd', 'phone_number': Decimal('123544586765'), 'email': 'asd@dsa.com',
                 'country': 'ireland', 'age': Decimal('33')}})
    dynamodb_clientError = ClientError({'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Not Found'}}, 'GetItem')
    bad_mock_api_call = Service.build_error_response(dynamodb_clientError)
    mock_token_api_call = b'asd@dsa.com'
    wrong_user_profile_mock_api_call = Service.build_ok_response(**{'item': None})

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.get_values')
    def test_proper_user_profile(self, mock_redis_get_values, mock_get_item_from_table, mock_get_item=proper_mock_api_call, mock_token=mock_token_api_call):
        mock_get_item_from_table.return_value = mock_get_item
        mock_redis_get_values.return_value = mock_token
        factory = APIRequestFactory()
        request = factory.post('/user/profile', data=self.proper_login_body)
        response = get_user_profile(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.get_values')
    def test_wrong_user_profile(self, mock_redis_get_values, mock_get_item_from_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_get_item_from_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/profile', self.wrong_user_email_body)
        response = get_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.get_values')
    def test_missing_token(self, mock_redis_get_values, mock_get_item_from_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_get_item_from_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/profile', self.missing_token_login_body)
        response = get_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.get_values')
    def test_mismatch_email(self, mock_redis_get_values, mock_get_item_from_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_get_item_from_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/profile', self.mismatch_email_login_body)
        response = get_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.get_values')
    def test_bad_response_from_db(self, mock_redis_get_values, mock_get_item_from_table, mock_api_call=bad_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_get_item_from_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/profile', self.proper_login_body)
        response = get_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.get_item_from_table')
    @patch('services.redis.Redis.get_values')
    def test_none_item_from_db(self, mock_redis_get_values, mock_get_item_from_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_get_item_from_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/profile', self.proper_login_body)
        response = get_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
