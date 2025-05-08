from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage_view,name='home'),
    path('category',views.categories_view,name='category'),
    path('acc-category',views.acc_categories_view,name='acc-category'),
]