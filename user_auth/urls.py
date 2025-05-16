from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),  
    path('verify-email/<uidb64>/<token>/', views.verify_email_view, name='verify-email'), 
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('email-verified',views.email_verified_view,name='email-verified'),
    path('password-reset/', views.custom_password_reset_view, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
]