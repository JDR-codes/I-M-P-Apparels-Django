from django.urls import path
from . import views

urlpatterns = [
    path('products/<str:cname>',views.products_view,name='products'),
    path('prd-det/<int:id>',views.product_details_view,name='prd-det'),
    path('wishlist/<int:id>',views.wishlist_view,name='wishlist'),
    path('user-wishlist',views.user_wishlist_view,name='user-wishlist'),
    path('myorders',views.myorders_view,name='myorders'),
    path('search-query',views.search_query_view,name='search-query'),
    path('rate-product/<int:product_id>',views.rate_product_view,name='rate-product'),
]