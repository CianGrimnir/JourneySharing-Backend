from django.views.decorators.csrf import csrf_exempt
from statistics import mode
from django.shortcuts import render
from services.redis import Redis
import services
import logging
from services import const
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

def match_journey_requests(journey_id):
    #search all req jouney 
    redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
    all_journeys = redis_client.get_current_journey("current_journey")
    matched_journeys = []
    current_journeys = []
    requested_journey = {}
    
    for journey in all_journeys:
        curr_journey = json.loads(journey)
        current_journeys.append(curr_journey)
        if curr_journey['journeyID'] == journey_id:
            requested_journey['journeyID'] = curr_journey['journeyID']
            requested_journey['src_lat'] = curr_journey['src_lat']    
            requested_journey['src_long'] = curr_journey['src_long']
            requested_journey['des_lat'] = curr_journey['des_lat']
            requested_journey['des_long'] = curr_journey['des_long']    
        
    bt = pd.DataFrame(current_journeys)
    bt.drop('userID', inplace=True, axis=1)
    bt.drop('preferred_mode', inplace=True, axis=1)
    bt.drop('radius', inplace=True, axis=1)
    bt.drop('time', inplace=True, axis=1)
    tree_list = BallTree(np.deg2rad(bt[['src_lat', 'src_long']].values), metric='haversine')
    distances, indices = tree_list.query(np.deg2rad(np.c_[requested_journey['src_lat'], requested_journey['src_long']]), k = 3)
    
    for idx in indices.tolist():
        for i in idx:
            print(current_journeys[i])
            matched_journeys.append(current_journeys[i])

    redis_client.remove_journey(journey_id)
    return matched_journeys

# Create your views here.
#user_id,slat, slong, dlat, dlong, preferred_mode, radius, time
@csrf_exempt
@api_view(["POST"])
def new_journey_user_request(request):
    if request.method == 'POST':
        #services.logger.debug(f'request body - {request.data}')
        if request.data.get("user_id") is None:
            services.logger.error('No data received from client')
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'user - bad request',
                             }
            return Response(response_body, status=HTTP_400_BAD_REQUEST)                  
        else:
            redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
        
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

            #search_key = {'userID': user_id}
            journey_request_details = { 'journeyID': journey_id,
                                    'userID': user_id,
                                    'src_lat': slat,
                                    'src_long': slong,
                                    'des_lat': dlat,
                                    'des_long':dlong,
                                    'preferred_mode': preferred_mode,
                                    'radius': radius,
                                    'time': time}
            journey_data = json.dumps(journey_request_details).encode('utf-8')
            redis_client.set_values(journey_id, journey_data)                                          
            redis_client.add_journey(const.REDIS_JOURNEY_KEY, journey_request_details, time)
            match_journey_requests(journey_id)
            response_body = {'status code': HTTP_200_OK} 
            return Response(response_body, status=HTTP_200_OK)
    else:   
        response_body = {'status code': HTTP_400_BAD_REQUEST,
                         'body': f'BAD REQUEST - expected POST, got {request.method}',
                         }
        return Response(response_body, status=HTTP_400_BAD_REQUEST) 
 
def start_journey(groupID):
    pass

def notify_user(message):
    pass

def join_existing_journey(journey_id):
    pass

def calc_start_pt():
    pass

def calc_midpoint(start_pt, destination_list):
    pass

def rate_journey():
    pass

def end_journey():
    pass