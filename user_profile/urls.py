from django.urls import path
from . import views

urlpatterns = [
    path('create-profile',views.create_profile_view,name='create-profile'),
    path('user-profile',views.user_profile_view,name='user-profile'),
    path('edit-profile',views.edit_profile_view,name='edit-profile'),
    path('add-address',views.add_address_view,name='add-address'),
    path('saved-address',views.saved_address_view,name='saved-address'),
    path('delete-address/<int:id>',views.delete_address_view,name='delete-address')
]