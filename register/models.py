from django.db import models
from django.core.validators import EmailValidator


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    age = models.IntegerField()
    email = models.CharField(max_length=30, validators=EmailValidator)
    phone_number = models.BigIntegerField(max_length=10)
