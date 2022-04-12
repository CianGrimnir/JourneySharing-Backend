import os
import binascii
import uuid
from journeysharing import settings
from services.redis import Redis


def get_token() -> str:
    """
    Function for generating a login token.
    """
    return binascii.hexlify(os.urandom(20)).decode()


def generate_uniqid() -> str:
    """
    Function for generating a unique identifier for journey_id.
    """
    return uuid.uuid4().hex[:15]


def generate_expression(attribute_values) -> (str, dict):
    """
    function for generating an expression strings required for DynamoDB update call.
    :param attribute_values: values to be updated in the DynamoDB table.
    :return: expression str and dict to be used for update_item API call.
    - expression: UpdateExpression required for update_item.
    - expressionValue: ExpressionAttributeValues required for update_item.
    """
    expression = "SET "
    place_holder = "var"
    counter = 1
    expression_value = {}
    for index, (k, v) in enumerate(attribute_values.items()):
        temp_expression = f":{place_holder}{counter}"
        temp_exp = f"{k}= {temp_expression}"
        expression += temp_exp
        expression_value[temp_expression] = v
        counter += 1
        if index != len(attribute_values) - 1:
            expression += ", "
    return expression, expression_value


def check_request_auth(request) -> (bool, str):
    """
    function to validate the token of the requested user.
    :param request: 'HttpRequest' wrapper object.
    :return: status of the logout request.
    - auth_flag - contains the status of the logout request.
    - reason - contains the error log if any error happens.
    """
    redis_client = Redis(hostname=settings.REDIS_HOST, port=settings.REDIS_PORT)
    request_token = request.data.get("token")
    email_address = request.data.get("email_address")
    auth_flag, reason = True, ""
    if not request_token:
        auth_flag, reason = False, "Missing"
    elif not redis_client.get_values(request_token) or redis_client.get_values(request_token).decode("utf-8") != email_address:
        auth_flag, reason = False, "Unauthorized"
    return auth_flag, reason


def build_response_dict(status_code: int, message: str) -> dict:
    """
    function for building response dict.
    :param status_code: HTTP response code.
    :param message: response body.
    :return: response dictionary
    """
    return {'status code': status_code,
            'body': message
            }
