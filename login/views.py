from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.dynamodb import DynamoDbService
import services
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED)
import logging
from services import const

services.logger.setLevel(logging.DEBUG)


# Create your views here.
@csrf_exempt
@api_view(["POST"])
def user_login(request):
    if request.method == 'POST':
        email_address = request.data.get("email_address")
        auth_key = request.data.get("password")
        dynamodbService = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        search_key = {'email': email_address}
        get_items = dynamodbService.get_item_from_table('user_profiles', search_key)
        services.logger.info(f"output from dynamodb - {get_items}")
        if get_items.errors is not None:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'user - {email_address} bad request, error - {get_items.errors}',
                             }
            services.logger.info(get_items.reason)
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        elif get_items.item is None:
            response_body = {'status code': HTTP_401_UNAUTHORIZED,
                             'body': 'user - ' + str(email_address) + ' not found',
                             }
            services.logger.info(f'user_name {email_address} does not exist in db')
            return Response(response_body, status=HTTP_401_UNAUTHORIZED)

        if get_items.item['password'] == auth_key:
            services.logger.info(f'{email_address} user authenticated')
            response_body = {'status code': HTTP_200_OK,
                             'body': f'user - {email_address} authenticated successfully.',
                             }
            return Response(response_body, status=HTTP_200_OK)
        else:
            response_body = {'status code': HTTP_401_UNAUTHORIZED,
                             'body': 'user - ' + str(email_address) + ' incorrect password',
                             }
            services.logger.info(f'user_name {email_address} incorrect password')
            return Response(response_body, status=HTTP_401_UNAUTHORIZED)
    else:
        response_body = {'status code': HTTP_400_BAD_REQUEST,
                         'body': f'BAD REQUEST - expected POST, got {request.method}',
                         }
        return Response(response_body, status=HTTP_400_BAD_REQUEST)
