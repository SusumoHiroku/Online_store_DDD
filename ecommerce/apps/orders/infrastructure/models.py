from django.db import models

class Order(models.Model):
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

