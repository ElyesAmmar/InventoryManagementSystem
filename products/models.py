from django.db import models


class Products(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length= 255)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.CharField(max_length= 2083)
    barcode = models.IntegerField()
    category = models.CharField(max_length= 255)

