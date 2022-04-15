from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'createNewRequest/', views.new_journey_user_request),
    re_path(r'joinJourney/', views.join_existing_journey)
]
