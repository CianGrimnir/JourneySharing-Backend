import django.core.management.commands.runserver as runserver
import requests
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT


class MyAppConfig:
    name = 'journeysharing'
    verbose_name = "Backpackers - Journey Sharing App"

    def __init__(self):
        self.current_port = None

    def ready(self):
        resp = True
        url = "http://localhost:8002/register?port="
        cmd = runserver.Command()
        self.current_port = cmd.default_port
        print("starting the application", self.current_port)
        try:
            resp = requests.get(url + self.current_port)
        except requests.exceptions.ConnectionError:
            resp = False
        return Response(status=HTTP_204_NO_CONTENT)
