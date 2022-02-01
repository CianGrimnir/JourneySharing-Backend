from django.shortcuts import render
import json


# Create your views here.
def user_register(request):
    if request.method == "PUT":
        json_data = json.loads(str(request.body, encoding='utf-8'))
