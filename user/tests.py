from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from user.views import get_user_profile
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from unittest.mock import patch
from services.service import Service


class GetUserProfileTest(TestCase):
    proper_login_body = {'email_address': 'asd@dsa.com'}
    wrong_user_email_body = {'email_address': 'asd@dsa.co'}
    proper_mock_api_call = Service.build_ok_response(**{
        'item': {'password': 'asddsa', 'user_id': 'asdffsda', 'last_name': 'dsa123', 'first_name': 'asd', 'phone_number': Decimal('123544586765'), 'email': 'asd@dsa.com',
                 'country': 'ireland', 'age': Decimal('33')}})
    wrong_user_profile_mock_api_call = Service.build_ok_response(**{'item': None})

    def test_proper_user_profile(self, mock_api_call=proper_mock_api_call):
        with patch('services.dynamodb.DynamoDbService.get_item_from_table') as dynamodbMock:
            dynamodbMock.return_value = mock_api_call
            factory = APIRequestFactory()
            request = factory.get('/user/profile/', self.proper_login_body)
            response = get_user_profile(request)
            self.assertEqual(response.status_code, HTTP_200_OK)

    def test_wrong_user_profile(self, mock_api_call=wrong_user_profile_mock_api_call):
        with patch('services.dynamodb.DynamoDbService.get_item_from_table') as dynamodbMock:
            dynamodbMock.return_value = mock_api_call
            factory = APIRequestFactory()
            request = factory.get('/login/', self.wrong_user_email_body)
            response = get_user_profile(request)
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
