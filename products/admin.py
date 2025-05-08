from django.contrib import admin
from . models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'cimage', 'cname']
    ordering = ['id']

class AccessoriesCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'acimage', 'acname']
    ordering = ['id']

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'pimage', 'pname', 'price', 'pcode',  'desc', 'trending', 'new', 'cname', 'acname']
    ordering = ['id']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'pcode', 'size', 'stock']
    ordering = ['id']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'added_at']
    ordering = ['id']


admin.site.register(Categories, CategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(AccessoriesCat,AccessoriesCategoryAdmin)
admin.site.register(WishList,WishListAdmin)