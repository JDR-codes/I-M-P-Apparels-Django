from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),  
    path('verify-email/<uidb64>/<token>/', views.verify_email_view, name='verify_email'), 
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('email-verified',views.email_verified_view,name='email-verified'),
]