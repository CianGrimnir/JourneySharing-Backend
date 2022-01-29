from django.shortcuts import render
import json
from pprint import pprint
import boto3

# Create your views here.
def register(user, passw):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserCreds')
    pprint(table)
    response = table.put_item(
       Item={
            'Username': user,
            'Password': passw
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
