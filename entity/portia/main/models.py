from django.db import models
from django.core.validators import validate_email

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=254, unique=True, validators = [validate_email])
    date_joined = models.DateTimeField()
    zipcode = models.IntegerField()
    password = models.CharField(max_length=96)    # TODO: hash later in project 4



class Pet(models.Model):
    name = models.CharField(max_length = 50)
    pet_type = models.CharField(max_length = 50)
    description = models.CharField(max_length = 1000)
    price = models.DecimalField(max_digits = 8, decimal_places = 3)
    date_posted = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)




class Authenticator(models.Model):
    authenticator = models.CharField(primary_key=True, max_length=255)
    user_id = models.IntegerField()
    date_created = models.DateTimeField()





