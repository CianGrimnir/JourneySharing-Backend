from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.dynamodb import DynamoDbService
from services.redis import Redis
import services
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK)
import logging
from services import const

services.logger.setLevel(logging.INFO)


@csrf_exempt
@api_view(["POST"])
def get_user_profile(request):
    """
    returns the profile information of the requested user.
    returns: HTTPResponse with profile information as dict.
    """
    if request.method == 'POST':
        redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
        # TODO: add mechanism to verify and secure this profile sharing communication.
        request_token = request.data.get("token")
        email_address = request.data.get("email_address")
        auth_flag, reason = True, ""
        if not request_token:
            auth_flag, reason = False, "Missing"
        elif not redis_client.get_values(request_token) or redis_client.get_values(request_token).decode("utf-8") != email_address:
            auth_flag, reason = False, "Unauthorized"
        if not auth_flag:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'user - {email_address} {reason} request token.',
                             }
            services.logger.info(f"username - {email_address} {reason} request token.")
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        dynamodbService = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        search_key = {'email': email_address}
        # fetch profile information from the dynamodb using email_address as primary key.
        get_items = dynamodbService.get_item_from_table('user_profiles', search_key)
        services.logger.info(f"output from dynamodb - {get_items}")
        # If exception is raised from AWS API call
        if get_items.errors is not None:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': f'user - {email_address} bad request, error - {get_items.errors}',
                             }
            services.logger.info(get_items.reason)
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        # If there is no information for provided user information
        elif get_items.item is None:
            response_body = {'status code': HTTP_400_BAD_REQUEST,
                             'body': 'user - ' + str(email_address) + ' not found',
                             }
            services.logger.info(f'user_name {email_address} does not exist in db')
            return Response(response_body, status=HTTP_400_BAD_REQUEST)

        request_profile = ['user_id', 'first_name', 'last_name', 'phone_number', 'email', 'country', 'age']
        user_profile = dict((k, get_items.item[k]) for k in request_profile)
        services.logger.info(f'{email_address} user request processed successfully.')
        response_body = {'status code': HTTP_200_OK,
                         'body': user_profile,
                         }
        return Response(response_body, status=HTTP_200_OK)
