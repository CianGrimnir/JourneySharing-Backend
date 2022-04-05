import re
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
    all_journeys = redis_client.get_all_journeys(const.REDIS_JOURNEY_KEY)
    src_matched_journeys = []
    des_matched_journeys = []
    current_journeys = []
    requested_journey = json.loads(redis_client.get_journey_from_journeyid(const.REDIS_JOURNEY_KEY, journey_id))
    
    for journey in all_journeys:
        if (journey == journey_id):
            continue
        
        curr_journey = json.loads(redis_client.get_journey_from_journeyid(const.REDIS_JOURNEY_KEY, journey))                   
        current_journeys.append(curr_journey)
        print("Adding journey: ", curr_journey)
 
    bt = pd.DataFrame(current_journeys)
    src_tree_list = BallTree(np.deg2rad(bt[['src_lat', 'src_long']].values), metric='haversine')
    src_indices = src_tree_list.query_radius(np.deg2rad(np.c_[requested_journey['src_lat'], requested_journey['src_long']]), 
                                                                r=requested_journey['radius'])

    for idx in src_indices.tolist():
        for i in idx:
            src_matched_journeys.append(current_journeys[i])

    bt = pd.DataFrame(src_matched_journeys)
    des_tree_list = BallTree(np.deg2rad(bt[['des_lat', 'des_long']].values), metric='haversine')
    des_indices = des_tree_list.query_radius(np.deg2rad(np.c_[requested_journey['des_lat'], requested_journey['des_long']]), 
                                                                r = requested_journey['radius'])
    for idx in des_indices.tolist():
        for i in idx:
            des_matched_journeys.append(src_matched_journeys[i])

    print("source and destination matched journeys:", len(des_matched_journeys))
    print(des_matched_journeys)
    ##########################################################
    ###### JOIN EXISTING JOURNEY #############################
    ##########################################################
    join_existing_journey(requested_journey["journeyID"], curr_journey["journeyID"])
    return des_matched_journeys

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

            redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
        
            user_id = utils.generate_uniqid()
            slat = 5.8
            slong = 4.8
            dlat = 3.93
            dlong = 5.8
            preferred_mode = "asd"
            radius = 555
            time = 23434 
            

            journey_id = utils.generate_uniqid()
            services.logger.debug(f'Creating new journey request with data: {journey_id, slat, slong, dlat, dlong, preferred_mode, radius, time}')
            drop_points = {}
            destination = [dlat, dlong]
            drop_points[user_id] = destination
            journey_request_details = { 'journeyID': journey_id,
                                    'userID': user_id,
                                    'src_lat': slat,
                                    'src_long': slong,
                                    'des_lat': dlat,
                                    'des_long':dlong,
                                    'preferred_mode': preferred_mode,
                                    'radius': radius,
                                    'time': time,
                                    'drop_points': drop_points}
            journey_data = json.dumps(journey_request_details).encode('utf-8')
            redis_client.add_new_journey(const.REDIS_JOURNEY_KEY, journey_id, journey_request_details)
            match_journey_requests(journey_id)
            response_body = {'status code': HTTP_200_OK} 
            return Response(response_body, status=HTTP_200_OK)                 
            
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

            drop_points = {}
            destination = [dlat, dlong]
            drop_points["user_id"].append(destination)

            #search_key = {'userID': user_id}
            journey_request_details = { 'journeyID': journey_id,
                                    'userID': user_id,
                                    'src_lat': slat,
                                    'src_long': slong,
                                    'des_lat': dlat,
                                    'des_long':dlong,
                                    'preferred_mode': preferred_mode,
                                    'radius': radius,
                                    'time': time,
                                    'drop_points': drop_points}
            journey_data = json.dumps(journey_request_details).encode('utf-8')
            redis_client.set_values(journey_id, journey_data)       
            print("VALUES SET:")
            print(journey_data)                                   
            #redis_client.add_journey(const.REDIS_JOURNEY_KEY, journey_request_details, time)
            #match_journey_requests(journey_id)
            response_body = {'status code': HTTP_200_OK} 
            return Response(response_body, status=HTTP_200_OK)
    else:   
        response_body = {'status code': HTTP_400_BAD_REQUEST,
                         'body': f'BAD REQUEST - expected POST, got {request.method}',
                         }
        return Response(response_body, status=HTTP_400_BAD_REQUEST) 
 
def start_journey(journey_id):
    pass

def notify_user(message):
    pass

def join_existing_journey(journey_id_self, journey_id_to_join):
    redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
    curr_journey = json.loads(redis_client.get_journey_from_journeyid(const.REDIS_JOURNEY_KEY, journey_id_self))  
    join_journey = json.loads(redis_client.get_journey_from_journeyid(const.REDIS_JOURNEY_KEY, journey_id_to_join)) 
    drop_points = []
    drop_points.append(join_journey["drop_points"])
    drop_points.append(curr_journey["drop_points"])
    join_journey["drop_points"] = drop_points   
    redis_client.delete_journey_from_journeyid(const.REDIS_JOURNEY_KEY, journey_id_self)
          
        
def calc_start_pt():
    pass

def calc_midpoint(start_pt, destination_list):
    pass

def rate_journey():
    pass

def end_journey():
    pass