from django.test import TestCase
from rest_framework.test import APIRequestFactory
from register.views import user_register
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED)
from unittest.mock import patch
from services.service import Service
from decimal import Decimal
import services
import logging

services.logger.setLevel(logging.ERROR)


class UserRegisterTest(TestCase):
    proper_register_body = {'first_name': 'daw1', 'last_name': 'daw1', 'email': f'dsa1@daw.com', 'gender': 'male', 'age': '2222', 'country': 'ireland',
                            'phone_number': '123345453423', 'password': '12345', 'confirm_password': '12345'}
    already_in_use_register_body = {'first_name': 'daw', 'last_name': 'daw', 'email': 'dsa@daw.com', 'gender': 'male', 'age': '2222', 'country': 'ireland',
                                    'phone_number': '123345453423', 'password': '12345', 'confirm_password': '12345'}
    mismatch_passwd_register_body = {'first_name': 'daw', 'daw': 'nair', 'email': 'dsa@daw.com', 'gender': 'male', 'age': '2222', 'country': 'ireland',
                                     'phone_number': '123345453423', 'password': '123456', 'confirm_password': '12345'}
    missing_field_register_body = {'first_name': 'daw', 'last_name': 'daw', 'email': 'dsa@daw.com', 'age': '2222', 'country': 'ireland', 'phone_number': '123345453423',
                                   'password': '12345', 'confirm_password': '12345'}
    proper_put_item_response = Service.build_ok_response(**{'item': {
        'ResponseMetadata': {'RequestId': 'LO63F6K3QV0CENCB0A72T6TJMBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200,
                             'HTTPHeaders': {'server': 'Server', 'date': 'Mon , 07 Feb 2022 00:55:25 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2',
                                             'connection': 'keep-alive', 'x-amzn-requestid': 'LO63F6K3QV0CENCB0A72T6TJMBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'},
                             'RetryAttempts': 0}}})
    already_in_use_get_item_response = Service.build_ok_response(**{
        'item': {'password': 'asddsa', 'user_id': 'asdffsda', 'last_name': 'dsa123', 'first_name': 'asd', 'phone_number': Decimal('123544586765'), 'email': 'dsa@daw.com',
                 'country': 'ireland', 'age': Decimal('33')}})

    @patch("services.dynamodb.DynamoDbService.get_item_from_table")
    @patch("services.dynamodb.DynamoDbService.put_item_in_table")
    def test_already_in_use_user_register(self, put_item, get_item, put_item_response=None, already_in_use_get_item_response=already_in_use_get_item_response):
        get_item.return_value = already_in_use_get_item_response
        put_item.return_value = put_item_response
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.already_in_use_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch("services.dynamodb.DynamoDbService.get_item_from_table")
    @patch("services.dynamodb.DynamoDbService.put_item_in_table")
    def test_proper_user_register(self, put_item, get_item, put_item_response=proper_put_item_response):
        get_item.return_value = Service.build_ok_response(**{'item': None})
        put_item.return_value = put_item_response
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.proper_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    @patch("services.dynamodb.DynamoDbService.get_item_from_table")
    @patch("services.dynamodb.DynamoDbService.put_item_in_table")
    def test_mismatch_passwd_user_register(self, put_item, get_item, put_item_response=None):
        get_item.return_value = Service.build_ok_response(**{'item': None})
        put_item.return_value = put_item_response
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.mismatch_passwd_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch("services.dynamodb.DynamoDbService.get_item_from_table")
    @patch("services.dynamodb.DynamoDbService.put_item_in_table")
    def test_missing_field_user_register(self, put_item, get_item, put_item_response=None):
        get_item.return_value = Service.build_ok_response(**{'item': None})
        put_item.return_value = put_item_response
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.missing_field_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
