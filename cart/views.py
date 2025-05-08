from django.shortcuts import redirect, render
from . forms import AddCartForm
from . models import CartItems
from products.models import Size, Products
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user_profile.models import UserProfile
# Create your views here.

@login_required(login_url='login')
def cart_form_view(request,id):
    try:
        profile = UserProfile.objects.get(user = request.user)
    except:
        return redirect('create-profile')

    product = Products.objects.get(id = id)
    sizes_queryset = Size.objects.filter(pcode = product)
    size_choices =[(s.size,s.size) for s in sizes_queryset]

    if request.method == 'POST':
        form = AddCartForm(request.POST,size_choices = size_choices)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            size = form.cleaned_data['size']
            
            size_obj = Size.objects.get(pcode = product, size = size)
            if quantity <= size_obj.stock:
                cart_item,created = CartItems.objects.get_or_create(
                    cart_user = request.user,
                    product = Products.objects.get(id = id),
                    quantity = quantity,
                    size= size
                )
                if not created:
                    cart_item.quantity += 1
                cart_item.save()
                return redirect('prd-det', id =id)
            else:
                messages.error(request, 'Requested quantity not available')
                return redirect('cart-form', id = id)

    form = AddCartForm(size_choices = size_choices)
    return render(request,'cart_form.html',{'form' : form})

@login_required(login_url='login')
def cart_view(request):
    cart = CartItems.objects.filter(cart_user = request.user)
    total_price = 0
    msg = None
    if cart:
        for item in cart:
            total_price += item.total
    else:
        msg = 'Your Cart is empty !!!'

    return render(request,'cart.html',{'cart' : cart, 'total_price' : total_price,'msg' : msg})

def remove_item_view(request,id):
    cartitem = CartItems.objects.get(id = id)
    cartitem.delete()
    return redirect('cart')