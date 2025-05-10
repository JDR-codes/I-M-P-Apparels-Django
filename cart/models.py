from django.db import models
from products.models import Products
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        total = sum(item.total for item in self.items.all())
        self.total = total
        self.save()

    def __str__(self):
        return f'cart of {self.user.username}'

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items',null=True,blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=5)
    total = models.IntegerField(null=True, blank= True)
    

    def save(self , *args, **kwargs):
        self.total = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cart.user.username
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(help_text="Discount percentage")
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    one_time = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to
    
class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'coupon')  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"