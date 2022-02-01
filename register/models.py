from django.db import models
from django.core.validators import EmailValidator, DecimalValidator


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(max_length=30, validators=EmailValidator)
    phone_number = models.DecimalField(max_length=10, validators=DecimalValidator(10))
