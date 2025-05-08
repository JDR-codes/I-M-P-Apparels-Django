from django.urls import path
from . import views

urlpatterns = [
    path('cart-form/<int:id>',views.cart_form_view,name='cart-form'),
    path('cart',views.cart_view,name='cart'),
    path('remove-item/<int:id>',views.remove_item_view,name='remove-item'),
]