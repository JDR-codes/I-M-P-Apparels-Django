from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'is_email_verified']  # Add field here
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_email_verified',)}),  # Show in edit form
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_email_verified',)}),  # Show in add form
    )
