import os
import binascii
import uuid


def get_token():
    """
    Function for generating a login token.
    """
    return binascii.hexlify(os.urandom(20)).decode()


def generate_uniqid():
    """
    Function for generating a unique identifier for journey_id.
    """
    return uuid.uuid4().hex[:15]


def generate_expression(attribute_values):
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
    expressionValue = {}
    for index, (k, v) in enumerate(attribute_values.items()):
        temp_expression = f":{place_holder}{counter}"
        temp_exp = f"{k}= {temp_expression}"
        expression += temp_exp
        expressionValue[temp_expression] = v
        counter += 1
        if index != len(attribute_values) - 1:
            expression += ", "
    return expression, expressionValue
