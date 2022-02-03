from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.dynamodb import DynamoDbService
import services
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
def user_register(request):
    if request.method == "POST":
        dynamodbService = DynamoDbService('dynamodb', services.default_region, services.AWS_ACCESS_KEY_ID, services.AWS_SECRET_ACCESS_KEY)
        REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'age', 'country', 'phone_number', 'password', 'confirm_password']
        request_data = json.loads(str(request.body, encoding='utf-8'))
        search_key = {'email': request_data['email'].lower()}
        get_items = dynamodbService.get_item_from_table('UserCreds', search_key)
        if get_items.errors is not None:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f' bad request, error - {get_items.errors}',
                             }
            services.logger.debug(get_items.reason)
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        if compare_dict(REQUIRED_FIELDS, request_data):
            return Response({'message': 'required field missing'}, status=HTTP_400_BAD_REQUEST)
        if get_items.item is not None:
            email = request_data['email']
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'email - {email}',
                             }
            services.logger.debug(f'email address - {email} already in use')
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        if request_data['password'] != request_data['confirm_password']:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'password mismatch!',
                             }
            services.logger.debug(f'password mismatch')
            return Response(response_body, status=HTTP_400_BAD_REQUEST)

        # Add logic to push data to dynamodb with return response - HTTP_201_CREATED


def compare_dict(required_field, request_data):
    for field in required_field:
        if field not in request_data:
            return False
    return True
