from django.db import models


class Customers(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length= 255)
    adresse = models.CharField(max_length= 255)
    email = models.CharField(max_length= 255)
    company = models.CharField(max_length= 255)
    phone = models.IntegerField()
