from django.shortcuts import render
import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

# Create your views here.
def login(user, passw):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('UserCreds')
    try:
        response = table.get_item(Key={'Username': user, 'Password': passw})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']
        
    return False
    