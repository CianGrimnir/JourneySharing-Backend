from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=5)
    email = models.CharField(max_length=30)
    phone_number = models.BigIntegerField()
    # Add validator method to verify email and other data validity.

    def __str__(self):
        return self.first_name + " " + self.last_name
