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
        user_name = request.data.get("user")
        auth_key = request.data.get("password")
        dynamodbService = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        search_key = {'Username': user_name, 'Password': auth_key}
        get_items = dynamodbService.get_item_from_table('UserCreds', search_key)
        if get_items.errors is not None:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'user - {user_name} bad request, error - {get_items.errors}',
                             }
            services.logger.debug(get_items.reason)
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        elif get_items.item is None:
            response_body = {'status code': HTTP_401_UNAUTHORIZED,
                             'body': 'user - ' + str(user_name) + ' not found',
                             }
            services.logger.debug(f'user_name {user_name} does not exist in db')
            return Response(response_body, status=HTTP_401_UNAUTHORIZED)

        services.logger.info(f'{user_name} user authenticated')
        response_body = {'status code': HTTP_200_OK,
                         'body': f'user - {user_name} authenticated successfully.',
                         }
        return Response(response_body, status=HTTP_200_OK)
    else:
        response_body = {'status code': HTTP_400_BAD_REQUEST,
                         'body': f'BAD REQUEST - expected POST, got {request.method}',
                         }
        return Response(response_body, status=HTTP_400_BAD_REQUEST)
