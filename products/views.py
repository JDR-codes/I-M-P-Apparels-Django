from django.shortcuts import redirect, render, get_object_or_404
from . models import *
from orders.models import *
from django.db.models import Q
from . forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

def products_view(request,cname):
    try:
        catname = Categories.objects.get(cname = cname)
        products = Products.objects.filter(cname = catname)
    except:
        catname = AccessoriesCat.objects.get(acname = cname)
        products = Products.objects.filter(acname = catname)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte = min_price)
    if max_price:
        products = products.filter(price__lte = max_price)
    
    sort_by = request.GET.get('sort_by')
    if sort_by in ['price', '-price']:
        products = products.order_by(sort_by)
    
    return render(request,'products.html',{
        'products' : products,
        'min_price' : min_price,
        'max_price' : max_price,
        'sort_by' : sort_by
        })

def product_details_view(request,id):
    prd_det = Products.objects.get(id = id)
    prd_sizes = Size.objects.filter(pcode = id)
    user = User.objects.get(username = request.user)
    try:
        ratings = Rating.objects.filter(product = id)
    except:
        ratings = None
    try:
        product = WishList.objects.get(user = user, product = id)
    except:
        product = None
    context = {
        'prd_det' : prd_det,
        'prd_sizes' : prd_sizes,
        'wishlist' :product,
        'ratings' : ratings
    }
    return render(request,'prd_details.html',context)

def wishlist_view(request,id):
    try:
        wish_product = WishList.objects.get(product = id, user = request.user)
        wish_product.delete()
    except:
        product = Products.objects.get(id = id)
        WishList.objects.create(
            user = request.user,
            product = product,
        )
    return redirect('prd-det',id)

def user_wishlist_view(request):
    user = User.objects.get(username = request.user)
    products = WishList.objects.filter(user = user)
    return render(request,'wishlist.html',{'products':products})

def myorders_view(request):
    orders = Order.objects.filter(user = request.user, is_paid = True)
    return render(request,'myorders.html',{'orders':orders})
    
def search_query_view(request):
    query = request.GET.get('q')
    print(query)
    if query:
        products = Products.objects.filter(
            Q(pname__icontains = query) |
            Q(cname__cname__icontains = query) |
            Q(acname__acname__icontains = query)
        )
    else:
        return redirect('home')
    return render(request,'products.html',{'search_results' : products if query else None})

@login_required
def rate_product_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    try:
        rating = Rating.objects.get(user=request.user, product=product)
    except Rating.DoesNotExist:
        rating = None

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            new_rating = form.save(commit=False)
            new_rating.user = request.user
            new_rating.product = product
            new_rating.save()
            return redirect('prd-det', id = product_id)
    else:
        form = RatingForm(instance=rating)

    return render(request, 'rate_product.html', {'product': product, 'form': form})