from django.contrib import admin
from . models import CartItems
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_user', 'product', 'quantity', 'size', 'total']
    ordering = ['id']

admin.site.register(CartItems,CartAdmin)