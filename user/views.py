from django.views.decorators.csrf import csrf_exempt
import django.http.request
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
from services import const, utils

services.logger.setLevel(logging.INFO)


@csrf_exempt
@api_view(["POST"])
def get_user_profile(request):
    """
    returns the profile information of the requested user.
    returns: HTTPResponse with profile information as dict.
    """
    if request.method == 'POST':
        email_address = request.data.get("email_address")
        auth, reason = utils.check_request_auth(request)
        if not auth:
            response_body = utils.build_response_dict(HTTP_400_BAD_REQUEST, f'user - {email_address} {reason} request token.')
            services.logger.info(f"username - {email_address} {reason} request token.")
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        dynamodb_service = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        search_key = {'email': email_address}
        # fetch profile information from the dynamodb using email_address as primary key.
        get_items = dynamodb_service.get_item_from_table('user_profiles', search_key)
        services.logger.info(f"output from dynamodb - {get_items}")
        # If exception is raised from AWS API call
        if get_items.errors is not None:
            response_body = utils.build_response_dict(HTTP_400_BAD_REQUEST, f'user - {email_address} bad request, error - {get_items.errors}')
            services.logger.info(get_items.reason)
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        # If there is no information for provided user information
        elif get_items.item is None:
            response_body = utils.build_response_dict(HTTP_400_BAD_REQUEST, f'user {str(email_address)} not found')
            services.logger.info(f'user_name {email_address} does not exist in db')
            return Response(response_body, status=HTTP_400_BAD_REQUEST)

        request_profile = ['user_id', 'first_name', 'last_name', 'phone_number', 'email', 'country', 'age', 'gender']
        user_profile = dict((k, get_items.item[k]) for k in request_profile)
        services.logger.info(f'{email_address} user request processed successfully.')
        response_body = utils.build_response_dict(HTTP_200_OK, user_profile)
        return Response(response_body, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def update_user_profile(request):
    """
    returns the updated profile information of the user.
    returns: HTTPResponse with profile information as dict.
    """
    if request.method == 'POST':
        email_address = request.data.get("email_address")
        auth, reason = utils.check_request_auth(request)
        if not auth:
            response_body = utils.build_response_dict(HTTP_400_BAD_REQUEST, f'user - {email_address} {reason} request token.')
            services.logger.info(f"username - {email_address} {reason} request token.")
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        if isinstance(request.data, django.http.request.QueryDict):
            update_profile_data = request.data.dict()
        else:
            update_profile_data = request.data
        services.logger.info(f"removing unwanted information {[update_profile_data.pop(key) for key in ['token', 'email_address']]}")
        dynamodb_service = DynamoDbService('dynamodb', const.default_region, const.AWS_ACCESS_KEY_ID, const.AWS_SECRET_ACCESS_KEY)
        search_key = {'email': email_address}
        # fetch profile information from the dynamodb using email_address as primary key.
        update_items = dynamodb_service.update_item('user_profiles', search_key, update_profile_data)
        services.logger.info(f"output from dynamodb - {update_items}")
        # If exception is raised from AWS API call
        if update_items.errors is not None:
            response_body = utils.build_response_dict(HTTP_400_BAD_REQUEST, f'user - {email_address} bad request, error - {update_items.errors}')
            services.logger.info(update_items.reason)
            return Response(response_body, status=HTTP_400_BAD_REQUEST)
        # If there is no information for provided user information
        elif update_items.item is None:
            response_body = utils.build_response_dict(HTTP_400_BAD_REQUEST, f'user - {str(email_address)} not found')
            services.logger.info(f'user_name {email_address} does not exist in db')
            return Response(response_body, status=HTTP_400_BAD_REQUEST)

        response_body = utils.build_response_dict(HTTP_200_OK, update_items.item)
        return Response(response_body, status=HTTP_200_OK)

