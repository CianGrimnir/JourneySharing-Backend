import random
import string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.dynamodb import DynamoDbService
import services
from services.service import Service
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED)
import logging
from services import const

services.logger.setLevel(logging.DEBUG)


@csrf_exempt
@api_view(["POST"])
def user_register(request):
    if request.method == "POST":
        dynamodbService = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'gender', 'age', 'country', 'phone_number', 'password', 'confirm_password']
        if isinstance(request.data, dict):
            request_data = request.data
        else:
            request_data = request.data.dict()
        services.logger.info(f"request body - {request_data}")
        if not compare_dict(REQUIRED_FIELDS, request_data):
            services.logger.debug(f"reason - required field missing.")
            return Response({'message': 'required field missing'}, status=HTTP_400_BAD_REQUEST)
        search_key = {'email': request_data['email'].lower()}
        get_items = dynamodbService.get_item_from_table('user_profiles', search_key)
        if get_items.errors is not None:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f' bad request, error - {get_items.errors}',
                             }
            services.logger.debug(f"reason error - {get_items.__dict__}")
            return Response(response_body, status=HTTP_400_BAD_REQUEST)

        if get_items.item is not None:
            email = request_data['email']
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'email - {email} already in use',
                             }
            services.logger.debug(f'email address - {email} already in use')
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        if request_data['password'] != request_data['confirm_password']:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'password mismatch!',
                             }
            services.logger.debug(f'password mismatch')
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        _ = request_data.pop('confirm_password')
        request_data['user_id'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
        response = dynamodbService.put_item_in_table('user_profiles', request_data)
        services.logger.debug(f"put item - {response}")
        if response.errors is not None and response.return_code is not Service.Response.OK:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'issue with AWS API call - {response.errors} {response.return_code}',
                             }
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        response_body = {'status code': HTTP_201_CREATED,
                         'body': f'successfully created user - {request_data["email"]}'
                         }
        services.logger.debug(f"user created {request_data['email']}")
        return Response(response_body, status=HTTP_201_CREATED)


# TODO: Add validator methods to verify the compliance's for email and password
def compare_dict(required_field, request_data):
    for field in required_field:
        if field not in request_data:
            return False
    return True
