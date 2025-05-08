from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'razorpay_id', 'is_paid', 'total_price']
    ordering = ['id']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'size']
    ordering = ['id']

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)