from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Categories(models.Model):
    cimage = models.ImageField(upload_to='cat_image')
    cname = models.CharField(max_length=25)

    def __str__(self):
        return self.cname
    
class AccessoriesCat(models.Model):
    acimage = models.ImageField(upload_to='cat_image/acc-image')
    acname = models.CharField(max_length=20)

    def __str__(self):
        return self.acname
    
class Products(models.Model):
    pimage = models.ImageField(upload_to='products_image')
    pname = models.CharField(max_length=30, unique=False)
    pcode = models.CharField(max_length=10,null=True,blank=True)
    price = models.IntegerField()
    desc = models.TextField()
    trending = models.BooleanField()
    new = models.BooleanField()
    cname = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True,blank=True)
    acname = models.ForeignKey(AccessoriesCat,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.pcode
    
class Size(models.Model):
    size_choices = [
        ('S','S'),
        ('M','M'),
        ('L','L'),
        ('XL','XL'),
        ('XXL','XXL'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('10','10'),
        ('11','11'),
        ('12','12'),
        ('38','38'),
        ('40','40'),
        ('42','42'),
        ('free','free'),
        ('12L','12L'),
        ('15L','15L')
    ]

    pcode = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices = size_choices, null=True)
    stock = models.IntegerField(default = 5)
    
    def __str__(self):
        return self.pcode.pname


class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f'{self.user.username} -> {self.product.pname}'
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveSmallIntegerField()  
    review = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'product'] 

    def __str__(self):
        return f"{self.user} rated {self.product} - {self.stars} stars"