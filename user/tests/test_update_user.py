from botocore.exceptions import ClientError
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from user.views import update_user_profile
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from unittest.mock import patch
from services.service import Service
import services
import logging

services.logger.setLevel(logging.ERROR)


class UpdateUserProfileTest(TestCase):
    proper_profile_update_body = {'email_address': 'asd@dsa.com', 'token': 'testmocktoken', 'country': 'Ireland', 'gender': 'Female'}
    mismatch_email_login_body = {'email_address': 'asd@dsa.co', 'token': 'testmocktoken', 'country': 'Ireland', 'gender': 'Female'}
    missing_token_login_body = {'email_address': 'asd@dsa.com', 'country': 'Ireland', 'gender': 'Female'}
    wrong_user_email_body = {'email_address': 'asd@dsa.co', 'country': 'Ireland', 'gender': 'Female'}
    proper_mock_api_call = Service.build_ok_response(**{
        'item': {'country': 'Ireland', 'gender': 'Female'}})
    dynamodb_clientError = ClientError({'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Not Found'}}, 'GetItem')
    bad_mock_api_call = Service.build_error_response(dynamodb_clientError)
    mock_token_api_call = b'asd@dsa.com'
    wrong_user_profile_mock_api_call = Service.build_ok_response(**{'item': None})

    @patch('services.dynamodb.DynamoDbService.update_item')
    @patch('services.redis.Redis.get_values')
    def test_proper_user_update_profile(self, mock_redis_get_values, mock_update_table, mock_update_item=proper_mock_api_call, mock_token=mock_token_api_call):
        mock_update_table.return_value = mock_update_item
        mock_redis_get_values.return_value = mock_token
        factory = APIRequestFactory()
        request = factory.post('/user/update', data=self.proper_profile_update_body)
        response = update_user_profile(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @patch('services.dynamodb.DynamoDbService.update_item')
    @patch('services.redis.Redis.get_values')
    def test_wrong_user_profile(self, mock_redis_get_values, mock_update_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_update_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/update', self.wrong_user_email_body)
        response = update_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.update_item')
    @patch('services.redis.Redis.get_values')
    def test_missing_token(self, mock_redis_get_values, mock_update_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_update_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/update', self.missing_token_login_body)
        response = update_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.update_item')
    @patch('services.redis.Redis.get_values')
    def test_mismatch_email(self, mock_redis_get_values, mock_update_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_update_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/update', self.mismatch_email_login_body)
        response = update_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.update_item')
    @patch('services.redis.Redis.get_values')
    def test_bad_response_from_db(self, mock_redis_get_values, mock_update_table, mock_api_call=bad_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_update_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/update', self.proper_profile_update_body)
        response = update_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('services.dynamodb.DynamoDbService.update_item')
    @patch('services.redis.Redis.get_values')
    def test_none_item_from_db(self, mock_redis_get_values, mock_update_table, mock_api_call=wrong_user_profile_mock_api_call, mock_token=mock_token_api_call):
        mock_redis_get_values.return_value = mock_token
        mock_update_table.return_value = mock_api_call
        factory = APIRequestFactory()
        request = factory.post('/user/update', self.proper_profile_update_body)
        response = update_user_profile(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
