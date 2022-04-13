import django.http.request
from ratelimit.decorators import ratelimit
from services.redis import Redis
import services
import logging
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK)
import logging
import django.core.exceptions
from services import const
import json
import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree

services.logger.setLevel(logging.DEBUG)
import services.utils as utils


def match_locations(request_list, requested_journey):
    matched_journeys = []
    bt = pd.DataFrame(request_list)
    if bt.empty:
        services.logger.error('No data in balltree')
        return 0
    tree_list = BallTree(np.deg2rad(bt[['src_lat', 'src_long']].values), metric='haversine')
    indices = tree_list.query_radius(np.deg2rad(np.c_[requested_journey['src_lat'], requested_journey['src_long']]),
                                     r=requested_journey['radius'])
    for idx in indices.tolist():
        for i in idx:
            matched_journeys.append(request_list[i])
    return matched_journeys


def match_journey_requests(journey_id):
    # search all req journey
    redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
    all_journeys = redis_client.get_all_journeys(const.REDIS_JOURNEY_KEY)
    src_matched_locs = []
    des_matched_locs = []
    current_journeys = []
    requested_journey = json.loads(redis_client.get_journey_from_journey_id(const.REDIS_JOURNEY_KEY, journey_id))
    if requested_journey is None:
        services.logger.error('No journey found with the given journey ID')
        return;
    for journey in all_journeys:
        if journey == journey_id:
            continue
        curr_journey = json.loads(redis_client.get_journey_from_journey_id(const.REDIS_JOURNEY_KEY, journey))
        current_journeys.append(curr_journey)
    src_matched_locs = match_locations(current_journeys, requested_journey)
    des_matched_locs = match_locations(src_matched_locs, requested_journey)
    return des_matched_locs


# Create your views here.
# user_id,slat, slong, dlat, dlong, preferred_mode, radius, time
@ratelimit(key='ip', rate='100/s', block=True)
@api_view(["POST"])
def new_journey_user_request(request):
    if request.method == 'POST':
        redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
        request_token = request.data.get("token")
        email_address = request.data.get("email_address")
        print(request.data)
        auth, reason = utils.check_request_auth(request)
        print(auth, reason)
        if not auth:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'user - {email_address} {reason} request token.',
                             }
            services.logger.info(f"username - {email_address} {reason} request token.")
            return Response(response_body, status=HTTP_400_BAD_REQUEST)

        REQUIRED_FIELDS = ['email_address', 'slat', 'slong', 'dlat', 'dlong', 'preferred_mode', 'radius', 'time']
        if isinstance(request.data, django.http.request.QueryDict):
            request_data = request.data.dict()
        else:
            request_data = request.data
        services.logger.info(f"request body - {request_data}")
        if not compare_dict(REQUIRED_FIELDS, request_data):
            services.logger.debug(f"CANNOT process req, reason - required field missing.")
            return Response({'message': 'required field missing'}, status=HTTP_400_BAD_REQUEST)
        else:            
            user_id = request.data.get("user_id")
            slat = request.data.get("slat")
            slong = request.data.get("slong")
            dlat = request.data.get("dlat")
            dlong = request.data.get("dlong")
            preferred_mode = request.data.get("preferred_mode")
            radius = request.data.get("radius")
            time = request.data.get("time")
            journey_id = utils.generate_uniqid()
            services.logger.debug(f'Creating new journey request with data: {journey_id, slat, slong, dlat, dlong, preferred_mode, radius, time}')
            drop_points = {}
            destination = [dlat, dlong]
            drop_points.setdefault("user_id", []).append(destination)
            journey_request_details = {'journeyID': journey_id,
                                       'userID': user_id,
                                       'src_lat': slat,
                                       'src_long': slong,
                                       'des_lat': dlat,
                                       'des_long': dlong,
                                       'preferred_mode': preferred_mode,
                                       'radius': radius,
                                       'time': time,
                                       'drop_points': drop_points}
            journey_data = json.dumps(journey_request_details)
            redis_client.set_values(journey_id, journey_data)
            redis_client.add_new_journey(const.REDIS_JOURNEY_KEY, journey_id, journey_request_details)
            match_journey_requests(journey_id)
            response_body = {'status code': HTTP_200_OK}
            return Response(response_body, status=HTTP_200_OK)
   


def start_journey(journey_id):
    pass


def notify_user(message):
    pass


def join_existing_journey(journey_id_self, journey_id_to_join):
    redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
    curr_journey = json.loads(redis_client.get_journey_from_journey_id(const.REDIS_JOURNEY_KEY, journey_id_self))
    join_journey = json.loads(redis_client.get_journey_from_journey_id(const.REDIS_JOURNEY_KEY, journey_id_to_join))
    drop_points = [join_journey["drop_points"], curr_journey["drop_points"]]
    join_journey["drop_points"] = drop_points
    redis_client.delete_journey_from_journey_id(const.REDIS_JOURNEY_KEY, journey_id_self)


def calc_start_pt():
    pass


def rate_journey():
    pass


def end_journey():
    pass


def compare_dict(required_field, request_data):
    for field in required_field:
        if field not in request_data:
            return False
    return True
