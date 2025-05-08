from django.urls import path
from . import views

urlpatterns = [
    path('checkout',views.checkout_view,name='checkout'),
    path('payment-handler',views.payment_handler_view,name='payment-handler'),
]