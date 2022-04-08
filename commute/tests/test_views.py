from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from commute.views import new_journey_user_request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST)
from unittest.mock import patch
import services
import logging
import json
services.logger.setLevel(logging.DEBUG)
class CommuteRequestTest(TestCase):
    proper_details_request_body = {'user_id': 'asd@dsa.com', 'slat': 5.8, 'slong': 56.9, 'dlat': 6.4, 'dlong': 6.67, 'preferred_mode': 'car',
                                   'radius': 500, 'time': 30}
    missing_details_request_body = {'slat': 5.8, 'slong': 56.9, 'dlat': 6.4, 'preferred_mode': '',
                                    'radius': 500, 'time': 30}
    proper_mock_get_journey_from_journeyid = json.dumps([{"journeyID": "qe81313qer", "userID": "asdffsda", "src_lat": 3.4, "src_long": 7.7, "des_lat": 4.5, "des_long": 23.5,
                                                          "preferred_mode": "car", "radius": 344, "drop_points": {"134134ldkjfa": [3.3, 5.5]}}])
    proper_mock_get_all_journey_api_call = {
        'fd7a87957eaa4e8': '{"journeyID": "fd7a87957eaa4e8", "userID": "bd5a37976b074ad", "src_lat": 5.8, "src_long": 4.8, "des_lat": 3.93, "des_long": 5.8, "preferred_mode": "asd", "radius": 555, "time": 23434, "drop_points": {"bd5a37976b074ad": [3.93, 5.8]}}',
        '4b6418b912ee41f': '{"journeyID": "4b6418b912ee41f", "userID": "e4e81bf832e3496", "src_lat": 5.8, "src_long": 4.8, "des_lat": 3.93, "des_long": 5.8, "preferred_mode": "asd", "radius": 555, "time": 23434, "drop_points": {"e4e81bf832e3496": [3.93, 5.8]}}'}
    mock_api_balltree_matching_call = [{'journeyID': 'ed9b3c5cad054d0', 'userID': '2674c06e79e44ef', 'src_lat': 5.8, 'src_long': 4.8, 'des_lat': 3.93, 'des_long': 5.8, 'preferred_mode': 'asd', 'radius': 555, 'time': 23434, 'drop_points': {'2674c06e79e44ef': [3.93, 5.8]}}]
    @patch('services.redis.Redis.set_values')
    @patch('services.redis.Redis.add_new_journey')
    @patch('services.redis.Redis.get_all_journeys')
    @patch('services.redis.Redis.get_journey_from_journeyid')
    @patch('commute.views.match_locations')
    def test_proper_details_journey_request(self, mock_balltree, mock_redis_get_journey_from_journeyid, mock_redis_get_all_journeys,
                                            mock_redis_add_journey, mock_redis_set_values,
                                            mock_balltree_return = mock_api_balltree_matching_call,
                                            mock_get_all_journey_api_call=proper_mock_get_all_journey_api_call, \
                                            mock_get_journey_from_journeyid=proper_mock_get_journey_from_journeyid):
        mock_redis_add_journey.return_value = None
        mock_redis_set_values.return_value = None
        mock_balltree.return_value = mock_balltree_return
        mock_redis_get_all_journeys.return_value = mock_get_all_journey_api_call
        mock_redis_get_journey_from_journeyid.return_value = mock_get_journey_from_journeyid
        factory = APIRequestFactory()
        request = factory.post('/commute/createNewRequest/', self.proper_details_request_body)
        response = new_journey_user_request(request)
        self.assertEqual(response.status_code, HTTP_200_OK)
    def test_missing_details_journey_request(self):
        factory = APIRequestFactory()
        request = factory.post('/commute/createNewRequest/', self.missing_details_request_body)
        response = new_journey_user_request(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)