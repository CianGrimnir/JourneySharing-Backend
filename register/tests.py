from django.test import TestCase
from rest_framework.test import APIRequestFactory
from register.views import user_register
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED)


# Create your tests here.

class UserRegisterTest(TestCase):
    proper_register_body = {'first_name': 'daw1', 'last_name': 'daw1', 'email': f'dsa1@daw.com', 'gender': 'male', 'age': '2222', 'country': 'ireland',
                            'phone_number': '123345453423', 'password': '12345', 'confirm_password': '12345'}
    already_in_use_register_body = {'first_name': 'daw', 'last_name': 'daw', 'email': f'dsa@daw.com', 'gender': 'male', 'age': '2222', 'country': 'ireland',
                                    'phone_number': '123345453423', 'password': '12345', 'confirm_password': '12345'}
    mismatch_passwd_register_body = {'first_name': 'daw', 'daw': 'nair', 'email': 'dsa@daw.com', 'gender': 'male', 'age': '2222', 'country': 'ireland',
                                     'phone_number': '123345453423', 'password': '123456', 'confirm_password': '12345'}
    missing_field_register_body = {'first_name': 'daw', 'last_name': 'daw', 'email': 'dsa@daw.com', 'age': '2222', 'country': 'ireland', 'phone_number': '123345453423',
                                   'password': '12345', 'confirm_password': '12345'}

    def test_already_in_use_user_register(self):
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.already_in_use_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_proper_user_register(self):
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.proper_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_mismatch_passwd_user_register(self):
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.mismatch_passwd_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_missing_field_user_register(self):
        factory = APIRequestFactory()
        request = factory.post('/register/register', self.missing_field_register_body)
        response = user_register(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
