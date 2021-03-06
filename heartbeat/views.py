from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT


@api_view(('GET',))
def heart_beat(request):
    """
    Basic HearBeat mechanism that will allow LoadBalancer to check if the service is alive or down.
    """
    return Response(status=HTTP_204_NO_CONTENT)
