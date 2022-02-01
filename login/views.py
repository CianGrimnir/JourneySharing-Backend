from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from rest_framework.decorators import api_view
from services.dynamodb import DynamoDbService
import json
import services


# Create your views here.
@csrf_exempt
@api_view(["POST"])
def user_login(request):
    if request.method == 'POST':
        user_name = request.data.user
        auth_key = request.data.password
        dynamodbService = DynamoDbService('dynamodb', services.default_region, services.AWS_ACCESS_KEY_ID, services.AWS_SECRET_ACCESS_KEY)
        search_key = {'Username': user_name, 'Password': auth_key}
        get_items = dynamodbService.get_item_from_table('UserCreds', search_key)
        if get_items.errors is not None:
            response_body = {'status code': 404,
                             'body': f'user - {user_name} not found, error - {get_items.errors}',
                             }
            services.logger.debug(get_items.reason)
            return HttpResponseNotFound(json.dumps(response_body), content_type="application/json")
        elif get_items.item is None:
            response_body = {'status code': 404,
                             'body': 'user - ' + str(user_name) + ' not found',
                             }
            services.logger.debug(f'user_name does not exist in db')
            return HttpResponseNotFound(json.dumps(response_body), content_type="application/json")

        services.logger.info(f'{user_name} user authenticated')
        response_body = {'status code': 200,
                         'body': f'user - {user_name} authenticated successfully.',
                         }
        return HttpResponse(json.dumps(response_body), content_type="application/json")
    else:
        response_body = {'status code': 400,
                         'body': f'BAD REQUEST - expected POST, got {request.method}',
                         }
        return HttpResponse(json.dumps(response_body), content_type="application/json")
