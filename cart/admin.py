from django.contrib import admin
from . models import CartItems, Coupon, Cart, UserCoupon
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'size', 'total']
    ordering = ['id']

admin.site.register(CartItems,CartAdmin)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'updated_at']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'valid_from', 'valid_to', 'active', 'one_time']

@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon', 'used']