from django.test import TestCase
from rest_framework.test import APIRequestFactory
from journeysharing.app import MyAppConfig
from rest_framework.status import HTTP_204_NO_CONTENT
from unittest.mock import patch
import logging
import services


services.logger.setLevel(logging.DEBUG)


class JourneyMyAppTest(TestCase):

    def test_proper_user_login(self):
        setup = MyAppConfig()
        response = setup.ready()
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


