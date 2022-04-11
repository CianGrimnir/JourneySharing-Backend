from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'profile/', views.get_user_profile),
    re_path(r'update/', views.update_user_profile)
]
