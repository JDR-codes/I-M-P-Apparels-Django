from django.shortcuts import redirect, render
from . forms import AddCartForm, CouponApplyForm
from . models import CartItems, Coupon, Cart, UserCoupon
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

            cart, created = Cart.objects.get_or_create(user=request.user)

            if quantity <= size_obj.stock:
                cart_item,created = CartItems.objects.get_or_create(
                    cart = cart,
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
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    cartitems = CartItems.objects.filter(cart=cart)
    total_price = 0
    discount = 0
    final_price = 0
    msg = None
    applied_code = ''

    if cartitems.exists():
        total_price = cart.total

        # Check if a coupon is applied
        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            try:
                coupon = Coupon.objects.get(id=coupon_id)

                if coupon.is_valid():
                    # Check if the coupon is one-time and already used by the user
                    if coupon.one_time:
                        user_coupon, created = UserCoupon.objects.get_or_create(user=request.user, coupon=coupon)
                        if user_coupon.used:
                            messages.error(request, "This coupon has already been used.")
                            del request.session['coupon_id']  
                        else:
                            discount = float((coupon.discount / 100)) * float(total_price)
                            applied_code = coupon.code
                            messages.success(request, f"Coupon '{applied_code}' applied successfully!")
                            # Mark the coupon as used for this user
                            user_coupon.used = True
                            user_coupon.save()
                    else:
                        discount = float((coupon.discount / 100)) * float(total_price)
                        applied_code = coupon.code
                        messages.success(request, f"Coupon '{applied_code}' applied successfully!")
                else:
                    del request.session['coupon_id']  
                    messages.error(request, "This coupon is no longer valid.")
            except Coupon.DoesNotExist:
                del request.session['coupon_id'] 
                messages.error(request, "This coupon does not exist.")
        
        final_price = float(total_price) - discount
    else:
        msg = 'Your Cart is empty!'

    # Handle coupon form submission
    if request.method == 'POST':
        if 'remove_coupon' in request.POST:
            request.session.pop('coupon_id', None)
            return redirect('cart')
        else:
            form = CouponApplyForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                try:
                    coupon = Coupon.objects.get(code__iexact=code)
                    if coupon.is_valid():
                        # Handle one-time use coupon
                        if coupon.one_time:
                            user_coupon, created = UserCoupon.objects.get_or_create(user=request.user, coupon=coupon)
                            if user_coupon.used:
                                form.add_error('code', 'This coupon has already been used.')
                            else:
                                request.session['coupon_id'] = coupon.id
                                return redirect('cart')
                        else:
                            request.session['coupon_id'] = coupon.id
                            return redirect('cart')
                    else:
                        form.add_error('code', 'This coupon is not valid anymore.')
                except Coupon.DoesNotExist:
                    form.add_error('code', 'This coupon does not exist.')
    else:
        form = CouponApplyForm(initial={'code': applied_code})

    context = {
        'cartitems': cartitems,
        'total_price': total_price,
        'discount': discount,
        'final_price': final_price,
        'msg': msg,
        'form': form,
        'applied_code': applied_code,
    }
    return render(request, 'cart.html', context)

def remove_item_view(request,id):
    cartitem = CartItems.objects.get(id = id)
    cartitem.delete()
    return redirect('cart')

