from django.contrib import admin
from . models import *
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'city', 'state', 'postal_code', 'profile_picture', 'created_at']
    ordering = ['id']

class UserSavedAddress(admin.ModelAdmin):
    list_display = ['id', 'user', 'address']

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(SavedAddress,UserSavedAddress)