from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from heartbeat.views import heart_beat
from rest_framework.status import HTTP_204_NO_CONTENT
import services
import logging


services.logger.setLevel(logging.ERROR)


class HealthCheckTest(TestCase):
    @patch('journeysharing.app.MyAppConfig.ready')
    def test_proper_health_check(self, call_lb):
        call_lb.return_value = None
        factory = APIRequestFactory()
        request = factory.get('/health/ping/')
        response = heart_beat(request)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

