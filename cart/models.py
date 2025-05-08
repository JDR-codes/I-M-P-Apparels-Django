from django.db import models
from products.models import Products
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class CartItems(models.Model):
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=5)
    total = models.IntegerField(null=True, blank= True)
    

    def save(self , *args, **kwargs):
        self.total = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cart_user.username
    

