from django.db import models


class Orders(models.Model):
    user_id = models.IntegerField()
    order_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.IntegerField()
    total_amount = models.FloatField()
    shipping_address = models.CharField(max_length= 255)


class OrdersItems(models.Model):
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
